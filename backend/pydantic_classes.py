from datetime import datetime, date, time
from typing import List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator

from abc import ABC, abstractmethod

############################################
# Enumerations are defined here
############################################

class EvaluationStatus(Enum):
    Processing = "Processing"
    Done = "Done"
    Custom = "Custom"
    Archived = "Archived"
    Pending = "Pending"

class DatasetType(Enum):
    Training = "Training"
    Test = "Test"
    Validation = "Validation"

class LicensingType(Enum):
    Proprietary = "Proprietary"
    Open_Source = "Open_Source"

class ProjectStatus(Enum):
    Closed = "Closed"
    Created = "Created"
    Ready = "Ready"
    Pending = "Pending"
    Archived = "Archived"

############################################
# Classes are defined here
############################################
class CommentsCreate(BaseModel):
    Name: str
    TimeStamp: datetime
    Comments: str

class LegalRequirementCreate(BaseModel):
    standard: str
    principle: str
    legal_ref: str
    project_1: int  # N:1 Relationship (mandatory)

class ToolCreate(BaseModel):
    source: str
    version: str
    licensing: LicensingType
    name: str
    observation_1: Optional[List[int]] = None  # 1:N Relationship

class DatashapeCreate(BaseModel):
    accepted_target_values: str
    f_date: Optional[List[int]] = None  # 1:N Relationship
    dataset_1: Optional[List[int]] = None  # 1:N Relationship
    f_features: Optional[List[int]] = None  # 1:N Relationship

class ProjectCreate(BaseModel):
    status: ProjectStatus
    name: str
    involves: Optional[List[int]] = None  # 1:N Relationship
    eval: Optional[List[int]] = None  # 1:N Relationship
    legal_requirements: Optional[List[int]] = None  # 1:N Relationship

class EvaluationCreate(BaseModel):
    status: EvaluationStatus
    config: int  # N:1 Relationship (mandatory)
    evaluates: List[int]  # N:M Relationship
    observations: Optional[List[int]] = None  # 1:N Relationship
    ref: List[int]  # N:M Relationship
    project: int  # N:1 Relationship (mandatory)

class MeasureCreate(BaseModel):
    value: float
    unit: str
    error: str
    uncertainty: float
    observation: int  # N:1 Relationship (mandatory)
    metric: int  # N:1 Relationship (mandatory)
    measurand: int  # N:1 Relationship (mandatory)

class AssessmentElementCreate(ABC, BaseModel):
    description: str
    name: str

class ObservationCreate(AssessmentElementCreate):
    whenObserved: datetime
    observer: str
    eval: int  # N:1 Relationship (mandatory)
    tool: int  # N:1 Relationship (mandatory)
    measures: Optional[List[int]] = None  # 1:N Relationship
    dataset: int  # N:1 Relationship (mandatory)

class ConfParamCreate(AssessmentElementCreate):
    param_type: str
    value: str
    conf: int  # N:1 Relationship (mandatory)

class ElementCreate(AssessmentElementCreate):
    eval: List[int]  # N:M Relationship
    project: Optional[int] = None  # N:1 Relationship (optional)
    measure: Optional[List[int]] = None  # 1:N Relationship
    evalu: List[int]  # N:M Relationship

class ModelCreate(ElementCreate):
    pid: str
    licensing: LicensingType
    source: str
    data: str
    dataset: int  # N:1 Relationship (mandatory)

class FeatureCreate(ElementCreate):
    min_value: float
    max_value: float
    feature_type: str
    date: int  # N:1 Relationship (mandatory)
    features: int  # N:1 Relationship (mandatory)

class DatasetCreate(ElementCreate):
    version: str
    source: str
    dataset_type: DatasetType
    licensing: LicensingType
    models: Optional[List[int]] = None  # 1:N Relationship
    observation_2: Optional[List[int]] = None  # 1:N Relationship
    datashape: int  # N:1 Relationship (mandatory)

class ConfigurationCreate(AssessmentElementCreate):
    params: Optional[List[int]] = None  # 1:N Relationship
    eval: Optional[List[int]] = None  # 1:N Relationship

class MetricCreate(AssessmentElementCreate):
    measures: Optional[List[int]] = None  # 1:N Relationship
    derivedBy: List[int]  # N:M Relationship
    category: List[int]  # N:M Relationship

class DirectCreate(MetricCreate):
    pass

class DerivedCreate(MetricCreate):
    expression: str
    baseMetric: List[int]  # N:M Relationship

class MetricCategoryCreate(AssessmentElementCreate):
    metrics: List[int]  # N:M Relationship

