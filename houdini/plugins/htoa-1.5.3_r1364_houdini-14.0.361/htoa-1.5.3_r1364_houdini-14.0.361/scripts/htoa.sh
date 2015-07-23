#!/bin/bash
#
# Sample bash script to launch Houdini with HtoA enabled
#

# edit these to suit your environment
HOUDINI_ROOT="/opt/hfs12.1.185"
HTOA="/path/to/htoa/folder"

# source houdini environment
cd ${HOUDINI_ROOT}
source houdini_setup
cd - &> /dev/null

# set HOUDINI_PATH
export HOUDINI_PATH="${HOME}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE};${HTOA};${HFS}/houdini"

# launch houdini
houdini $@
