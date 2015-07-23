# $Id: license.py 1322 2015-05-29 11:20:53Z kik $

from arnold import *

## License information, see AtLicenseInfo
info = POINTER(AtLicenseInfo)()

## Number of licenses found
count = c_uint(0)

## License status, see ai_license.py
status = AiLicenseGetInfo(info, count)

## Flag to skip licensing entirely and avoid license checking timeout
skip = status not in (AI_LIC_SUCCESS, AI_LIC_ERROR_NOTAVAILABLE)
