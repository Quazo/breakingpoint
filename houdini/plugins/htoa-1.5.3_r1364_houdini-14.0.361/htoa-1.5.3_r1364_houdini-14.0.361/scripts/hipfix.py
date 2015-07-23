#!/usr/bin/env python
# $Id: hipfix.py 555 2013-11-01 17:30:47Z kik $

import os
import sys
import getopt
import glob

__doc__ = 'usage: hipfix [-h|--help] <htoa_version> <hipfile> [...]'

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
        
    # process options
    for o, a in opts:
        if o in ("-h", "--help") or not args:
            print __doc__
            sys.exit(0)

    if len(args) < 2:
        print __doc__
        sys.exit(2)
    
    # welcome
    htoa_version = args[0]
    print '[hipfix] converting pre-%s hip files' % htoa_version
    
    # make sure HFS is defined
    try:
        HFS = os.environ['HFS']
    except:
        print "[hipfix] error: define the HFS environment variable or source the Houdini environment"
        sys.exit(1)
        
    # gather node definitions
    types_to_update = {}
    fixconf = os.path.join(os.path.dirname(__file__), 'fixconf-%s' % (htoa_version))
    for folder, subfolders, files in os.walk(fixconf):
        for f in files:
            if f.endswith('.def'):
                node_type = os.path.splitext(f)[0]
                types_to_update[node_type] = {}
                with open(os.path.join(folder, f)) as fd:
                    is_reading_io = False
                    iodef = ''
                    for line in fd:
                        if line.startswith('connectornextid'):
                            nextid = int(line[15:].strip())
                            types_to_update[node_type]['nextid'] = nextid
                            
                        if line.startswith('outputsNamed3'):
                            is_reading_io = True
                        
                        if line.startswith('stat'):
                            types_to_update[node_type]['iodef'] = iodef
                            break
                            
                        if is_reading_io:
                            iodef = iodef + line 
    
    print '[hipfix] found %i node definitions to update' % len(types_to_update)

    # get rename definitions
    node_renames = {}
    try:
        exec(open(os.path.join(fixconf, 'rename.py')).read())
    except: pass
    print '[hipfix] found %i node renaming rules' % len(node_renames)

    # process hip files
    for hipfile in args[1:]:

        # expand the hip file
        print '[hipfix] expanding %s ...' % hipfile
        os.system(os.path.join(HFS, 'bin', 'hexpand') + ' ' + hipfile)
        
        # look for nodes to update
        for folder, subfolders, files in os.walk(hipfile + '.dir'):
            for f in files:
                if f.endswith(".init"):
                    file_path = os.path.join(folder, f)
                    
                    with open(file_path) as fd:
                        header = fd.readline()
                    
                    # rename node
                    node_name = header[7:].strip()
                    if node_name in node_renames:
                        print '[hipfix] renaming type %s to %s: /%s' % (node_name, node_renames[node_name], os.path.splitext(file_path)[0].split(os.path.sep, 1)[1])
                        
                        with open(file_path) as fd:
                            init = fd.read().replace(node_name, node_renames[node_name])
                        
                        with open(file_path, 'w') as fd:
                            fd.write(init)
                        
                    # update node inputs/outputs definitions
                    if header[:15] == 'type = arnold::':
                        node_type = header[15:].strip()
                        node_path = os.path.splitext(file_path)[0]
                        
                        if node_type in types_to_update:
                            print "[hipfix] updating definition [%s]: /%s" % (node_type, node_path.split(os.path.sep, 1)[1])
                            
                            os.rename(node_path + '.def', node_path + '.orig')
                            
                            with open(node_path + '.def', 'w') as fd:
                                with open(node_path + '.orig') as fd_old:
                                    is_reading_io = False
                                    
                                    for line in fd_old:
                                        if line.startswith('connectornextid'):
                                            fd.write('connectornextid %i\n' % types_to_update[node_type]['nextid'])
                                            continue
                                            
                                        if line.startswith('outputsNamed3'):
                                            is_reading_io = True
                                            fd.write(types_to_update[node_type]['iodef'])
                                            continue
                                        
                                        if line.startswith('stat'):
                                            is_reading_io = False
                                            
                                        if not is_reading_io:
                                            fd.write(line) 
        
        print '[hipfix] collapsing %s ...' % hipfile
        os.system(os.path.join(HFS, 'bin', 'hcollapse') + ' -r ' + hipfile)
        
    print '[hipfix] done.'

if __name__ == "__main__":
    main()
