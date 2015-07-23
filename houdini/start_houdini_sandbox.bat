@echo off
 rem /* HOUDINI */

 rem /* ROOTS */
set "BP_PROJECT_ROOT=//bigfoot/breakingpoint"
set "BP_PIPELINE_PATH=%BP_PROJECT_ROOT%/_pipeline"
set "BP_HOUDINI_PIPELINE_PATH=%BP_PIPELINE_PATH%/_sandbox/houdini"
set "BP_HOUDINI_PLUGINS_PATH=%BP_PIPELINE_PATH%/software/houdini/plugins"
set "BP_HOUDINI_VERSION=Houdini 14.0.361"

 rem /* Royal Render */
set "RR_ROOT=//smaug/Renderfarm/_RR6"

 rem /* Houdini Variables */
set "PATH=%BP_HOUDINI_PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361/scripts/bin;%PATH%"
set "HOUDINI_PATH=%BP_HOUDINI_PIPELINE_PATH%/setup;%BP_HOUDINI_PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361;&"

 rem set "HOUDINI_SCRIPT_PATH=%PIPELINE_PATH%/_sandbox/houdini/setup/scripts"
set "HOUDINI_OTLSCAN_PATH=%BP_HOUDINI_PLUGINS_PATH%/qLib-dev/otls/base;%BP_HOUDINI_PLUGINS_PATH%/qLib-dev/otls/experimental;%BP_HOUDINI_PLUGINS_PATH%/qLib-dev/otls/base/future;%BP_PIPELINE_PATH%/software/houdini/otl/publish;&"
set "HOME=%BP_HOUDINI_PIPELINE_PATH%/setup"
set "HOUDINI_BUFFEREDSAVE=1"
set "HOUDINI_USER_PREF_DIR=%BP_HOUDINI_PIPELINE_PATH%/pref__HVER__"

set "BP_MENU_SCRIPTS_PATH=%BP_HOUDINI_PIPELINE_PATH%/setup/scripts/menu_scripts"


 rem /* Arnold Variables */
set "HOUDINI_DSO_ERROR=2"
set "HTOA_STARTUP_LOG=0"

 rem /* SplashScreen */
set "HOUDINI_SPLASH_FILE=%BP_PIPELINE_PATH%/img/logo/houdinisplash_sandbox.png"
set "HOUDINI_SPLASH_MESSAGE=Breaking Point Sandbox - %BP_HOUDINI_VERSION%"

 rem /* Call Houdini */
set "HOUDINI=C:/Program Files/Side Effects Software/%BP_HOUDINI_VERSION%/bin"
set "PATH=%PATH%;%HOUDINI%"
houdinifx %PYSETUP%

exit