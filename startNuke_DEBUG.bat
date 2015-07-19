@echo off
 rem Nuke

 rem --- Path ---
set "PROJECT_ROOT=//bigfoot/breakingpoint"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline/_sandbox"
set "PLUGINS_PATH=%PIPELINE_PATH%/nuke"
set "NUKE_VERSION=Nuke9.0v6"


 rem --- Plugins ---
set "NUKE_PATH=%PLUGINS_PATH%;%NUKE_PATH%"
set "NUKE_PATH=%PLUGINS_PATH%/plugins;%NUKE_PATH%"


set "NUKE_INIT_PATH=%PLUGINS_PATH%;%NUKE_PATH%"
set "NUKE_MENU_PATH=%PLUGINS_PATH%;%NUKE_PATH%"


 rem --- Call Nuke ---
set "NUKE_DIR=C:/Program Files/%NUKE_VERSION%"
set "PATH=%NUKE_DIR%;%PATH%"
start Nuke9.0.exe --nukex %1

