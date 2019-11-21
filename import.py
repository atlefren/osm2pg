import sys
import os

from queue import Queue
from _thread import start_new_thread
from WkbHandler import WKBHandler
from database import Database


def read_and_parse(osmfile, geom_type):
    """
    Uses Osmium and our WKBHandler to parse geometries
    Use some tricks (a Queue and a new thread) to convert
    this into a generator
    """
    queue = Queue()
    job_done = object()

    def task():
        handler = WKBHandler(geom_type, queue)
        handler.apply_file(
            osmfile,
            locations=True,
            idx=f'dense_file_array,{geom_type}.nodecache'
        )
        queue.put(job_done)
        queue.join()  # Blocks until task_done is called

    start_new_thread(task, ())

    while True:
        next_item = queue.get(True)  # Blocks until an input is available
        if next_item is job_done:
            break
        yield next_item
        queue.task_done()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    path = sys.argv[1]
    db = Database(os.environ['CONN_STR'])
    geom_types = ['point', 'linestring', 'polygon']
    for geom_type in geom_types:
        generator = read_and_parse(path, geom_type)
        db.write(generator, f'diff.osm_{geom_type}')
