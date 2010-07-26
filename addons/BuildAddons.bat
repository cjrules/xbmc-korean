@Echo off

rem ----Usage----
rem BuildAddons [Addon Name]

SET AddonName="%1"
SET AddonName=plugin.video.dabdate.com

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

xcopy BUILD_TEMP "..\..\..\xbmc-korea-addons\addons\dharma\%AddonName%" /E /Q /I /Y
rmdir /s /q BUILD_TEMP

xml.exe ed -u "/addons/addon[@id='%AddonName%']/@version" -v %rev% "..\..\..\xbmc-korea-addons\addons\dharma\addons.xml" >> temp.xml
mv -f temp.xml D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml
del D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml.md5
md5 -n D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml > D:\xbmc-korean\xbmc-korea-addons\addons\dharma\addons.xml.md5