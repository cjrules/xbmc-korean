# -*- coding: utf-8 -*- 
import xbmc, math

DAYS = { "Mon": xbmc.getLocalizedString( 11 ),
         "Tue": xbmc.getLocalizedString( 12 ),
         "Wed": xbmc.getLocalizedString( 13 ),
         "Thu": xbmc.getLocalizedString( 14 ),
         "Fri": xbmc.getLocalizedString( 15 ),
         "Sat": xbmc.getLocalizedString( 16 ),
         "Sun": xbmc.getLocalizedString( 17 )}

DAY_RANGES = [(8,18), (7,18), (7,19), (6, 19), (5,20), (5,20), (5, 20), (6,19), (6,19), (7, 18), (7,17), (8,17)]

# http://forum.xbmc.org/showthread.php?tid=123332&pid=1022495
# http://illuminatedimages.co.uk/xbmc_skin/grid.jpg

WEATHER_CODES = {
    #KMA:                  code  DESCRIPTION
    '':                    'na', #Not Available
    '':                    '0',  #Tornado 용오름
    '':                    '1',  #Tropical Storm 열대 폭풍 (약한 태풍)
    '':                    '2',  #Hurricane 태풍
    '':                    '3',  #Severe Thunderstorms 강한 뇌우
    'Thunderstorms':       '4',  #Thunderstorms 뇌우
    'Snow/Rain':           '5',  #Rain Snow 진눈깨비
    '':                    '6',  #Rain Sleet 진눈깨비 
    '':                    '7',  #Snow/Rain Icy Mix 진눈깨비
    '':                    '8',  #Freezing Drizzle 차가운 안개비 
    'Drizzle':             '9',  #Drizzle 안개비
    '':                    '10', #Freezing Rain 차가운 비
    'Showers':             '11', #Showers 소나기
    '':                    '12', #Heavy Rain 폭우
    '':                    '13', #Snow Flurries 약한 눈이 잠깐 내리는것
    '':                    '14', #Light Snow 약한 눈
    '':                    '15', #Snowflakes 함박눈
    '':                    '16', #Heavy Snow 폭설
    '':                    '17', #Thunderstorms 뇌우 #4
    '':                    '18', #Hail 우박
    'Dust':                '19', #Dust 먼지바람, 황사
    'Fog':                 '20', #Fog 안개
    'Haze':                '21', #Haze 연무, 박무(mist)
    '':                    '22', #Smoke 스모크 (대기오염)
    '':                    '23', #Blustery 돌풍
    'Windy':               '24', #Windy 강한바람
    'Frigid':              '25', #Frigid 강추위
    'Cloudy':              '26', #Cloudy 흐림
    'Night_Mostly Cloudy': '27', #Mostly Cloudy Night 구름 많음
    'Mostly Cloudy':       '28', #Mostly Cloudy
    'Night_Partly Cloudy': '29', #Partly Cloudy Night 구름 약간
    'Partly Cloudy':       '30', #Partly Cloudy
    'Night_Clear':         '31', #Clear Night 맑음
    'Clear':               '32', #Sunny 맑음
    '':                    '33', #Mostly Clear Night 
    '':                    '34', #Mostly Sunny
    '':                    '35', #Rain and Hail 비와 우박
    'Hot':                 '36', #Hot 
    'Thunder':             '37', #Isolated Thunder 국지적 천둥
    '':                    '38', #Scattered Thunderstorms 산발적인 뇌우
    'Scattered Rain':      '39', #Scattered Rain 산발적인 비
    'Rainy':               '40', #Heavy Rain 폭우
    'Snow':                '41', #Scattered Snow 때때로 눈
    '':                    '42', #Heavy Snow 폭설
    '':                    '43', #Windy/Snow 강한바람과 눈
    '':                    '44', #Partly Cloudy Day 구름 약간
    'Night_Rainy':         '45', #Scattered Showers Night 산발적인 소나기
    'Night_Snow':          '46', #Snowy Night
    '':                    '47', #Scattered Thunderstorms Night
    }

