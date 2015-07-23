# $Id: dialog.py 1334 2015-06-03 13:22:23Z kik $
# -*- coding: utf-8 -*-

import htoa
import htoa.build
from arnold import AiGetVersionString
import hou
import os

def about():
    '''Display the "About" dialog'''
    
    help_text = ('HtoA %s\n'
                 'Arnold %s\n'
                 '\n'
                 '© 2001-2009 Marcos Fajardo\n'
                 '© 2009-2015 Solid Angle SL\n'
                 '\n'
                 'Developed by:\n'
                 'Frédéric Servant, Ivan DeWolf, Stefano Jannuzzo.\n'
                 '\n'
                 'Acknowledgements:\n'
                 'Fabian Gohde, Borja Morales, Michael Strathearn,\n'
                 'Gaétan Guidet, Brecht Van Lommel.\n'
                 % (htoa.__version__, AiGetVersionString()))
    
    f = open(os.path.join(htoa.folder, 'docs', 'legal', 'copyright.txt'), 'r')
    details_text = f.read()
    f.close()
    
    hou.ui.displayMessage('Arnold for Houdini', title='About HtoA', help=help_text, details=details_text)
    
def eula():
    '''Display the EULA dialog'''
    
    f = open(os.path.join(htoa.folder, 'docs', 'legal', 'eula.txt'), 'r')
    details_text = f.read()
    f.close()
    
    hou.ui.displayMessage('End User License Agreement', title='HtoA Legal Notice', details_expanded=True, details=details_text)

def diagnostics():
    '''Run some diagnostics'''
    
    severity_type = hou.severityType.Message
    
    # check for Houdini version mismatch
    if hou.applicationVersionString() != htoa.build.houdini_version:
        houdini_status = 'ERROR: should be %s' % htoa.build.houdini_version
        severity_type = hou.severityType.Error
    else:
        houdini_status = 'OK'
        
    # check for Arnold version mismatch
    if AiGetVersionString() != htoa.build.arnold_version:
        arnold_status = 'ERROR: should be %s' % htoa.build.arnold_version
        severity_type = hou.severityType.Error
    else:
        arnold_status = 'OK'
    
    diag_text = ('Houdini version: %s (%s)\n'
                 'Arnold version: %s (%s)' %
                 (hou.applicationVersionString(), houdini_status,
                  AiGetVersionString(), arnold_status))

    hou.ui.displayMessage('Diagnostics', title='HtoA Diagnostics', severity=severity_type, help=diag_text)
    