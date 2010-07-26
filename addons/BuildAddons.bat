@Echo off

rem ----Usage----
rem BuildAddons [Addon Name]

SET AddonName="%1"
SET AddonName=plugin.video.dabdate.com

ECHO ------------------------------------------------------------
ECHO Select addon to package
ECHO [1] metadata.albums.daum.net
ECHO [2] metadata.albums.naver.com
ECHO [3] metadata.artists.daum.net
ECHO [4] metadata.artists.naver.com
ECHO [5] metadata.common.movie.daum.net
ECHO [6] metadata.movie.daum.net
ECHO [7] metadata.movie.naver.com
ECHO [8] metadata.tv.daum.net
ECHO [9] plugin.video.dabdate.com
ECHO [10] plugin.video.daum.net
ECHO [11] plugin.video.gomtv.com
ECHO [12] plugin.video.joonmedia.net
ECHO [13] repository.xbmc-korea.com
ECHO [14] script.xbmc-korea.lyrics
ECHO [15] script.xbmc-korea.subtitles
ECHO ------------------------------------------------------------
  set /P ADDON_ANSWER=Which ADDON? [1-15]:
  if /I %ADDON_ANSWER% EQU 1 SET AddonName=metadata.albums.daum.net
  if /I %ADDON_ANSWER% EQU 2 SET AddonName=metadata.albums.naver.com
  if /I %ADDON_ANSWER% EQU 3 SET AddonName=metadata.artists.daum.net
  if /I %ADDON_ANSWER% EQU 4 SET AddonName=metadata.artists.naver.com
  if /I %ADDON_ANSWER% EQU 5 SET AddonName=metadata.common.movie.daum.net
  if /I %ADDON_ANSWER% EQU 6 SET AddonName=metadata.movie.daum.net
  if /I %ADDON_ANSWER% EQU 7 SET AddonName=metadata.movie.naver.com
  if /I %ADDON_ANSWER% EQU 8 SET AddonName=metadata.tv.daum.net
  if /I %ADDON_ANSWER% EQU 9 SET AddonName=plugin.video.dabdate.com
  if /I %ADDON_ANSWER% EQU 10 SET AddonName=plugin.video.daum.net
  if /I %ADDON_ANSWER% EQU 11 SET AddonName=plugin.video.gomtv.com
  if /I %ADDON_ANSWER% EQU 12 SET AddonName=plugin.video.joonmedia.net
  if /I %ADDON_ANSWER% EQU 13 SET AddonName=repository.xbmc-korea.com
  if /I %ADDON_ANSWER% EQU 14 SET AddonName=script.xbmc-korea.lyrics
  if /I %ADDON_ANSWER% EQU 15 SET AddonName=script.xbmc-korea.subtitles

:: Create Build folder
Echo ------------------------------
Echo Creating %AddonName% Build Folder . . .
IF EXIST BUILD_TEMP rmdir BUILD_TEMP /S /Q
md BUILD_TEMP
Echo.

:: Create exclude file
Echo ------------------------------
Echo Creating exclude.txt file . . .
Echo.
Echo .svn>"BUILD_TEMP\exclude.txt"
Echo Thumbs.db>>"BUILD_TEMP\exclude.txt"
Echo Desktop.ini>>"BUILD_TEMP\exclude.txt"
Echo.

Echo ------------------------------
Echo Copying required files to \BUILD_TEMP\%AddonName%%\ folder . . .
xcopy %AddonName% "BUILD_TEMP\%AddonName%\" /E /Q /I /Y /EXCLUDE:BUILD_TEMP\exclude.txt
Echo.

IF EXIST BUILD_TEMP\exclude.txt del BUILD_TEMP\exclude.txt  > NUL

Echo Build Complete - Scroll Up to check for errors.
Echo Final build is located in the BUILD folder.
Echo copy: \%AddonName%\ folder in the \BUILD\ folder.

xml.exe sel -t -v "/addon/@version" BUILD_TEMP\%AddonName%\addon.xml > rev.txt
set /p rev= <rev.txt
del rev.txt

7z.exe a BUILD_TEMP\%AddonName%-%rev%.zip .\BUILD_TEMP\%AddonName%\
copy BUILD_TEMP\%AddonName%\changelog.txt BUILD_TEMP\changelog-%rev%.txt
copy BUILD_TEMP\%AddonName%\icon.png BUILD_TEMP\icon.png

rmdir /s /q BUILD_TEMP\%AddonName%

del /q ..\..\..\xbmc-korea-addons\addons\dharma\%AddonName%\*.*
xcopy BUILD_TEMP "..\..\..\xbmc-korea-addons\addons\dharma\%AddonName%" /E /Q /I /Y
rmdir /s /q BUILD_TEMP

xml.exe ed -u "/addons/addon[@id='%AddonName%']/@version" -v %rev% "..\..\..\xbmc-korea-addons\addons\dharma\addons.xml" >> temp.xml
mv -f temp.xml D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml
del D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml.md5
md5 -n D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml > D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml.md5