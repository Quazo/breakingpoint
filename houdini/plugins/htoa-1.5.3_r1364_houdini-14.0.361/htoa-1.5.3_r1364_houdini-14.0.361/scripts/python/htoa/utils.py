# $Id: utils.py 1353 2015-06-11 15:58:22Z kik $

import os
import soho

def mkdirs(path):
    try:
        os.makedirs(path)
    except:
        if path == '':
            path = os.getcwd()
            
        if not os.access(path, os.R_OK):
            soho.error('Path "%s" is not readable' % path)
        elif not os.path.isdir(path):
            soho.error('Path "%s" is not a directory' % path)
        elif not os.access(path, os.W_OK):
            soho.error('Directory "%s" is not writable' % path)
