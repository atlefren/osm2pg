# -*- coding: utf-8 -*-
from pygeos import to_wkb, from_wkb, set_srid


def add_srid(wkb, srid=4326):
    return to_wkb(
        set_srid(from_wkb(wkb), srid),
        hex=True,
        include_srid=True
    )
