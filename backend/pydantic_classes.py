from datetime import datetime, date, time
from typing import List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator

from abc import ABC, abstractmethod

############################################
# Enumerations are defined here
############################################

class LicensingType(Enum):
    Open_Source = "Open_Source"
    Proprietary = "Proprietary"

class DatasetType(Enum):
    Training = "Training"
    Validation = "Validation"
    Test = "Test"

class EvaluationStatus(Enum):
    Custom = "Custom"
    Processing = "Processing"
    Pending = "Pending"
    Archived = "Archived"
    Done = "Done"

class ProjectStatus(Enum):
    Archived = "Archived"
    Ready = "Ready"
    Pending = "Pending"
    Created = "Created"
    Closed = "Closed"

############################################
# Classes are defined here
############################################
class MeasureCreate(BaseModel):
    error: str
    uncertainty: float
    value: float
    unit: str
    metric: int  # N:1 Relationship (mandatory)
    measurand: int  # N:1 Relationship (mandatory)
    observation: int  # N:1 Relationship (mandatory)

class AssessmentElementCreate(ABC, BaseModel):
    name: str
    description: str

class ElementCreate(AssessmentElementCreate):
    measure: Optional[List[int]] = None  # 1:N Relationship
    eval: List[int]  # N:M Relationship
    project: Optional[int] = None  # N:1 Relationship (optional)
    evalu: List[int]  # N:M Relationship

class MetricCreate(AssessmentElementCreate):
    measures: Optional[List[int]] = None  # 1:N Relationship
    derivedBy: List[int]  # N:M Relationship
    category: List[int]  # N:M Relationship

class MetricCategoryCreate(AssessmentElementCreate):
    metrics: List[int]  # N:M Relationship

class CommentsCreate(BaseModel):
    Name: str
    Comments: str
    TimeStamp: datetime

class LegalRequirementCreate(BaseModel):
    principle: str
    legal_ref: str
    standard: str
    project_1: int  # N:1 Relationship (mandatory)

class ToolCreate(BaseModel):
    source: str
    version: str
    name: str
    licensing: LicensingType
    observation_1: Optional[List[int]] = None  # 1:N Relationship

class ConfParamCreate(AssessmentElementCreate):
    param_type: str
    value: str
    conf: int  # N:1 Relationship (mandatory)

class ConfigurationCreate(AssessmentElementCreate):
    eval: Optional[List[int]] = None  # 1:N Relationship
    params: Optional[List[int]] = None  # 1:N Relationship

class FeatureCreate(ElementCreate):
    min_value: float
    feature_type: str
    max_value: float
    features: int  # N:1 Relationship (mandatory)
    date: int  # N:1 Relationship (mandatory)

class DatashapeCreate(BaseModel):
    accepted_target_values: str
    dataset_1: Optional[List[int]] = None  # 1:N Relationship
    f_features: Optional[List[int]] = None  # 1:N Relationship
    f_date: Optional[List[int]] = None  # 1:N Relationship

class DatasetCreate(ElementCreate):
    dataset_type: DatasetType
    version: str
    licensing: LicensingType
    source: str
    datashape: int  # N:1 Relationship (mandatory)
    models: Optional[List[int]] = None  # 1:N Relationship
    observation_2: Optional[List[int]] = None  # 1:N Relationship

class ProjectCreate(BaseModel):
    status: ProjectStatus
    name: str
    eval: Optional[List[int]] = None  # 1:N Relationship
    legal_requirements: Optional[List[int]] = None  # 1:N Relationship
    involves: Optional[List[int]] = None  # 1:N Relationship

class ModelCreate(ElementCreate):
    pid: str
    licensing: LicensingType
    source: str
    data: str
    dataset: int  # N:1 Relationship (mandatory)

class DerivedCreate(MetricCreate):
    expression: str
    baseMetric: List[int]  # N:M Relationship

class DirectCreate(MetricCreate):
    pass

class EvaluationCreate(BaseModel):
    status: EvaluationStatus
    project: int  # N:1 Relationship (mandatory)
    observations: Optional[List[int]] = None  # 1:N Relationship
    ref: List[int]  # N:M Relationship
    evaluates: List[int]  # N:M Relationship
    config: int  # N:1 Relationship (mandatory)

class ObservationCreate(AssessmentElementCreate):
    observer: str
    whenObserved: datetime
    tool: int  # N:1 Relationship (mandatory)
    eval: int  # N:1 Relationship (mandatory)
    measures: Optional[List[int]] = None  # 1:N Relationship
    dataset: int  # N:1 Relationship (mandatory)

