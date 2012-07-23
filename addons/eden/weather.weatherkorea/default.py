# -*- coding: utf-8 -*-

# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *

import os, sys, urllib2, socket, json, re, datetime, sqlite3
from xml.etree import ElementTree
import xbmcgui, xbmcaddon

__addonID__    = "weather.weatherkorea"
__addon__      = xbmcaddon.Addon( id=__addonID__ )
__service__    = __addon__.getAddonInfo('name')
__script__     = __addon__.getAddonInfo('id')
__cwd__        = __addon__.getAddonInfo('path')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString
__resource__   = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')).decode("utf-8")

sys.path.append (__resource__)

from utilities import *

CODEDB = xbmc.translatePath(os.path.join( __resource__, "codes.db"))
CURRENT_CITY_WEATHER_URL = 'http://www.kma.go.kr/repositary/xml/weather/sfc_web_now.xml'
CURRENT_WEATHER_URL = 'http://www.kma.go.kr/wid/queryODAM.jsp?gridx=%s&gridy=%s'
DAY_WEATHER_URL = 'http://www.kma.go.kr/wid/queryNewDFS.jsp?gridx=%s&gridy=%s'
MIDTERM_WEATHER_URL = 'http://www.kma.go.kr/weather/forecast/mid-term-xml.jsp?stnId=%s'
UV_INDEX_URL = 'http://www.kma.go.kr/repositary/xml/imi2/FCT_IMI2_A07.csv'

WEATHER_WINDOW  = xbmcgui.Window(12600)

socket.setdefaulttimeout(10)

def set_property(name, value):
    WEATHER_WINDOW.setProperty(name, value)

def refresh_locations():
    locations = 0
    for count in range(1, 4):
        loc_name = __addon__.getSetting('Location%s' % count)
        if loc_name != '':
            locations += 1
        else:
            __addon__.setSetting('Location%sid' % count, '')
        set_property('Location%s' % count, loc_name)
    set_property('Locations', str(locations))

def getUVIndex(citycode):
    csv_string = urllib2.urlopen(UV_INDEX_URL).read()
    uvi = re.search(re.compile(r'A07#%s#\d{10}#(\d\.\d)#(\d\.\d)#' % citycode), csv_string).group(1)
    return uvi

def getGridXY(code):
    con = sqlite3.connect(CODEDB)
    xbmc.log( "code(%s)" % code, xbmc.LOGDEBUG )
    with con:    
        cur = con.cursor()    
        cur.execute("SELECT x, y FROM donglist WHERE code = ?", [str(code).decode('utf-8')])
        gridxy = cur.fetchone()
    return gridxy

def getCityCode(code):
    con = sqlite3.connect(CODEDB)
    with con:    
        cur = con.cursor()
        cur.execute("SELECT mappingnum FROM donglist WHERE code = ?", [code])
        mappingnum = cur.fetchone()
        cur.execute("SELECT * FROM dongmapping WHERE num = ?", mappingnum)
        row = cur.fetchone()
    citycode = {'sumstn':row[7],'weeklystn':row[8],'nowstn':row[9],'recentstn':row[10],'weekendstn':row[11]}
    return citycode

def currentSummary(tm, spot_data ,city_data):
    city_special_weather = ('fog/ice fog', 'mist', 'haze', 'thunderstorm/rain', 'lightning', 'blowing snow', 'rime')
    daych = DAY_RANGES[int(tm[4:-6])-1][0] <= tm[8:-2] <= DAY_RANGES[int(tm[4:-6])-1][1]
    night_weathers = ('Clear', 'Snow', 'Rainy', 'Mostly Cloudy', 'Little Cloudy')
    if city_data and (city_data.lower() in city_special_weather):
        wfEn = WEATHER_CONVERSION[city_data.lower()]
    else : wfEn = WEATHER_CONVERSION[spot_data.lower()]
    if wfEn in night_weathers and not daych:
        wfEn = "Night_" + wfEn
    return wfEn
    
def forecastWorst(wfEn):
    if 'Rainy' and 'Snow'in wfEn or 'Snow/Rain' in wfEn:
        sum_wfEn = 'Snow/Rain'
    elif 'Rainy' in wfEn:
        sum_wfEn = 'Rainy'
    elif 'Snow' in wfEn:
        sum_wfEn = 'Snow'
    elif 'Mostly Cloudy' in wfEn:
        sum_wfEn = 'Mostly Cloudy'
    elif 'Little Cloudy' in wfEn:
        sum_wfEn = 'Little Cloudy'
    return WEATHER_CONVERSION[sum_wfEn]

