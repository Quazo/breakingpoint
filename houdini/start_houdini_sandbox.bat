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
set "PATH=%PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361/scripts/bin;%PATH%"
set "HOUDINI_PATH=%PIPELINE_PATH%/_sandbox/houdini/setup;%PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361;&"
 rem set "HOUDINI_SCRIPT_PATH=%PIPELINE_PATH%/_sandbox/houdini/setup/scripts"
set "HOUDINI_OTLSCAN_PATH=%PLUGINS_PATH%/qLib-dev/otls/base;%PLUGINS_PATH%/qLib-dev/otls/experimental;%PLUGINS_PATH%/qLib-dev/otls/base/future;%PIPELINE_PATH%/houdini/otl/publish;&"
 rem set "JOB=%PIPELINE_PATH%/_sandbox/houdini"
set "HOUDINI_BUFFEREDSAVE=1"
set "HOUDINI_USER_PREF_DIR=%PIPELINE_PATH%/_sandbox/houdini/setup/pref__HVER__"
set "HOUDINI_TEMP_DIR=%PIPELINE_PATH%/houdini/temp_dir"

 rem Arnold Variables
set "HOUDINI_DSO_ERROR=2" 
set "HTOA_STARTUP_LOG=0"

 rem SplashScreen
set "HOUDINI_SPLASH_FILE=%PIPELINE_PATH%/img/logo/houdinisplash_sandbox.png"
set "HOUDINI_SPLASH_MESSAGE=BP SANDBOX - %HOUDINI_VERSION%"

 rem Call Houdini
set "HOUDINI=C:/Program Files/Side Effects Software/%HOUDINI_VERSION%/bin"
set "PATH=%PATH%;%HOUDINI%"
houdinifx %PYSETUP%

exit