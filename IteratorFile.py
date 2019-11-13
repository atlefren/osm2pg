# -*- coding: utf-8 -*-
import io
import sys
import json
from datetime import datetime, date


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def escape(value):
    return value.replace('\\', '\\\\')


def format_line(record, columns):
    line_template = '\t'.join(['%s'] * 5)
    data = []
    for column in columns:
        value = None
        if column in record:
            value = record[column]

        if value is None or value == '':
            data.append('\\N')
        elif isinstance(value, dict):
            data.append(escape(json.dumps(
                value,
                ensure_ascii=False,
                cls=DateTimeEncoder
            )))
        else:
            data.append(value)
    return line_template % tuple(data)


class IteratorFile(io.TextIOBase):
    """
        Use this class to support writing geometries to PostGIS using COPY
        based on https://gist.github.com/jsheedy/ed81cdf18190183b3b7d
    """

    def __init__(self, records, columns):
        self._records = records
        self._columns = columns
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):
        pass

    def readline(self):
        return self._get_next()

    def _get_next(self):
        record = next(self._records)
        return format_line(record, self._columns)
