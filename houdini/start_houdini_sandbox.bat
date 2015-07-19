@echo off
 rem HOUDINI

 rem ROOTS
set "PROJECT_ROOT=//bigfoot/breakingpoint"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline"
set "PLUGINS_PATH=%PIPELINE_PATH%/houdini/plugins"
set "HOUDINI_VERSION=Houdini 14.0.361"

 rem Royal Render
set "RR_ROOT=//smaug/Renderfarm/_RR6"

 rem Houdini Variables
set "PATH=%PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361/scripts/bin"
set "HOUDINI_PATH=%PIPELINE_PATH%/_sandbox/houdini/setup;%PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361;&"
set "HOUDINI_OTLSCAN_PATH=%PLUGINS_PATH%/qLib-dev/otls;%PIPELINE_PATH%/houdini/otl/publish;&"
set "JOB=%PIPELINE_PATH%/_sandbox/houdini"
set "HOUDINI_BUFFEREDSAVE=1"
 rem set "HOUDINI_USER_PREF_DIR=%PIPELINE_PATH%/_sandbox/houdini/setup/pref__HVER__"

 rem Arnold Variables
set "HOUDINI_DSO_ERROR=2" 
set "HTOA_STARTUP_LOG=0"

 rem SplashScreen
set "HOUDINI_SPLASH_FILE=%PIPELINE_PATH%/img/logo/houdinisplash_sandbox.png"
set "HOUDINI_SPLASH_MESSAGE=BP SANDBOX HOUDINI"

 rem Call Houdini
set "HOUDINI=C:/Program Files/Side Effects Software/%HOUDINI_VERSION%/bin"
set "PATH=%PATH%;%HOUDINI%"
houdinifx %PYSETUP%

exit