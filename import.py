import tracemalloc
import sys
import os
import psycopg2

from queue import Queue
from _thread import start_new_thread

from WkbHandler import WKBHandler
from IteratorFile import IteratorFile
from split_generator import split_generator


def get_pg_conn():
    conn_str = os.environ['CONN_STR']
    return psycopg2.connect(conn_str)


def read_and_parse(osmfile):
    """
    Uses Osmium and our WKBHandler to parse geometries
    Use some tricks (a Queue and a new thread) to convert
    this into a generator
    """
    queue = Queue()
    job_done = object()

    def task():
        handler = WKBHandler(queue)
        handler.apply_file(osmfile, locations=True)
        queue.put(job_done)

    start_new_thread(task, ())
    while True:
        next_item = queue.get(True)  # Blocks until an input is available
        queue.task_done()
        if next_item is job_done:
            break
        yield next_item


def write_to_db(feature_generator, table_name):
    columns = ['id', 'version', 'timestamp', 'tags', 'geom']

    connection = get_pg_conn()
    num = 200000
    tracemalloc.start()
    start = tracemalloc.take_snapshot()
    with connection.cursor() as cur:
        for file_generator in split_generator(feature_generator, num):

            file = IteratorFile(file_generator, columns)
            cur.copy_from(file, table_name, columns=columns)
            connection.commit()
            print('commit')
            current = tracemalloc.take_snapshot()
            stats = current.compare_to(start, 'filename')
            for i, stat in enumerate(stats[:1], 1):
                print('since_start', i, str(stat))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    path = sys.argv[1]
    generator = read_and_parse(path)
    write_to_db(generator, 'diff.osm')
