# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Unicode, String, ForeignKey, desc, cast, text
from sqlalchemy.orm import relationship, backref, column_property

Base = declarative_base()


class Participant(Base):
    """ Участник голосования - кандидат или партия """
    __tablename__ = 'participant'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    color = Column(String(6), nullable=False)

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            color=(
                int(self.color[0:2], 16),
                int(self.color[2:4], 16),
                int(self.color[4:6], 16),
            )
        )


class Level(Base):
    """ Уровень иерархии """
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    geometry = Column(String)
    zoom = Column(Integer)

    results = relationship('Result', backref=backref('level'))

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            geometry=self.geometry,
            zoom=self.zoom,
        )


class Result(Base):
    """ Результат голосования """
    __tablename__ = 'result'

    id = Column(Unicode, primary_key=True)
    level_id = Column(Integer, ForeignKey(Level.id), nullable=False)
    parent_id = Column(Unicode, ForeignKey('result.id'))

    name = Column(Unicode)

    a_canceled = Column(Integer)
    a_count = Column(Integer)
    a_issued_l = Column(Integer)
    a_issued_t = Column(Integer)
    a_stolen = Column(Integer)
    b_canceled = Column(Integer)
    b_count = Column(Integer)
    b_early = Column(Integer)
    b_fixed = Column(Integer)
    b_inside = Column(Integer)
    b_invalid = Column(Integer)
    b_outside = Column(Integer)
    b_portable = Column(Integer)
    b_stolen = Column(Integer)
    b_valid = Column(Integer)
    b_wtf = Column(Integer)
    v_abs = Column(Integer)
    v_count = Column(Integer)

    # полигон
    area_wkt = Column(String)

    # центроид
    centroid_x = Column(Float)
    centroid_y = Column(Float)

    # место для голосования
    site_x = Column(Float)
    site_y = Column(Float)
    site_address = Column(Unicode)

    # расположение комиссии
    office_x = Column(Float)
    office_y = Column(Float)
    office_address = Column(Unicode)
    
    # вычисляемые поля
    turnout_c = Column(Integer)
    turnout_p = Column(Float)
    absentee_c = Column(Integer)
    absentee_p = Column(Float)

    votes = relationship('ResultVote', order_by=desc('result_vote.vote_count'))

    @property
    def parameters(self):
        vparameters = dict()
        for v in self.votes:
            vparameters[v.participant_id] = (v.vote_persent, v.vote_count)

        return dict(
            participant=vparameters,
            participant_order=[v.participant_id for v in self.votes],
            turnout=(round(self.turnout_p, 2), self.turnout_c),
            absentee=(round(self.absentee_p, 2) if self.absentee_p else None, self.absentee_c),
        )

    def update_vote_persent(self):
        vsum = 0
        for v in self.votes:
            vsum += v.vote_count

        for v in self.votes:
            v.vote_persent = round(100.0 * v.vote_count / vsum, 2)

    @classmethod
    def update_calc_fields(cls, session):
        session.execute(text("""
            UPDATE result SET
                turnout_c = b_valid + b_invalid,
                turnout_p = round(100.0 * (b_valid + b_invalid) / v_count, 2),
                absentee_c = v_abs,
                absentee_p = round(100.0 * v_abs / v_count,2 );
        """))


class ResultVote(Base):
    """ Количество голосов за определнную партию или кандитата """
    __tablename__ = 'result_vote'

    result_id = Column(Unicode, ForeignKey(Result.id), primary_key=True)
    participant_id = Column(Integer, ForeignKey(Participant.id), primary_key=True)
    vote_count = Column(Integer, nullable=False)
    vote_persent = Column(Float)


metadata = Base.metadata
