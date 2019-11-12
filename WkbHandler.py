# -*- coding: utf-8 -*-

import osmium

from ewkb import add_srid


def parse_taglist(taglist):
    res = {}
    for tag in taglist:
        res[tag.k] = tag.v
    return res


wkb_factory = osmium.geom.WKBFactory()


class WKBHandler(osmium.SimpleHandler):

    def __init__(self, queue):
        super(WKBHandler, self).__init__()
        self.queue = queue

    def save_geom(self, geom, obj):
        tags = parse_taglist(obj.tags)
        data = {
            'id': obj.id,
            'version': obj.version,
            'timestamp': obj.timestamp,
            'tags': tags,
            'geom': add_srid(geom)
        }

        self.queue.put(data)

    def node(self, n):
        g = wkb_factory.create_point(n)
        self.save_geom(g, n)

    def area(self, a):
        g = wkb_factory.create_multipolygon(a)
        self.save_geom(g, a)

    def way(self, w):
        g = wkb_factory.create_linestring(w)
        self.save_geom(g, w)