def ShortForecastSummary(current_tm, short_tm, short_data):
    tot_0_wfEn = []
    tot_1_wfEn = []
    if short_tm < current_tm :
        tmEf = 1
    else :
        tmEf = 0
    for element in short_data:
        if element.find('day').text == str(tmEf):
            tot_0_wfEn.append(element.find('wfEn').text)
            short_0_tmx = element.find('tmx').text
            short_0_tmn = element.find('tmn').text
        elif element.find('day').text == str(tmEf+1):
            tot_1_wfEn.append(element.find('wfEn').text)
            short_1_tmx = element.find('tmx').text
            short_1_tmn = element.find('tmn').text
    if float(short_0_tmx) < -900:
        short_0_tmx = '-'
    if float(short_0_tmn) < -900:
        short_0_tmn = '-'
    short_summary = [[current_tm.strftime('%a'),forecastWorst(tot_0_wfEn), short_0_tmx, short_0_tmn]
                     ,[(current_tm + datetime.timedelta(days=1)).strftime('%a'), forecastWorst(tot_1_wfEn), short_1_tmx, short_1_tmn]]

    return short_summary

def fetch(url):
    xbmc.log( "url: %s" % url, xbmc.LOGDEBUG )
    MAX_ATTEMPTS = 8
    for attempt in range(MAX_ATTEMPTS):
        try:
            req = urllib2.urlopen(url, timeout = 2)
        except urllib2.URLError, e:
            xbmc.log( "urllib2: %s" % e.args, xbmc.LOGDEBUG )
        try:
            parsed_xml = ElementTree.parse(req)
            req.close()
            break
        except:
            xbmc.log( "ElementTree: parse error", xbmc.LOGDEBUG )
    return parsed_xml

def location(step,code):
    loc   = []
    locid = []
    con = sqlite3.connect(CODEDB)
    with con:
        cur = con.cursor()    
        if step == 0:
            cur.execute("SELECT sido FROM donglist ORDER BY sidonum")
            sidos = cur.fetchall()
            for sido in sidos:
                if not(sido[0] in loc):
                    loc.append(sido[0])
                    locid.append(sido[0])
        elif step == 1:
            cur.execute("SELECT gugun FROM donglist WHERE sido LIKE ? ORDER BY code", [code])
            guguns = cur.fetchall()
            for gugun in guguns:
                if not(gugun[0] in loc):
                    loc.append(gugun[0])
                    locid.append(gugun[0])
        elif step == 2:
            cur.execute("SELECT dong, code FROM donglist WHERE gugun LIKE ? ORDER BY code", [code])
            dongs = cur.fetchall()
            for dong in dongs:
                loc.append(dong[0])
                locid.append(dong[1])
    return loc, locid

def forecast(code):
    gridxy = getGridXY(code)
    citycode = getCityCode(code)
    xbmc.log("citycode(%s)" % citycode['nowstn'], xbmc.LOGDEBUG )
    current_city_data = fetch(CURRENT_CITY_WEATHER_URL)
    current_spot_data = fetch(CURRENT_WEATHER_URL % (gridxy[0], gridxy[1]))
    shortterm_data = fetch(DAY_WEATHER_URL % (gridxy[0], gridxy[1]))
    midterm_data = fetch(MIDTERM_WEATHER_URL % (citycode['weeklystn'])[:-18])

    city_data_all = current_city_data.findall("{0}weather/{0}local".format("{sfc_now}"))
    city_data = [c for c in city_data_all if c.get('stn_id') == str(citycode['nowstn'])][0].attrib
    spot_data = current_spot_data.find('body/data')
    short_data = shortterm_data.findall('body/data')
    mid_data_all = midterm_data.findall("body/location")
    mid_data = [c for c in mid_data_all if c.get('city') == str((citycode['weeklystn'])[13:])][0]

    c_tm = current_spot_data.find('header/tm').text
    s_tm = shortterm_data.find('header/tm').text
    current_tm = datetime.datetime(int(c_tm[0:4]), int(c_tm[4:6]), int(c_tm[6:8]))
    short_tm = datetime.datetime(int(s_tm[0:4]), int(s_tm[4:6]), int(s_tm[6:8]))
    wfEn = currentSummary(c_tm, spot_data.find('wfEn').text ,city_data['ww'])
    weeklyForecast = ShortForecastSummary(current_tm, short_tm, short_data)
    midterm_wf = mid_data.findall('data')
    for element in midterm_wf:
        tmEf = datetime.datetime(int(element.find('tmEf').text[0:4]),int(element.find('tmEf').text[5:7]),int(element.find('tmEf').text[8:10]))
        if (tmEf - current_tm) > datetime.timedelta(days=1):
            weeklyForecast.append([tmEf.strftime('%a'), element.find('wf').text, element.find('tmx').text, element.find('tmn').text])
    if not city_data['ww_ko'] == '':
        currentCond = spot_data.find('wfKor').text + '/' + city_data['ww_ko']
    else :
        currentCond = spot_data.find('wfKor').text

    set_property('Current.Condition', currentCond)
    set_property('Current.Temperature', str(int(round(float(spot_data.find('temp').text),0))))
    set_property('Current.Wind', str(int(round(float(spot_data.find('ws').text),0))))
    set_property('Current.WindDirection', spot_data.find('wdEn').text)
    set_property('Current.Humidity', spot_data.find('reh').text)
    set_property('Current.FeelsLike', getFeelsLike(spot_data.find('temp').text, spot_data.find('ws').text))
    set_property('Current.UVIndex', getUVIndex(citycode['nowstn']))
    set_property('Current.DewPoint', getDewPoint(spot_data.find('temp').text, spot_data.find('reh').text))
    set_property('Current.OutlookIcon', "%s.png" % WEATHER_CODES[wfEn])
    set_property('Current.FanartCode', WEATHER_CODES[wfEn])
    xbmc.log( "wfen(%s)" % wfEn.encode("utf-8"), xbmc.LOGDEBUG ) 
    for count in range (0, len(weeklyForecast)):
        set_property('Day%i.Title'       % count, DAYS[weeklyForecast[count][0]])
        set_property('Day%i.HighTemp'    % count, weeklyForecast[count][2])
        set_property('Day%i.LowTemp'     % count, weeklyForecast[count][3])
        set_property('Day%i.Outlook'     % count, weeklyForecast[count][1])
        set_property('Day%i.OutlookIcon' % count, '%s.png' % WEATHER_CODES[WEATHER_CONVERSION[weeklyForecast[count][1].lower()]])
        set_property('Day%i.FanartCode'  % count, WEATHER_CODES[WEATHER_CONVERSION[weeklyForecast[count][1].lower()]])
        xbmc.log( "wfkr(%s)" % weeklyForecast[count][1].encode("utf-8"), xbmc.LOGDEBUG )
        
