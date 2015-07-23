'''
@file
@since: 2011-11-19
@author: Frederic Servant <frederic.servant@gmail.com>
@namespace: htoa.log
'''
import sys
from arnold.ai_msg import AiMsgDebug, AiMsgError, AiMsgWarning, AiMsgInfo, AiMsgFatal

'''Logging utility functions.
    
Please use these log functions in HtoA over the AiMsgX() raw functions provided
by Arnold as it helps getting a consistent look of the log in all modules.

@section using_log Using the log functions
    
The recommended way of using these log functions is to import htoa.log as log:
    
@code
import htoa.log as log
@endcode
    
You can then log messages for each log level with these simple functions:
    
@code
log.debug('This is a debug message')
log.info('This is an info message')
log.warning('This is a warning message')
log.error('This is an error message')
log.fatal('This is a fatal message, application will now exit')
@endcode
    
Besides being simpler to use and type than their AiMsgXXX() Arnold
counterparts, another benefit is that the calling class will automatically be
written in the log between square brackets, easing the debug:

@code
00:00:03  751mb         | [htoa.object.geometry] Generating /obj/grid/grid1
00:00:03  751mb         | [htoa.node.polymesh] Generating mesh: /obj/grid:<empty>:polygons_0
@endcode

@section trace_mode Trace mode

Also available are a set of @e trace methods, prefixed with the first letter of
the log level (eg. 'e' for "error"):

@code
log.dtrace('This is a trace debug message')
log.itrace('This is a trace info message')
log.wtrace('This is a trace warning message')
log.etrace('This is a trace error message')
log.ftrace('This is a trace fatal message, application will now exit')
@endcode

These methods will be inactive unless htoa.log.enable_trace is set to True. 
<tt>[TRACE]</tt> is then added to the log line:

@code
00:00:03  758mb         | [htoa.node.node] [TRACE]  Parameter "subdiv_adaptive_metric" is set
00:00:03  758mb         | [htoa.node.node] [TRACE]  Parameter "subdiv_uv_smoothing" is set
00:00:03  758mb WARNING | [htoa.node.node] [TRACE]  Parameter "disp_map" is blacklisted
00:00:03  758mb WARNING | [htoa.node.node] [TRACE]  Parameter "disp_padding" is blacklisted
@endcode

The trace methods are intended for obsessive logging of everything, like
monitoring the transaltion of parameters. In everyday use, printing every
parameter value passed produces unreadable logs hence trace mode is turned off
by default.
'''

## Logging functions dict
_logfunc = {'debug': AiMsgDebug,
            'info': AiMsgInfo,
            'warning': AiMsgWarning,
            'error': AiMsgError,
            'fatal': AiMsgFatal}

## Enable trace flag
enable_trace = False

def _logMessage(level, message):
    '''Log a generic message.'''
    logmsg = '[%s] %s' % (sys._getframe(2).f_globals['__name__'], message)
    _logfunc[level](logmsg)
    
def _traceMessage(level, message):
    '''Log a generic trace message.'''
    logmsg = '[%s] [TRACE] %s' % (sys._getframe(2).f_globals['__name__'], message)
    _logfunc[level](logmsg)
    
def debug(message):
    '''Log a debug message.'''
    _logMessage('debug', message)
    
def info(message):
    '''Log an info message.'''
    _logMessage('info', message)

def warning(message):
    '''Log a warning message.'''
    _logMessage('warning', message)

def error(message):
    '''Log an error message.'''
    _logMessage('error', message)

def fatal(message):
    '''Log a fatal message and terminate.'''
    _logMessage('fatal', message)
    
def dtrace(message):
    '''Log a debug trace message.'''
    global enable_trace
    if enable_trace:
        _traceMessage('debug', message)

def itrace(message):
    '''Log an info trace message.'''
    global enable_trace
    if enable_trace:
        _traceMessage('info', message)

def wtrace(message):
    '''Log a warning trace message.'''
    global enable_trace
    if enable_trace:
        _traceMessage('warning', message)

def etrace(message):
    '''Log an error trace message.'''
    global enable_trace
    if enable_trace:
        _traceMessage('error', message)

def ftrace(message):
    '''Log a fatal trace message and terminate.'''
    global enable_trace
    if enable_trace:
        _traceMessage('fatal', message)
