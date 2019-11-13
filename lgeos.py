# -*- coding: utf-8 -*-
from ctypes import (CDLL, DEFAULT_MODE, c_char_p, c_void_p, c_int, c_size_t,
                    POINTER, CFUNCTYPE, Structure, pointer, string_at)
from ctypes.util import find_library


c_size_t_p = POINTER(c_size_t)


class allocated_c_char_p(c_char_p):
    pass


def error_handler(fmt, *fmt_args):
    pass


def notice_handler(fmt, *fmt_args):
    pass


_lgeos = CDLL(find_library('geos_c'), mode=DEFAULT_MODE)

EXCEPTION_HANDLER_FUNCTYPE = CFUNCTYPE(None, c_char_p, c_void_p)
_lgeos.initGEOS.restype = None
_lgeos.initGEOS.argtypes = [
    EXCEPTION_HANDLER_FUNCTYPE,
    EXCEPTION_HANDLER_FUNCTYPE
]


# WKBReader


class WKBReader_st(Structure):
    pass


WKB_READ_PTR = POINTER(WKBReader_st)

# create
_lgeos.GEOSWKBReader_create.restype = WKB_READ_PTR
_lgeos.GEOSWKBReader_create.argtypes = []

# read
_lgeos.GEOSWKBReader_readHEX.restype = c_void_p
_lgeos.GEOSWKBReader_readHEX.argtypes = [c_void_p, c_char_p, c_size_t]

# destroy
_lgeos.GEOSWKBReader_destroy.restype = None
_lgeos.GEOSWKBReader_destroy.argtypes = [WKB_READ_PTR]

# WKBWriter


class WKBWriter_st(Structure):
    pass


WKB_WRITE_PTR = POINTER(WKBReader_st)

_lgeos.GEOSWKBWriter_create.restype = WKB_WRITE_PTR
_lgeos.GEOSWKBWriter_create.argtypes = []

_lgeos.GEOSWKBWriter_destroy.restype = None
_lgeos.GEOSWKBWriter_destroy.argtypes = [WKB_WRITE_PTR]

_lgeos.GEOSWKBWriter_writeHEX.restype = allocated_c_char_p
_lgeos.GEOSWKBWriter_writeHEX.argtypes = [c_void_p, c_void_p, c_size_t_p]

_lgeos.GEOSWKBWriter_setIncludeSRID.restype = None
_lgeos.GEOSWKBWriter_setIncludeSRID.argtypes = [c_void_p, c_int]

# utils

_lgeos.GEOSSetSRID.restype = None
_lgeos.GEOSSetSRID.argtypes = [c_void_p, c_int]

_lgeos.GEOSFree.restype = None
_lgeos.GEOSFree.argtypes = [c_void_p]


error_h = EXCEPTION_HANDLER_FUNCTYPE(error_handler)
notice_h = EXCEPTION_HANDLER_FUNCTYPE(notice_handler)


geos_handle = _lgeos.initGEOS(notice_h, error_h)

lgeos = _lgeos


def readWkbHex(wkbhex):
    reader = lgeos.GEOSWKBReader_create()
    wkb_bytes = str(wkbhex).encode('ascii')
    geos_geom = lgeos.GEOSWKBReader_readHEX(
        reader,
        c_char_p(wkb_bytes),
        c_size_t(len(wkb_bytes))
    )
    lgeos.GEOSWKBReader_destroy(reader)
    return geos_geom


def writeEWkbHex(geos_geom, srid=4326):
    writer = lgeos.GEOSWKBWriter_create()
    _lgeos.GEOSWKBWriter_setIncludeSRID(writer, bool(True))
    size = c_size_t()
    result = lgeos.GEOSWKBWriter_writeHEX(writer, geos_geom, pointer(size))
    lgeos.GEOSSetSRID(geos_geom, srid)
    data = string_at(result, size.value)
    lgeos.GEOSFree(result)
    lgeos.GEOSWKBWriter_destroy(writer)
    return data.decode('ascii')
