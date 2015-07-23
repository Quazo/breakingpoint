# development utilities

import hou

def setRopTestSettings():
    rop = hou.selectedNodes()[0]
    rop.parm('ar_picture').set('$HIP/testrender.tif')
    rop.parm('ar_picture_format').set('tiff')
    rop.parm('ar_output_driver_gamma').set(2.2)
    rop.parm('ar_progressive').set(False)
    rop.parm('ar_skip_license_check').set(False)
    rop.parm('ar_bucket_size').set(32)
    rop.parm('ar_texture_searchpath').set('$HIP/../../common;$HIP/../common')
    rop.parm('ar_log_verbosity').set('debug')
    