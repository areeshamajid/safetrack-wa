from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Site(Base):
    __tablename__ = 'sites'

    site_id        = Column(Integer, primary_key=True)
    operator_name  = Column(String(200), nullable=False)
    commodity      = Column(String(50))
    region         = Column(String(50))
    total_area_ha  = Column(Float)
    lease_count    = Column(Integer)

    workers             = relationship('Worker',           back_populates='site')
    incidents           = relationship('Incident',         back_populates='site')
    near_miss           = relationship('NearMiss',         back_populates='site')
    inspections         = relationship('Inspection',       back_populates='site')
    compliance_actions  = relationship('ComplianceAction', back_populates='site')


class Worker(Base):
    __tablename__ = 'workers'

    worker_id       = Column(Integer, primary_key=True)
    site_id         = Column(Integer, ForeignKey('sites.site_id'))
    first_name      = Column(String(50))
    last_name       = Column(String(50))
    role            = Column(String(100))
    department      = Column(String(100))
    employment_type = Column(String(50))
    start_date      = Column(Date)

    site      = relationship('Site',     back_populates='workers')
    incidents = relationship('Incident', back_populates='worker')


class Incident(Base):
    __tablename__ = 'incidents'

    incident_id       = Column(Integer, primary_key=True)
    site_id           = Column(Integer, ForeignKey('sites.site_id'))
    worker_id         = Column(Integer, ForeignKey('workers.worker_id'))
    incident_date     = Column(Date)
    incident_type     = Column(String(20))
    hazard_category   = Column(String(100))
    severity          = Column(String(20))
    shift             = Column(String(20))
    body_part_injured = Column(String(50))
    days_lost         = Column(Integer)
    description       = Column(Text)
    corrective_action = Column(Text)

    site   = relationship('Site',   back_populates='incidents')
    worker = relationship('Worker', back_populates='incidents')


class NearMiss(Base):
    __tablename__ = 'near_miss'

    near_miss_id             = Column(Integer, primary_key=True)
    site_id                  = Column(Integer, ForeignKey('sites.site_id'))
    report_date              = Column(Date)
    hazard_category          = Column(String(100))
    shift                    = Column(String(20))
    location_on_site         = Column(String(100))
    potential_severity       = Column(String(20))
    corrective_action_taken  = Column(Boolean)
    description              = Column(Text)

    site = relationship('Site', back_populates='near_miss')


class Inspection(Base):
    __tablename__ = 'inspections'

    inspection_id   = Column(Integer, primary_key=True)
    site_id         = Column(Integer, ForeignKey('sites.site_id'))
    inspection_date = Column(Date)
    inspector       = Column(String(100))
    inspection_type = Column(String(50))
    findings_count  = Column(Integer)
    score           = Column(Integer)
    passed          = Column(Boolean)

    site               = relationship('Site',             back_populates='inspections')
    compliance_actions = relationship('ComplianceAction', back_populates='inspection')


class ComplianceAction(Base):
    __tablename__ = 'compliance_actions'

    action_id          = Column(Integer, primary_key=True)
    inspection_id      = Column(Integer, ForeignKey('inspections.inspection_id'))
    site_id            = Column(Integer, ForeignKey('sites.site_id'))
    action_description = Column(Text)
    due_date           = Column(Date)
    status             = Column(String(20))
    priority           = Column(String(20))

    site       = relationship('Site',       back_populates='compliance_actions')
    inspection = relationship('Inspection', back_populates='compliance_actions')
    