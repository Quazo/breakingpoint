# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.5
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_htoa_pygeo', [dirname(__file__)])
        except ImportError:
            import _htoa_pygeo
            return _htoa_pygeo
        if fp is not None:
            try:
                _mod = imp.load_module('_htoa_pygeo', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _htoa_pygeo = swig_import_helper()
    del swig_import_helper
else:
    import _htoa_pygeo
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _htoa_pygeo.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self):
        return _htoa_pygeo.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _htoa_pygeo.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _htoa_pygeo.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _htoa_pygeo.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _htoa_pygeo.SwigPyIterator_equal(self, x)

    def copy(self):
        return _htoa_pygeo.SwigPyIterator_copy(self)

    def next(self):
        return _htoa_pygeo.SwigPyIterator_next(self)

    def __next__(self):
        return _htoa_pygeo.SwigPyIterator___next__(self)

    def previous(self):
        return _htoa_pygeo.SwigPyIterator_previous(self)

    def advance(self, n):
        return _htoa_pygeo.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _htoa_pygeo.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _htoa_pygeo.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _htoa_pygeo.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _htoa_pygeo.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _htoa_pygeo.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _htoa_pygeo.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _htoa_pygeo.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class vectorf(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorf, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorf, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _htoa_pygeo.vectorf_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _htoa_pygeo.vectorf___nonzero__(self)

    def __bool__(self):
        return _htoa_pygeo.vectorf___bool__(self)

    def __len__(self):
        return _htoa_pygeo.vectorf___len__(self)

    def pop(self):
        return _htoa_pygeo.vectorf_pop(self)

    def __getslice__(self, i, j):
        return _htoa_pygeo.vectorf___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _htoa_pygeo.vectorf___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _htoa_pygeo.vectorf___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _htoa_pygeo.vectorf___delitem__(self, *args)

    def __getitem__(self, *args):
        return _htoa_pygeo.vectorf___getitem__(self, *args)

    def __setitem__(self, *args):
        return _htoa_pygeo.vectorf___setitem__(self, *args)

    def append(self, x):
        return _htoa_pygeo.vectorf_append(self, x)

    def empty(self):
        return _htoa_pygeo.vectorf_empty(self)

    def size(self):
        return _htoa_pygeo.vectorf_size(self)

    def clear(self):
        return _htoa_pygeo.vectorf_clear(self)

    def swap(self, v):
        return _htoa_pygeo.vectorf_swap(self, v)

    def get_allocator(self):
        return _htoa_pygeo.vectorf_get_allocator(self)

    def begin(self):
        return _htoa_pygeo.vectorf_begin(self)

    def end(self):
        return _htoa_pygeo.vectorf_end(self)

    def rbegin(self):
        return _htoa_pygeo.vectorf_rbegin(self)

    def rend(self):
        return _htoa_pygeo.vectorf_rend(self)

    def pop_back(self):
        return _htoa_pygeo.vectorf_pop_back(self)

    def erase(self, *args):
        return _htoa_pygeo.vectorf_erase(self, *args)

    def __init__(self, *args):
        this = _htoa_pygeo.new_vectorf(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def push_back(self, x):
        return _htoa_pygeo.vectorf_push_back(self, x)

    def front(self):
        return _htoa_pygeo.vectorf_front(self)

    def back(self):
        return _htoa_pygeo.vectorf_back(self)

    def assign(self, n, x):
        return _htoa_pygeo.vectorf_assign(self, n, x)

    def resize(self, *args):
        return _htoa_pygeo.vectorf_resize(self, *args)

    def insert(self, *args):
        return _htoa_pygeo.vectorf_insert(self, *args)

    def reserve(self, n):
        return _htoa_pygeo.vectorf_reserve(self, n)

    def capacity(self):
        return _htoa_pygeo.vectorf_capacity(self)
    __swig_destroy__ = _htoa_pygeo.delete_vectorf
    __del__ = lambda self: None
vectorf_swigregister = _htoa_pygeo.vectorf_swigregister
vectorf_swigregister(vectorf)

class Session(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Session, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Session, name)
    __repr__ = _swig_repr

    def __init__(self, rop_path, time=0):
        this = _htoa_pygeo.new_Session(rop_path, time)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _htoa_pygeo.delete_Session
    __del__ = lambda self: None

    def setTime(self, time):
        return _htoa_pygeo.Session_setTime(self, time)

    def setFrame(self, frame):
        return _htoa_pygeo.Session_setFrame(self, frame)

    def setRop(self, rop_path):
        return _htoa_pygeo.Session_setRop(self, rop_path)

    def parmInt(self, *args):
        return _htoa_pygeo.Session_parmInt(self, *args)

    def parmBool(self, *args):
        return _htoa_pygeo.Session_parmBool(self, *args)

    def parmFlt(self, *args):
        return _htoa_pygeo.Session_parmFlt(self, *args)

    def parmVec(self, *args):
        return _htoa_pygeo.Session_parmVec(self, *args)

    def parmStr(self, *args):
        return _htoa_pygeo.Session_parmStr(self, *args)

    def frame(self):
        return _htoa_pygeo.Session_frame(self)

    def time(self):
        return _htoa_pygeo.Session_time(self)

    def rop(self):
        return _htoa_pygeo.Session_rop(self)

    def isTraceEnabled(self):
        return _htoa_pygeo.Session_isTraceEnabled(self)

    def isExtraUserDataEnabled(self):
        return _htoa_pygeo.Session_isExtraUserDataEnabled(self)

    def instancees(self):
        return _htoa_pygeo.Session_instancees(self)

    def isForcedPhantom(self, op):
        return _htoa_pygeo.Session_isForcedPhantom(self, op)
Session_swigregister = _htoa_pygeo.Session_swigregister
Session_swigregister(Session)

class Object(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Object, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Object, name)
    __repr__ = _swig_repr
    NO_POINT_RENDERING = _htoa_pygeo.Object_NO_POINT_RENDERING
    RENDER_ONLY_POINTS = _htoa_pygeo.Object_RENDER_ONLY_POINTS
    RENDER_UNCONNECTED = _htoa_pygeo.Object_RENDER_UNCONNECTED

    def __init__(self, *args):
        this = _htoa_pygeo.new_Object(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _htoa_pygeo.delete_Object
    __del__ = lambda self: None

    def build(self):
        return _htoa_pygeo.Object_build(self)

    def generate(self):
        return _htoa_pygeo.Object_generate(self)

    def isInstance(self):
        return _htoa_pygeo.Object_isInstance(self)

    def translateAs(self):
        return _htoa_pygeo.Object_translateAs(self)

    def objPath(self):
        return _htoa_pygeo.Object_objPath(self)

    def sopPath(self):
        return _htoa_pygeo.Object_sopPath(self)

    def session(self):
        return _htoa_pygeo.Object_session(self)

    def detail(self):
        return _htoa_pygeo.Object_detail(self)

    def obj(self):
        return _htoa_pygeo.Object_obj(self)

    def mb(self):
        return _htoa_pygeo.Object_mb(self)

    def inputMb(self):
        return _htoa_pygeo.Object_inputMb(self)

    def accelerationAttribute(self):
        return _htoa_pygeo.Object_accelerationAttribute(self)

    def velocityAttribute(self):
        return _htoa_pygeo.Object_velocityAttribute(self)

    def smoothing(self):
        return _htoa_pygeo.Object_smoothing(self)

    def materials(self):
        return _htoa_pygeo.Object_materials(self)

    def material_idxs(self):
        return _htoa_pygeo.Object_material_idxs(self)

    def attributeNames(self):
        return _htoa_pygeo.Object_attributeNames(self)

    def instanceIndex(self):
        return _htoa_pygeo.Object_instanceIndex(self)

    def renderAsPoints(self):
        return _htoa_pygeo.Object_renderAsPoints(self)

    def userOptions(self):
        return _htoa_pygeo.Object_userOptions(self)

    def mergeVertexData(self):
        return _htoa_pygeo.Object_mergeVertexData(self)
    __swig_getmethods__["printShaderMap"] = lambda x: _htoa_pygeo.Object_printShaderMap
    if _newclass:
        printShaderMap = staticmethod(_htoa_pygeo.Object_printShaderMap)

    def shutterRange(self):
        return _htoa_pygeo.Object_shutterRange(self)

    def bprop(self, prop_name, defvalue=False):
        return _htoa_pygeo.Object_bprop(self, prop_name, defvalue)

    def iprop(self, prop_name, defvalue=-1):
        return _htoa_pygeo.Object_iprop(self, prop_name, defvalue)

    def fprop(self, prop_name, defvalue=-1.0):
        return _htoa_pygeo.Object_fprop(self, prop_name, defvalue)

    def sprop(self, *args):
        return _htoa_pygeo.Object_sprop(self, *args)

    def bprop2(self, prop_name, prop_name2, defvalue=False):
        return _htoa_pygeo.Object_bprop2(self, prop_name, prop_name2, defvalue)

    def iprop2(self, prop_name, prop_name2, defvalue=-1):
        return _htoa_pygeo.Object_iprop2(self, prop_name, prop_name2, defvalue)

    def fprop2(self, prop_name, prop_name2, defvalue=-1.0):
        return _htoa_pygeo.Object_fprop2(self, prop_name, prop_name2, defvalue)

    def isPhantom(self):
        return _htoa_pygeo.Object_isPhantom(self)
Object_swigregister = _htoa_pygeo.Object_swigregister
Object_swigregister(Object)

def Object_printShaderMap(*args):
    return _htoa_pygeo.Object_printShaderMap(*args)
Object_printShaderMap = _htoa_pygeo.Object_printShaderMap

# This file is compatible with both classic and new-style classes.

