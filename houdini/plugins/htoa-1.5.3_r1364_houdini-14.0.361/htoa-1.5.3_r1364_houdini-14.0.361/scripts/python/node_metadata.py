from arnold import *

AiBegin()
AiMsgSetConsoleFlags(AI_LOG_ALL)

nentry_iter = AiUniverseGetNodeEntryIterator(AI_NODE_LIGHT)
while not AiNodeEntryIteratorFinished(nentry_iter):
    nentry = AiNodeEntryIteratorGetNext(nentry_iter)
    
    print
    print "##############################################################################"
    print "[node %s]" % AiNodeEntryGetName(nentry)
    print
    
    pentry_iter = AiNodeEntryGetParamIterator(nentry)
    while not AiParamIteratorFinished(pentry_iter):
        pentry = AiParamIteratorGetNext(pentry_iter)
        print "[attr %s]" % AiParamGetName(pentry)
        print
        
AiNodeEntryIteratorDestroy(nentry_iter)

