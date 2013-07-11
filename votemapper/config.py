# -*- coding: utf-8 -*-
import os.path
import yaml
import re


DEFAULT_BASELAYER = dict(
    url="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution=u"Map data © OpenStreetMap contributors"
)

DEFAULT_PARTICIPANT_COLOR = (
    (166, 206, 227),
    (31, 120, 180),
    (178, 223, 138),
    (51, 160, 44),
    (251, 154, 153),
    (227, 26, 28),
    (253, 191, 111),
    (255, 127, 0),
    (202, 178, 214),
    (106, 61, 154),
)


class ConfigurationError(Exception):
    pass


class Config(object):

    def __init__(self, filename):
        self.basedir = os.path.split(filename)[0]

        with open(filename, 'r') as f:
            data = yaml.load(f)
            self._data = data

        self.title = data.get('title', None)
        self.subtitle = data.get('subtitle', None)

        self.baselayer = data.get('baselayer', DEFAULT_BASELAYER)

        if not 'participants' in data or not isinstance(data['participants'], list):
            raise ConfigurationError("Missing 'participants' section!")

        participants = []
        index = 1
        for p in data['participants']:
            participants.append(ParticipantConfig(self, index, p))
            index += 1

        self.participants = tuple(participants)

        if not 'levels' in data or not isinstance(data['levels'], list):
            raise ConfigurationError("Missing 'levels' section!")

        levels = []
        index = 1
        for l in data['levels']:
            levels.append(LevelConfig(self, index, l))
            index += 1

        self.levels = tuple(levels)


class ParticipantConfig(object):

    def __init__(self, parent, id, data):
        self.parent = parent
        self.id = id

        if not 'name' in data or not isinstance(data['name'], basestring):
            raise ConfigurationError("Missing 'name' for participant %d" % (id))

        self.name = unicode(data['name'])

        if not 'color' in data and id > len(DEFAULT_PARTICIPANT_COLOR):
            raise ConfigurationError("Missing 'color' for participant %d" % (id))

        if 'color' in data:
            if not re.match('[0-9a-f]{6}', data['color']):
                raise ConfigurationError("Invalid color: %s", data['color'])
            self.color = data['color']
        else:
            self.color = ''.join([hex(c)[2:] for c in DEFAULT_PARTICIPANT_COLOR[id]])


class LevelConfig(object):

    def __init__(self, parent, id, data):
        self.parent = parent
        self.id = id

        if not 'name' in data or not isinstance(data['name'], basestring):
            raise ConfigurationError("Missing 'name' for level %d" % (id))

        self.name = data['name']

        if not 'geometry' in data:
            raise ConfigurationError("Missing 'geometry' for level %d" % (id))

        if not isinstance(data['geometry'], basestring) or not data['geometry'] in ('area', 'site', 'office'):
            raise ConfigurationError("Invalid 'geometry' for level %d" % (id))

        self.geometry = data['geometry']

        if id > 1 and not 'zoom' in data:
            raise ConfigurationError("Missing 'zoom' for level %d" % (id))

        if id == 1 and 'zoom' in data:
            raise ConfigurationError("Unused 'zoom' for level %d" % (id))

        if 'zoom' in data:
            self.zoom = int(data['zoom'])
        else:
            self.zoom = None

        if not 'datasource' in data:
            raise ConfigurationError("Missing 'datasource' for level %d" % (id))

        datasource_data = data['datasource'] if isinstance(data['datasource'], list) else (data['datasource'], )
        datasources = []
        for d in datasource_data:
            datasources.append(DatasourceConfig(self, d))

        self.datasources = tuple(datasources)



class DatasourceConfig(object):
    
    def __init__(self, parent, data):
        self.parent = parent
        self.type = data['type']

        t = dict(data)
        del t['type']
        self.data = t