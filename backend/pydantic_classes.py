from datetime import datetime, date, time
from typing import List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator

from abc import ABC, abstractmethod

############################################
# Enumerations are defined here
############################################

class EvaluationStatus(Enum):
    Custom = "Custom"
    Processing = "Processing"
    Done = "Done"
    Pending = "Pending"
    Archived = "Archived"

class ProjectStatus(Enum):
    Pending = "Pending"
    Created = "Created"
    Closed = "Closed"
    Ready = "Ready"
    Archived = "Archived"

class LicensingType(Enum):
    Proprietary = "Proprietary"
    Open_Source = "Open_Source"

class DatasetType(Enum):
    Validation = "Validation"
    Training = "Training"
    Test = "Test"

############################################
# Classes are defined here
############################################
class EvaluationCreate(BaseModel):
    status: EvaluationStatus
    observations: Optional[List[int]] = None  # 1:N Relationship
    evaluates: List[int]  # N:M Relationship
    ref: List[int]  # N:M Relationship
    config: int  # N:1 Relationship (mandatory)
    project: int  # N:1 Relationship (mandatory)

class MeasureCreate(BaseModel):
    uncertainty: float
    value: float
    error: str
    unit: str
    measurand: int  # N:1 Relationship (mandatory)
    metric: int  # N:1 Relationship (mandatory)
    observation: int  # N:1 Relationship (mandatory)

class AssessmentElementCreate(ABC, BaseModel):
    name: str
    description: str

class ObservationCreate(AssessmentElementCreate):
    whenObserved: datetime
    observer: str
    tool: int  # N:1 Relationship (mandatory)
    eval: int  # N:1 Relationship (mandatory)
    dataset: int  # N:1 Relationship (mandatory)
    measures: Optional[List[int]] = None  # 1:N Relationship

class ElementCreate(AssessmentElementCreate):
    measure: Optional[List[int]] = None  # 1:N Relationship
    project: Optional[int] = None  # N:1 Relationship (optional)
    evalu: List[int]  # N:M Relationship
    eval: List[int]  # N:M Relationship

class MetricCreate(AssessmentElementCreate):
    category: List[int]  # N:M Relationship
    measures: Optional[List[int]] = None  # 1:N Relationship
    derivedBy: List[int]  # N:M Relationship

class DirectCreate(MetricCreate):
    pass

class CommentsCreate(BaseModel):
    TimeStamp: datetime
    Comments: str
    Name: str

class MetricCategoryCreate(AssessmentElementCreate):
    metrics: List[int]  # N:M Relationship

class LegalRequirementCreate(BaseModel):
    legal_ref: str
    principle: str
    standard: str
    project_1: int  # N:1 Relationship (mandatory)

class ToolCreate(BaseModel):
    version: str
    licensing: LicensingType
    source: str
    name: str
    observation_1: Optional[List[int]] = None  # 1:N Relationship

class ConfParamCreate(AssessmentElementCreate):
    param_type: str
    value: str
    conf: int  # N:1 Relationship (mandatory)

class ConfigurationCreate(AssessmentElementCreate):
    params: Optional[List[int]] = None  # 1:N Relationship
    eval: Optional[List[int]] = None  # 1:N Relationship

class FeatureCreate(ElementCreate):
    min_value: float
    max_value: float
    feature_type: str
    features: int  # N:1 Relationship (mandatory)
    date: int  # N:1 Relationship (mandatory)

class DatashapeCreate(BaseModel):
    accepted_target_values: str
    f_features: Optional[List[int]] = None  # 1:N Relationship
    dataset_1: Optional[List[int]] = None  # 1:N Relationship
    f_date: Optional[List[int]] = None  # 1:N Relationship

class DatasetCreate(ElementCreate):
    licensing: LicensingType
    version: str
    source: str
    dataset_type: DatasetType
    datashape: int  # N:1 Relationship (mandatory)
    observation_2: Optional[List[int]] = None  # 1:N Relationship
    models: Optional[List[int]] = None  # 1:N Relationship

class ProjectCreate(BaseModel):
    status: ProjectStatus
    name: str
    legal_requirements: Optional[List[int]] = None  # 1:N Relationship
    involves: Optional[List[int]] = None  # 1:N Relationship
    eval: Optional[List[int]] = None  # 1:N Relationship

class ModelCreate(ElementCreate):
    data: str
    source: str
    pid: str
    licensing: LicensingType
    dataset: int  # N:1 Relationship (mandatory)

class DerivedCreate(MetricCreate):
    expression: str
    baseMetric: List[int]  # N:M Relationship

