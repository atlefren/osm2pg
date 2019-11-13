# -*- coding: utf-8 -*-
from lgeos import lgeos
from ctypes import string_at, c_char_p, c_size_t, pointer


def add_srid(wkb, srid=4326):
    wkb_bytes = str(wkb).encode('ascii')
    reader = lgeos.GEOSWKBReader_create()
    geos_geom = lgeos.GEOSWKBReader_readHEX(
        reader,
        c_char_p(wkb_bytes),
        c_size_t(len(wkb_bytes))
    )
    writer = lgeos.GEOSWKBWriter_create()
    lgeos.GEOSWKBWriter_setIncludeSRID(writer, bool(True))
    lgeos.GEOSSetSRID(geos_geom, srid)
    size = c_size_t()
    result = lgeos.GEOSWKBWriter_writeHEX(writer, geos_geom, pointer(size))
    data = string_at(result, size.value)
    lgeos.GEOSFree(result)
    return data.decode('ascii')
