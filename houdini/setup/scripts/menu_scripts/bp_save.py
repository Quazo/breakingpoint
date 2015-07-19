import sys
import hou

def save_increment():

	# Houdini Variables
	hip = hou.expandString('$HIP')
	hipname = hou.expandString('$HIPNAME')

	# Parse HIP File
	# version = hipname.split('_v')[1].split('_')[0]
	# version_incremented = "%03d" % (int(version)+1)

try:

	hou.hipFile.saveAndIncrementFileName()
	print(".hip saved under : {0}".format(hou.expandString('$HIPFILE')))

except:

	print("Save aborted!")

# ---------------------------------------------
arg = sys.argv[1]

if(arg=='increment'): save_increment()