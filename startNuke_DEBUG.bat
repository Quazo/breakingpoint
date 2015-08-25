@echo off
 rem NUKE

 rem --- Path ---
set "PROJECT_ROOT=//bigfoot/breakingpoint"
set "PROJECT_ROOT=P:"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline"
set "SOFTWARE_PATH=%PIPELINE_PATH%/_sandbox/nuke"
set "PLUGINS_PATH=%SOFTWARE_PATH%/plugins"

set "NUKE_VERSION=Nuke9.0v6"


 rem --- Settings & Lib ---
set "NUKE_PATH=%SOFTWARE_PATH%;%NUKE_PATH%"
set "NUKE_PATH=%PIPELINE_PATH%;%NUKE_PATH%"
 

 rem --- Init & Menu ---
set "NUKE_INIT_PATH=%SOFTWARE_PATH%;%NUKE_INIT_PATH%"
set "NUKE_MENU_PATH=%SOFTWARE_PATH%;%NUKE_MENU_PATH%"


 rem --- Plugins ---
set "NUKE_PATH=%PLUGINS_PATH%/plugins;%NUKE_PATH%"


 rem --- Call Nuke ---
set "NUKE_DIR=C:/Program Files/%NUKE_VERSION%"
set "PATH=%NUKE_DIR%;%PATH%"
start Nuke9.0.exe --nukex %1

