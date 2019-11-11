import osmium as o
import sys
import psycopg2
from psycopg2.extras import Json

wkbfab = o.geom.WKTFactory()


def parse_taglist(taglist):
    res = {}
    for tag in taglist:
        res[tag.k] = tag.v
    return res


class FileStatsHandler(o.SimpleHandler):

    def __init__(self):
        super(FileStatsHandler, self).__init__()
        self.conn = psycopg2.connect(
            "dbname=bench2 user=atlefren host=13.79.191.128 password=nisse2gnom"
        )
        self.cursor = self.conn.cursor()
        self.c = 0

    def save_geom(self, geom, obj):
        tags = parse_taglist(obj.tags)
        data = {
            'id': obj.id,
            'version': obj.version,
            'timestamp': obj.timestamp,
            'tags': Json(tags),
            'geom': geom
        }

        self.cursor.execute('''
            INSERT INTO diff.osm
                (id, version, timestamp, tags, geom)
            VALUES (%(id)s, %(version)s, %(timestamp)s, %(tags)s, ST_SETSRID(ST_GeomFromText(%(geom)s), 4326))
            ''', data)
        self.c += 1
        if self.c % 1000 == 0:
            print('Commited')
            self.conn.commit()
            print('Commited: %s' % self.c)

    def node(self, n):
        g = wkbfab.create_point(n)
        self.save_geom(g, n)

    def area(self, a):
        g = wkbfab.create_multipolygon(a)
        self.save_geom(g, a)

    def way(self, w):
        g = wkbfab.create_linestring(w)
        self.save_geom(g, w)


def main(osmfile):
    h = FileStatsHandler()

    #  h.apply_file(osmfile, locations=True)
    h.apply_file(osmfile, locations=True)
    print("!!")

    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1]))
