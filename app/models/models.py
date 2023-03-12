from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, ForeignKey, String, DateTime, Numeric
from sqlalchemy import Enum
from datetime import datetime
from app.utils.utils import uuid4Str
from .enums import *
from app import db, ma
from marshmallow import fields

class MedicalCase(db.Model):
    uuid = Column(String(40), primary_key=True, default=uuid4Str)
    type_of_injury = Column(Enum(TypeOfInjury))
    shape_of_injury = Column(Enum(ShapeOfInjury))
    number_of_injuries = Column(Enum(NumberOfInjuries))
    injury_distribucion = Column(Enum(InjuryDistribution))
    body_part = Column(Enum(BodyPart))
    type_of_diagnosis = Column(Enum(TypeOfDiagnosis))
    patient_uuid = Column(String(40), ForeignKey('patient.uuid'), nullable=False)
    doctor_uuid = Column(String(40), ForeignKey('doctor.uuid'), nullable=True)

    class Config:
        use_enum_values = True

class MedicalDiagnostic(db.Model):
    uuid = Column(String(40), primary_key=True, default=uuid4Str)
    name_of_injury = Column(String(24))
    diagnosis = Column(String(200))
    treatment = Column(String(200))
    diagnostic_date = Column(DateTime, default=datetime.now())
    certification_percentage = Column(String(5), nullable=True)
    medical_case_uuid = Column(String(40), ForeignKey('medical_case.uuid'), nullable=True)
    doctor_uuid = Column(String(40), ForeignKey('doctor.uuid'), nullable=True)
    
class Doctor(db.Model):
    uuid = Column(String(40), primary_key=True, nullable=False)
    location = Column(String(150), nullable=False)
    diagnostics = db.relationship("MedicalDiagnostic", backref="doctor", lazy='dynamic')

class Patient(db.Model):
    uuid = Column(String(40), primary_key=True, nullable=False)
    location = Column(String(150), nullable=False)
    notifications = db.relationship('Notification', backref='patient', lazy=True)

class Notification(db.Model):
    uuid = Column(String(40), primary_key=True, nullable=False)
    title = Column(String(40))
    message = Column(String(100))
    patient_uuid = db.Column(String(40), db.ForeignKey('patient.uuid'), nullable=False)


class EnumField(ma.Field):
    def _serialize(self, value, attr, obj):
        return value.name

class MedicalCaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  MedicalCase
        load_instance = True
        include_relationships = True

    type_of_injury = EnumField()
    shape_of_injury = EnumField()
    number_of_injuries = EnumField()
    injury_distribucion = EnumField()
    body_part = EnumField()
    type_of_diagnosis = EnumField()

class DoctorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Doctor
        load_instance = True
        exclude = ('location',)

class MedicalDiagnosticSchema(SQLAlchemyAutoSchema):
    
    class Meta:
        model = MedicalDiagnostic
        exclude = ('diagnostic_date',)
        load_instance = True
        include_relationships = True

    doctor = fields.Nested(DoctorSchema)

class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        