#*************************************************************
# title:        combine SHD & MODEL
#
# content:      automaticly saves work and publish files
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%/maya;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

# shader name must be unique not part of another
# object must have the shader name inside (-1 character)
# shading group must have the save name as shader (+SG)


import maya.cmds as cmds
import maya.mel as mel

import uniteShaderGroup

def start():

    uniteShaderGroup.start()

    shaderList = cmds.ls(type = 'alSurface')
    #print shaderList

    objList = cmds.ls( type="mesh")
    #print objList

    for shader in shaderList:
    	
        tmpShader = shader
        
        if (tmpShader.find("SHD")):
            #print "SHD" + tmpShader
            tmpShader = tmpShader.replace("SHD", "MODEL") 
          
        for obj in objList:

            tmpObj = obj

            if(obj.startswith("_ANIM")):
                tmpObj = cmds.getAttr(tmpObj + '.name')
                
            if (tmpObj.find(tmpShader[:-1]) != -1):   

                #print "Set SHD"
                #print obj
                #print shader
                #print ""
                mel.eval('select -r ' + obj + ';')
                mel.eval('sets -e -forceElement ' + shader + 'SG;')
                
                objList[objList.index(obj)] = ""

    print ("** DONE: Combine SHD & MODEL **")