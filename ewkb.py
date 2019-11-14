# -*- coding: utf-8 -*-
from lgeos import readWkbHex, writeEWkbHex


def add_srid(wkb, srid=4326):
    try:
        geom = readWkbHex(wkb)
        ewkt = writeEWkbHex(geom, srid)
        return ewkt
    except MemoryError as e:
        print(e)
        raise e
