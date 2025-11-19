from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    document_id = Column(String(50), unique=True, index=True)  # ex: CPF
    email = Column(String(200), unique=True, index=True)

    prescriptions = relationship("Prescription", back_populates="patient")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    drug_name = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=False)
    notes = Column(Text)

    patient = relationship("Patient", back_populates="prescriptions")
