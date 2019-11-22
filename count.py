# -*- coding: utf-8 -*-
import sys
import osmium


class CountHandler(osmium.SimpleHandler):

    def __init__(self):
        super(CountHandler, self).__init__()
        self.nodes = 0
        self.areas = 0
        self.ways = 0

    def node(self, n):
        self.nodes += 1

    def area(self, a):
        self.areas += 1

    def way(self, w):
        self.ways += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    path = sys.argv[1]

    handler = CountHandler()
    handler.apply_file(path, locations=False)
    print(f'nodes: {handler.nodes:,}')
    print(f'ways: {handler.ways:,}')
    print(f'areas: {handler.areas:,}')
