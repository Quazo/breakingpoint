# Imports

import os
import sys

import hou


HIP = hou.expandString('$HIP')
HIPFILE = hou.expandString('$HIPFILE')
FULL_SHOT_NAME = hou.expandString('$BP_SHOT_NAME')
SHOT_NUMBER = FULL_SHOT_NAME.split('_')[0]
SHOT_NAME = FULL_SHOT_NAME[len(SHOT_NUMBER)+1:]
RR_ROOT = os.environ['RR_ROOT']

RR_SUBMITTERCONSOLE_PATH = RR_ROOT + '/win__rrSubmitter.bat'
ASS_FILE = ''

FLAGS = ''
SUBMITTER_OPTIONS = '\"' + 'CustomSCeneName=1~' + SHOT_NUMBER +  '\" ' + '\"' + 'CustomSHotName=1~' + SHOT_NAME + '\" ' + '\"' + 'PreviewGamma2.2=0~1' + '\" '

def get_node_info():


	info = []
	#rop_list = hou.node('/out').allSubChildren()
	rop_list = hou.selectedNodes()
	if(len(rop_list)==0):
		return None

	arnold_rop_list = []
	
	for rop in rop_list:
		if(rop.type().name()=='arnold'):
			arnold_rop_list.append(rop)

	'''
	for arnold_rop in arnold_rop_list:
		#arnold_rop.parm('execute').pressButton()
		ASS_FILE = hou.expandString(arnold_rop.evalParm('ar_ass_file'))
		print "ASSFILE:" + arnold_rop.evalParm('ar_ass_file')

	'''

	arnold_rop = arnold_rop_list[0]
	#arnold_rop.parm('execute').pressButton()
	info.append(hou.expandString(arnold_rop.parm('ar_ass_file').unexpandedString().replace('$F4', '####')))
	info.append(arnold_rop.path())

	return info


def bp_submit():

	info = get_node_info()
	ass_file = ''
	layer = ''
	if(info==None):
		return
	else:
		ass_file = info[0]
		layer = info[1]


	# Create Ass Files
	ass_file_name = os.path.basename(ass_file)
	ass_directory = os.path.dirname(ass_file)

	flags = FLAGS + '-R createASS ' + '-L ' + layer + ' ' + '-ID ' + ass_directory + ' ' + '-IF ' + ass_file_name + ' -IE .ass'
	submitter_options = SUBMITTER_OPTIONS

	command_line_a = RR_SUBMITTERCONSOLE_PATH + ' ' + HIPFILE + ' ' + flags + ' ' + submitter_options
	#os.system(command_line)

	# Kick Ass
	flags = FLAGS + '-L ' + layer
	submitter_options = SUBMITTER_OPTIONS

	command_line_b = RR_SUBMITTERCONSOLE_PATH + ' ' + ass_file + ' ' + flags + ' ' + submitter_options
	os.system(command_line_a + '\n' + command_line_b)


bp_submit()