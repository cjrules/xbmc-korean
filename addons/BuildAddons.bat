@Echo off
setLocal EnableDelayedExpansion

:: Change the relative path to the addon repository
SET ADDONREPO_PATH=..\..\..\xbmc-korea-addons\addons\dharma

:: List Addons (Directories)
ECHO ------------------------------------------------------------
ECHO Select addon to package
for /f "tokens=* delims= " %%a in ('dir /B /AD-H') do (
set /a N+=1
echo [!N!] %%a
)
ECHO ------------------------------------------------------------
  set /P ADDON_ANSWER=Which ADDON? [1-16]:

set counter=0
for /F "delims=" %%j in ('dir /B /AD-H') do (
  set /A counter+=1
  if !counter! equ %ADDON_ANSWER% (SET AddonName=%%j & goto :CONTINUE)
)
:CONTINUE
set AddonName=%AddonName: =%
echo %AddonName% is packaging...

:: Create Build folder
IF EXIST BUILD_TEMP rmdir BUILD_TEMP /S /Q 
md BUILD_TEMP

:: Create exclude file
Echo .svn>"BUILD_TEMP\exclude.txt"
Echo Thumbs.db>>"BUILD_TEMP\exclude.txt"

xml sel -t -v "/addon/@version" %AddonName%\addon.xml > BUILD_TEMP\rev.txt
set /p rev= <BUILD_TEMP\rev.txt

7z a BUILD_TEMP\%AddonName%-%rev%.zip .\%AddonName%\ -xr@BUILD_TEMP\exclude.txt
copy %AddonName%\changelog.txt BUILD_TEMP\changelog-%rev%.txt
copy %AddonName%\icon.png BUILD_TEMP\icon.png

del /q BUILD_TEMP\rev.txt BUILD_TEMP\exclude.txt %ADDONREPO_PATH%\%AddonName%\*.*
xcopy BUILD_TEMP "%ADDONREPO_PATH%\%AddonName%" /E /Q /I /Y

xml ed -u "/addons/addon[@id='%AddonName%']/@version" -v %rev% "%ADDONREPO_PATH%\addons.xml" > BUILD_TEMP\temp.xml
move /Y BUILD_TEMP\temp.xml %ADDONREPO_PATH%\addons.xml
md5 -n %ADDONREPO_PATH%\addons.xml > %ADDONREPO_PATH%\addons.xml.md5
rmdir /s /q BUILD_TEMP

Echo Build Complete - Scroll Up to check for errors.
pause