def clear():
    set_property('Current.Condition'     , '없음')
    set_property('Current.Temperature'   , '0')
    set_property('Current.Wind'          , '0')
    set_property('Current.WindDirection' , '없음')
    set_property('Current.Humidity'      , '0')
    set_property('Current.FeelsLike'     , '0')
    set_property('Current.UVIndex'       , '0')
    set_property('Current.DewPoint'      , '0')
    set_property('Current.OutlookIcon'   , 'na.png')
    set_property('Current.FanartCode'    , 'na')
    for count in range (0, 4):
        set_property('Day%i.Title'       % count, '없음')
        set_property('Day%i.HighTemp'    % count, '0')
        set_property('Day%i.LowTemp'     % count, '0')
        set_property('Day%i.Outlook'     % count, '없음')
        set_property('Day%i.OutlookIcon' % count, 'na.png')
        set_property('Day%i.FanartCode'  % count, 'na')

if sys.argv[1].startswith('Location'):
    dialog = xbmcgui.Dialog()
    locations_sido, locationids_sido = location(0,0)
    if locations_sido != []:
        selected_sido = dialog.select('시/도', locations_sido)
        if selected_sido != -1:
            locations_gugun, locationids_gugun = location(1,locationids_sido[selected_sido])
            if locations_gugun != []:
                selected_gugun = dialog.select(locations_sido[selected_sido].encode('utf-8')+'-시/구/군', locations_gugun)
                if selected_gugun != -1:
                    locations_dong, locationids_dong = location(2,locationids_gugun[selected_gugun])
                    if locations_dong != []:
                        selected_dong = dialog.select(locations_gugun[selected_gugun].encode('utf-8')+'-동/면/읍', locations_dong)
                        if selected_dong != -1:
                            __addon__.setSetting(sys.argv[1], locations_dong[selected_dong])
                            __addon__.setSetting(sys.argv[1] + 'id', str(locationids_dong[selected_dong]))
                            xbmc.log( "location: %s" % locations_dong[selected_dong].encode('utf-8'), xbmc.LOGDEBUG )
                            xbmc.log( "locationid: %s" % str(locationids_dong[selected_dong]).encode('utf-8'), xbmc.LOGDEBUG )
                    else:
                        dialog.ok(__provider__, xbmc.getLocalizedString(284))
            else:
                dialog.ok(__provider__, xbmc.getLocalizedString(284))
    else:
        dialog.ok(__provider__, xbmc.getLocalizedString(284))

else:
    location = __addon__.getSetting('Location%sid' % sys.argv[1])
    if (location == '') and (sys.argv[1] != '1'):
        location = __addon__.getSetting('Location1id')
    if not location == '':
        forecast(location)
    else:
        clear()
        # workaround to stop xbmc from running the script in a loop when no locations are set up:
        #set_property('Locations', '1')

refresh_locations()
set_property('WeatherProvider', '기상청(KMA)')
