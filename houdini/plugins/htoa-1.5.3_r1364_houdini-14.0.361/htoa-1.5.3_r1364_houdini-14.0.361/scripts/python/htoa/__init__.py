# $Id: __init__.py 1364 2015-06-16 16:45:37Z kik $

'''
@file
@namespace: htoa

The Houdini to Arnold module.

Because this module must be accessible from the normal (non-render) houdini
context, such as the OnDeleted event script of the Arnold ROP, no dependency
on the soho and sohog modules is allowed here.

'''
import os

## HtoA version
__version__ = '1.5.3'

## The global sessions dict keyed by uuid.
# 
# The persistance of the sessions relies on the HaSession instances
# being referenced in this dict, so that if you need to delete a session, you
# just delete its entry in the dict. Be careful when keeping references to 
# HaSession instance outside of the SOHO context.
#
# @note This dict is stored here and not as a static member of HaSession on
# purpose: it must be accessible outside of the SOHO context.
sessions = {}

## The HtoA installation location
folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

## FIXME: global flag to check if this is potentialy the first render on the render region
render_region_might_skip_generate = True

## FIXME: global flag to check if this is the first render on the render region
# has been skipped already, in case
render_region_force_generate = False

## The prefix to shader names used to namespace the shaders shipping with HtoA
shader_prefix = 'htoa__'

## The prefix to use for some DSOs such as procedurals
dso_prefix = 'htoa_'