WEATHER_CONVERSION = {
    u'맑음':               'Clear',
    u'구름조금':            'Partly Cloudy',
    u'구름많음':            'Mostly Cloudy',
    u'구름 조금':           'Partly Cloudy',
    u'구름 많음':           'Mostly Cloudy',
    u'흐림':               'Cloudy',
    u'구름많고 비':         'Rainy',
    u'흐리고 비':           'Rainy',
    u'구름많고 눈':         'Snow',
    u'흐리고 눈':           'Snow',
    u'구름많고 눈 또는 비':  'Snow/Rain',
    u'흐리고 눈 또는 비':    'Snow/Rain',
    u'비 끝남':            'Mostly Cloudy',
    u'눈 끝남':            'Mostly Cloudy',
    u'소나기':             'Showers',
    u'비':                'Rainy',
    u'약한비계속':         'Scattered Rain',
    u'약한비단속':         'Scattered Rain',
    u'약한이슬비':         'Drizzle',
    u'눈':                'Snow',
    u'약한눈계속':         'Snow',
    u'약한눈단속':         'Scattered Snow',
    u'눈 또는 비':         'Snow/Rain',
    u'약진눈깨비':         'Snow/Rain',
    u'천둥번개':           'Thunderstorms',
    u'안개':              'Fog',
    u'박무':              'Haze',
    u'연무':              'Haze',
    u'황사':              'Dust',
    'sunny':                       'Clear',
    'clear':                       'Clear',
    'clearly':                     'Clear',
    'partly cloudy':               'Partly Cloudy',
    'little cloudy':               'Partly Cloudy',
    'funnel cloud':                'Mostly Cloudy',
    'most cloudy':                 'Mostly Cloudy',
    'mostly cloudy':               'Mostly Cloudy',
    'preceding rain':              'Cloudy',
    'preceding drizzle':           'Cloudy',
    'preceding shower snow':       'Cloudy',
    'preceding shower rain':       'Cloudy',
    'preceding rain/snow':         'Cloudy',
    'preceding snow':              'Cloudy',
    'preceding thunderstorm':      'Cloudy',
    'precipitation within sight':  'Cloudy',
    'rain':                        'Rainy',
    'rainy':                       'Rainy',
    'cloudy':                      'Cloudy',
    'snow':                        'Snow',
    'fog/ice fog':                 'Fog',
    'mist':                        'Haze',
    'haze':                        'Haze',
    'preceding fog':               'Haze',
    'rain/snow':                   'Snow/Rain',
    'rain and snow':               'Snow/Rain',
    'thunderstorm/rain':           'Thunderstorms',
    'lightning':                   'Thunder',
    'blowing snow':                'Windy/Snow',
    'rime':                        'Frigid',
    'Rainy':                       u'비',
    'Snow/Rain':                   u'눈 또는 비',
    'Snow':                        u'눈',
    'Little Cloudy':               u'구름조금',
    'Mostly Cloudy':               u'구름많음',
    'Clear':                       u'맑음'
}



def getFeelsLike( T=10, V=25 ):
    """ The formula to calculate the equivalent temperature related to the wind chill is:
        T(REF) = 13.12 + 0.6215 * T - 11.37 * V**0.16 + 0.3965 * T * V**0.16
        Or:
        T(REF): is the equivalent temperature in degrees Celsius
        V: is the wind speed in km/h measured at 10m height
        T: is the temperature of the air in degrees Celsius
        source: view-source:http://www.kma.go.kr/HELP/basic/help_01_07.jsp
    """
    T = float(T)
    V = float(V)
    FeelsLike = T
    V = V * 3.6 #(m/s to km/h) 
    #Wind speeds of 4 mph or less, the wind chill temperature is the same as the actual air temperature.
    if V > 4.8:
        FeelsLike = ( 13.12 + ( 0.6215 * T ) - ( 11.37 * V**0.16 ) + ( 0.3965 * T * V**0.16 ) )
        if FeelsLike > T:
            FeelsLike = T
    #
    return str( int(round( FeelsLike )) )


def getDewPoint( Tc=0, RH=93, minRH=( 0, 0.075 )[ 0 ] ):
    """ Dewpoint from relative humidity and temperature
        If you know the relative humidity and the air temperature,
        and want to calculate the dewpoint, the formulas are as follows.
    """
    Tc = float(Tc)
    RH = float(RH)
    #First, if your air temperature is in degrees Fahrenheit, then you must convert it to degrees Celsius by using the Fahrenheit to Celsius formula.
    # Tc = 5.0 / 9.0 * ( Tf - 32.0 )
    #The next step is to obtain the saturation vapor pressure(Es) using this formula as before when air temperature is known.
    Es = 6.11 * 10.0**( 7.5 * Tc / ( 237.7 + Tc ) )
    #The next step is to use the saturation vapor pressure and the relative humidity to compute the actual vapor pressure(E) of the air. This can be done with the following formula.
    #RH=relative humidity of air expressed as a percent. or except minimum(.075) humidity to abort error with math.log.
    RH = RH or minRH #0.075
    E = ( RH * Es ) / 100
    #Note: math.log( ) means to take the natural log of the variable in the parentheses
    #Now you are ready to use the following formula to obtain the dewpoint temperature.
    try:
        DewPoint = ( -430.22 + 237.7 * math.log( E ) ) / ( -math.log( E ) + 19.08 )
    except ValueError:
        #math domain error, because RH = 0%
        #return "N/A"
        DewPoint = 0 #minRH
    #Note: Due to the rounding of decimal places, your answer may be slightly different from the above answer, but it should be within two degrees.
    return str( int( DewPoint ) )
