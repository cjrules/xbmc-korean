@Echo off
setLocal EnableDelayedExpansion

:: List Addons (Directories)

dir /B /AD-H > list.txt

ECHO ------------------------------------------------------------
ECHO Select addon to package
for /f "tokens=* delims= " %%a in (list.txt) do (
set /a N+=1
set v!N!=%%a
echo [!N!] %%a
)
ECHO ------------------------------------------------------------
  set /P ADDON_ANSWER=Which ADDON? [1-15]:

set counter=0
for /F "delims=" %%j in (list.txt) do (
  set /A counter+=1
  if !counter! equ %ADDON_ANSWER% (SET AddonName=%%j & goto :CONTINUE)
)
:CONTINUE
set AddonName=%AddonName: =%
echo %AddonName% is packaging...
del /q list.txt

:: Create Build folder
Echo ------------------------------
Echo Creating %AddonName% Build Folder . . .
md BUILD_TEMP
Echo.

:: Create exclude file
Echo ------------------------------
Echo Creating exclude.txt file . . .
Echo.
Echo .svn>"BUILD_TEMP\exclude.txt"
Echo Thumbs.db>>"BUILD_TEMP\exclude.txt"
Echo.

xml sel -t -v "/addon/@version" %AddonName%\addon.xml > BUILD_TEMP\rev.txt
set /p rev= <BUILD_TEMP\rev.txt

7z a BUILD_TEMP\%AddonName%-%rev%.zip .\%AddonName%\ -xr@BUILD_TEMP\exclude.txt
copy %AddonName%\changelog.txt BUILD_TEMP\changelog-%rev%.txt
copy %AddonName%\icon.png BUILD_TEMP\icon.png

:: Change the relative path to the addon repository

del /q ..\..\..\xbmc-korea-addons\addons\dharma\%AddonName%\*.*
xcopy BUILD_TEMP "..\..\..\xbmc-korea-addons\addons\dharma\%AddonName%" /E /Q /I /Y
rmdir /s /q BUILD_TEMP

xml ed -u "/addons/addon[@id='%AddonName%']/@version" -v %rev% "..\..\..\xbmc-korea-addons\addons\dharma\addons.xml" > temp.xml
move /Y temp.xml ..\..\..\xbmc-korea-addons\addons\dharma\addons.xml
md5 -n ..\..\..\xbmc-korea-addons\addons\dharma\addons.xml > ..\..\..\xbmc-korea-addons\addons\dharma\addons.xml.md5

Echo Build Complete - Scroll Up to check for errors.
pause