# -*- coding: utf-8 -*-
import os.path
import csv

import geojson
from shapely.geometry import asShape

from votemapper.model import (
    Result,
    ResultVote,
)


class BaseDatasource(object):

    def __init__(self, config=None, **kwargs):
        self._config = config
        self._geometry = config.parent.geometry

    def _process_record(self, record):
        return record


class CSVDatasource(BaseDatasource):

    def __init__(self, config=None, **kwargs):
        BaseDatasource.__init__(self, config, **kwargs)
        self.__filename = kwargs['file']

    def read(self):
        fn = os.path.join(self._config.parent.parent.basedir, self.__filename)
        with open(fn, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header = None
            for row in reader:
                if not header:
                    header = row
                else:
                    for i in self.__read_row(header, row):
                        yield i

    def __read_row(self, header, row):
        obj = Result(level_id=self._config.parent.id)

        record = self._process_record(dict(zip(header, row)))
        for k, v in record.items():
            if v == '':
                v = None
            if k in ('id', 'parent_id', 'name') and v:
                v = v.decode('utf-8')
            if not k.startswith('vote_count_') and hasattr(obj, k):
                setattr(obj, k, v)

        yield obj

        for k, v in record.items():
            if k.startswith('vote_count_'):
                vobj = ResultVote(
                    result_id=obj.id,
                    participant_id=int(k.replace('vote_count_', '')),
                    vote_count=int(v)
                )
                yield vobj


class GeoJSONDatasource(BaseDatasource):

    def __init__(self, config=None, **kwargs):
        BaseDatasource.__init__(self, config, **kwargs)
        self.__filename = kwargs['file']

    def read(self):
        fn = os.path.join(self._config.parent.parent.basedir, self.__filename)
        with open(fn, 'r') as f:
            data = geojson.loads(
                f.read(),
                object_hook=geojson.GeoJSON.to_instance
            )
            for f in data.features:
                obj = Result(
                    id=f.properties['ID'],
                    level_id=self._config.parent.id
                )
                if self._geometry == 'area':
                    obj.area_wkt = asShape(f.geometry).wkt
                yield obj


DATASOURCE_BY_NAME = dict(
    csv=CSVDatasource,
    geojson=GeoJSONDatasource,
)
