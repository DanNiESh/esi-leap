from oslo_db.sqlalchemy import models
from oslo_db.sqlalchemy import types as db_types

from sqlalchemy import (Column, DateTime, Index, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import ForeignKey, DateTime, Boolean, Text, Float


class ESILEAPBase(models.TimestampMixin, models.ModelBase):

    metadata = None


Base = declarative_base(cls=ESILEAPBase)


class Policy(Base):
    """Represents a policy that can be applied to a node."""

    __tablename__ = 'policies'
    __table_args__ = (
        Index('project_id_idx', 'project_id'),
        Index('uuid_idx', 'uuid'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column(String(36), nullable=False)
    project_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    max_time_for_lease = Column(Integer, default=0)
    extendible = Column(Boolean, default=False)


class AppliedPolicy(Base):
    """Represents a policy applied to a node."""

    __tablename__ = 'applied_policies'
    __table_args__ = (
        Index('policy_uuid_idx', 'policy_uuid'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    node_uuid = Column(String(36), nullable=False)
    policy_uuid = Column(String(36),
                         ForeignKey('policies.uuid'),
                         nullable=False)
    expiration_date = Column(DateTime)

    policy = orm.relationship(Policy,
                              backref=orm.backref('applied_nodes'),
                              foreign_keys=policy_uuid,
                              primaryjoin=policy_uuid == Policy.uuid)


class LeaseRequest(Base):
    """Represents a lease request."""

    __tablename__ = 'lease_requests'
    __table_args__ = (
        Index('project_id_idx', 'project_id'),
        Index('uuid_idx', 'uuid'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column(String(36), nullable=True)
    project_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    node_properties = Column(db_types.JsonEncodedDict)
    min_nodes = Column(Integer, default=0)
    max_nodes = Column(Integer, default=0)
    lease_time = Column(Integer, default=0)
    status = Column(String(15), nullable=False)
    cancel_date = Column(DateTime)
    fulfilled_date = Column(DateTime)
    expiration_date = Column(DateTime)


class LeasedNode(Base):
    """Represents a leased node."""

    __tablename__ = 'leased_nodes'
    __table_args__ = (
        Index('node_uuid_idx', 'node_uuid'),
        Index('request_uuid_idx', 'request_uuid'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    node_uuid = Column(String(36), nullable=False)
    request_uuid = Column(String(36),
                          ForeignKey('lease_requests.uuid'),
                          nullable=False)
    expiration_date = Column(DateTime)

    lease_request = orm.relationship(LeaseRequest,
                                     backref=orm.backref('leases'),
                                     foreign_keys=request_uuid,
                                     primaryjoin=request_uuid == LeaseRequest.uuid)