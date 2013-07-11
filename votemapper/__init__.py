import os

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from mako.lookup import TemplateLookup

import geojson
from shapely import wkt

from votemapper.model import metadata, Participant, Level, Result, ResultVote
from votemapper.datasource import DATASOURCE_BY_NAME
from votemapper.config import Config

__all__ = ('Env', 'Config')


class Env(object):

    def __init__(self, config):
        self._config = config
        self._engine = create_engine('sqlite:///tmp.sqlite')
        self._session = Session(bind=self._engine)

        root = os.path.abspath(os.path.dirname(__file__))
        self._templates = TemplateLookup(
            directories=[os.path.join(root, 'template'), ],
            input_encoding='utf-8',
            output_encoding='utf-8',
        )

    @property
    def config(self):
        return self._config

    @property
    def session(self):
        return self._session

    @property
    def levels(self):
        return self.session.query(Level)

    @property
    def participants(self):
        return self.session.query(Participant)

    def build_database(self):
        metadata.drop_all(self._session.connection())
        metadata.create_all(self._session.connection())

        for p in self.config.participants:
            pobj = Participant(id=p.id, name=p.name, color=p.color)
            self.session.merge(pobj)

        for l in self.config.levels:
            lobj = Level(
                id=l.id, name=l.name,
                geometry=l.geometry, zoom=l.zoom
            )
            self.session.merge(lobj)

            for d in l.datasources:
                ds = DATASOURCE_BY_NAME[d.type](config=d, **d.data)
                for obj in ds.read():
                    self._session.merge(obj)

        for r in self.session.query(Result):
            r.update_vote_persent()

        Result.update_calc_fields(self.session)

        self._session.commit()

    def participant_vote_stat(self):
        q = self.session.query(
            ResultVote.participant_id.label('participant_id'),
            func.min(ResultVote.vote_persent).label('min'),
            func.max(ResultVote.vote_persent).label('max'),
        ).group_by(ResultVote.participant_id)

        result = dict()
        for r in q:
            result[r.participant_id] = dict(min=r.min, max=r.max)

        return result

    def parameter_stat(self):
        r = self.session.query(
            func.min(Result.turnout_p).label('turnout_min'),
            func.max(Result.turnout_p).label('turnout_max'),
            func.min(Result.absentee_p).label('absentee_min'),
            func.max(Result.absentee_p).label('absentee_max'),
        ).one()

        return dict(
            turnout=dict(min=r.turnout_min, max=r.turnout_max),
            absentee=dict(min=r.absentee_min, max=r.absentee_max),
        )

    def level_json(self, level_id):
        q = self._session.query(Result).filter_by(level_id=level_id)
        features = []
        for r in q:
            geom = None
            if r.level.geometry == 'area' and r.area_wkt:
                geom = wkt.loads(r.area_wkt)
            elif r.level.geometry == 'site' and r.site_x and r.site_y:
                geom = geojson.Point([r.site_x, r.site_y])

            if geom:
                f = geojson.Feature(
                    geometry=geom,
                    properties=dict(name=r.name, **r.parameters)
                )
                features.append(f)

        return geojson.dumps(geojson.FeatureCollection(features))

    def render_template(self, template, target, context):
        templateobj = self._templates.get_template(template)
        with open(target, 'w') as f:
            f.write(templateobj.render(**context))
