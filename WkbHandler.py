# -*- coding: utf-8 -*-
import osmium
import copy

from ewkb import add_srid


def parse_taglist(taglist):
    res = {}
    for tag in taglist:
        res[tag.k] = copy.deepcopy(tag.v)
    return res


wkb_factory = osmium.geom.WKBFactory()


class WKBHandler(osmium.SimpleHandler):

    def __init__(self, geom_type, queue):
        super(WKBHandler, self).__init__()
        self.queue = queue
        self.geom_type = geom_type

    def save_geom(self, geom, obj):
        tags = parse_taglist(obj.tags)
        data = {
            'id': copy.deepcopy(obj.id),
            'version': copy.deepcopy(obj.version),
            'timestamp': copy.deepcopy(obj.timestamp),
            'tags': tags,
            'geom': add_srid(geom)
        }
        del obj
        self.queue.put(data)
        self.queue.join()  # Blocks until task_done is called

    def node(self, n):
        if self.geom_type != 'point':
            return
        try:
            g = wkb_factory.create_point(n)
            self.save_geom(g, n)
        except Exception as e:
            print('err', e, n.id)

    def area(self, a):
        if self.geom_type != 'polygon':
            return
        try:
            g = wkb_factory.create_multipolygon(a)
            self.save_geom(g, a)
        except Exception as e:
            print('err', e, a.id)

    def way(self, w):
        if self.geom_type != 'linestring':
            return
        try:
            g = wkb_factory.create_linestring(w)
            self.save_geom(g, w)
        except Exception as e:
            print('err', e, w.id)
