# -*- coding: utf-8 -*-
import sys
import osmium


class CountHandler(osmium.SimpleHandler):

    def __init__(self):
        super(CountHandler, self).__init__()
        self.c = 0

    def node(self, n):
        self.c += 1

    def area(self, a):
        self.c += 1

    def way(self, w):
        self.c += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    path = sys.argv[1]

    handler = CountHandler()
    handler.apply_file(path, locations=False)
    print(handler.c)
