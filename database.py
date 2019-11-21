# -*- coding: utf-8 -*-
import psycopg2

from split_generator import split_generator as split
from IteratorFile import IteratorFile


class Database:
    def __init__(self, conn_str, partition=20000):
        self.conn_str = conn_str
        self.partition = partition
        self.columns = ['id', 'version', 'timestamp', 'tags', 'geom']
        self.conn = None

    def get_cursor(self):
        if not self.conn:
            self.conn = psycopg2.connect(self.conn_str)
        return self.conn.cursor()

    def ensure_table(self, table_name):
        with self.get_cursor() as cur:
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id bigint,
                    version integer,
                    "timestamp" timestamp without time zone,
                    tags jsonb,
                    geom geometry(Geometry,4326)
                )
            ''')
            cur.execute(f'TRUNCATE TABLE {table_name}')

    def write(self, feature_generator, table_name):
        print(f'save to {table_name}')
        self.ensure_table(table_name)
        with self.get_cursor() as cur:
            for generator in split(feature_generator, self.partition):
                file = IteratorFile(generator, self.columns)
                cur.copy_from(file, table_name, columns=self.columns)
                print('commit')
