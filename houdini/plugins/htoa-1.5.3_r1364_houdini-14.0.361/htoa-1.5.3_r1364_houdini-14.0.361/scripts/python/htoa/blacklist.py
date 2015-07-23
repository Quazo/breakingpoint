# $Id: blacklist.py 1091 2014-11-14 16:37:30Z kik $

## attribute blacklist
attribute_blacklist = ['P', 'Pw', 'N', 'uv', 'varmap', 'shop_materialpath', 'creaseweight' ]

def attributeBlacklistCppDefine():
    return '{%s}' % ', '.join([r'\"%s\"' % attr for attr in attribute_blacklist])
