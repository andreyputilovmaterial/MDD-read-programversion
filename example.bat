@ECHO OFF



SET "MDD_FNAME=.\p2401215.mdd"

SET "DELIVERY_PATH=P:\CC1302_Palm\CC1302-2401215 Hasbro - Magic The Gathering Brand Tracking - Fa~\4_Data\IPS Deliverables\MDD for LI"


REM :: this script is just an example for possible usage
REM :: it copies MDD to a folder for LI
REM :: and date and program version are becoming parts of path



SET "SCRIPT_PATH=.\_Other Versions\mdmtoolsap-mdd-ver.py"

FOR /F "delims=" %%i IN ('python "%SCRIPT_PATH%" "%MDD_FNAME%"') DO SET "DELIVERYNAME_PROGVER_PART=%%i"

REM set delivery folder name, automatically sets to MM-DD-YY
REM works automatically
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
SET "YY=%dt:~2,2%" & set "YYYY=20%dt:~2,2%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%" & set "HHMMSS=%dt:~8,6%"
SET "DELIVERYNAME_DATE_PART=%MM%.%DD%.%YYYY%"

SET "DELIVERY_PATH_FINAL=%DELIVERY_PATH%\%DELIVERYNAME_DATE_PART% v. %DELIVERYNAME_PROGVER_PART%"

IF NOT EXIST "%DELIVERY_PATH_FINAL%\" (
    MKDIR "%DELIVERY_PATH_FINAL%\"
)
COPY "%MDD_FNAME%" "%DELIVERY_PATH_FINAL%\"

ECHO copied to %DELIVERY_PATH_FINAL%
