#*************************************************************
# title:        combine SHD & MODEL
#
# content:      set all shader on every object which has the shader name in its name
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
#               shader name must be unique not part of another shader
#               object must have the shader name inside (-1 character)
#               shading group must have the save name as shader (+SG)
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************


import maya.cmds as cmds
import maya.mel as mel

import uniteShaderGroup

def start(meshTypes = ["mesh"], shaderTypes = ["alSurface", "alLayer"]):
    shaderList = []
    objList = []
    
    try:
        uniteShaderGroup.start()
    except:
        print ("** FAIL | Unite Shader and Shader Group : Failed to load **")

    for shaderType in shaderTypes:
        shaderList += cmds.ls(type = shaderType)
   
    for meshType in meshTypes:
        objList += cmds.ls( type= meshType)

    for shader in shaderList:
        tmpShader = shader
        
        if(tmpShader.find("SHD")):
            tmpShader = tmpShader.replace("SHD", "MODEL") 
          
        for obj in objList:

            if(obj.find("RIG")):
                tmpShader = tmpShader.replace("SHD", "RIG")

            tmpObj = obj

            if(obj.startswith("_ANIM")):
                tmpObj = cmds.getAttr(tmpObj + '.name')
                
            if (tmpObj.find(tmpShader[:-1]) != -1):   

                mel.eval('select -r ' + obj + ';')
                mel.eval('sets -e -forceElement ' + shader + 'SG;')
                
                objList[objList.index(obj)] = ""

    print ("** DONE | Combine SHD & MODEL **")