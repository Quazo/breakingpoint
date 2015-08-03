@echo off
 rem MAYA

 rem --- Path ---
set "PROJECT_ROOT=//bigfoot/breakingpoint"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline"
set "SOFTWARE_PATH=%PIPELINE_PATH%/_sandbox"

set "SCRIPT_PATH=%SOFTWARE_PATH%/maya/scripts"
set "PLUGINS_PATH=%SOFTWARE_PATH%/maya/plugins"
set "ARNOLD_PATH=%PLUGINS_PATH%/arnold"
set "ARNOLD_SHADER_PATH=%ARNOLD_PATH%/alShader"

set "MAYA_VERSION=2015"


 rem --- Plugins ---
set "PYTHONPATH=%SOFTWARE_PATH%/maya;%PYTHONPATH%"


 rem ---arUtils ---
 rem set "MAYA_MODULE_PATH=%PLUGINS_PATH%/arUtils;%MAYA_MODULE_PATH%"
 rem set "PYTHONPATH=%PLUGINS_PATH%/arUtils;%PYTHONPATH%"


set "PYTHONPATH=%SCRIPT_PATH%/ArnoldDNA_03;%PYTHONPATH%"
set "XBMLANGPATH=%SCRIPT_PATH%/ArnoldDNA_03/icons;XBMLANGPATH"
set "MAYA_SHELF_PATH=%SOFTWARE_PATH%/maya/shelf;%MAYA_SHELF_PATH%"


 rem --- Arnold ---
set "MtoA=%ARNOLD_PATH%/%MAYA_VERSION%"
set "MAYA_MODULE_PATH=%MtoA%;%MAYA_MODULE_PATH%"
set "PATH=%MtoA%/bin;%PATH%"
set "ARNOLD_PLUGIN_PATH=%MtoA%/shaders;%ARNOLD_PLUGIN_PATH%;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_PLUGIN_PATH=%ARNOLD_PATH%/bin;%ARNOLD_PLUGIN_PATH%;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_PLUGIN_PATH=%ARNOLD_SHADER_PATH%/bin;%ARNOLD_PLUGIN_PATH%"
set "MTOA_TEMPLATES_PATH=%ARNOLD_SHADER_PATH%/ae;%MTOA_TEMPLATES_PATH%"

set "ARNOLD_LICENSE_HOST=blue"


set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"


 rem --- MayaEnvVars ---
 rem set "MAYA_PROJECT=%PROJECT_ROOT%/2_production"
 rem cd %MAYA_PROJECT%


 rem --- SplashScreen ---
 rem File: MayaEDUStartupImage.png
set "XBMLANGPATH=%PIPELINE_PATH%/img/logo;%XBMLANGPATH%"


 rem --- Call Maya ---
set "MAYA_DIR=C:/Program Files/Autodesk/Maya%MAYA_VERSION%"
set "PATH=%MAYA_DIR%/bin;%PATH%"
start maya

exit