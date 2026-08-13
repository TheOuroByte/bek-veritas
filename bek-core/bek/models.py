from pydantic import BaseModel, Field
from typing import List, Dict, Set, Optional

class SROTriple(BaseModel):
    """The fundamental unit of semantic reality."""
    subject: str = Field(..., description="The entity acting")
    relation: str = Field(..., description="The action/state")
    object: str = Field(..., description="The entity being acted upon")

class KnowledgeConstraint(BaseModel):
    """A thermodynamic law governing the hypergraph."""
    subjects: Set[str]
    relations: Set[str]
    objects: Set[str]

class VeritasResult(BaseModel):
    """The thermodynamic autopsy of a single claim."""
    triple: SROTriple
    verdict: str
    bravo_score: float
    operator_signature: str
    remaining_hypotheses: Dict[str, List[str]]

class FieldResult(BaseModel):
    """The geometric mean analysis of a multi-claim document."""
    field_score: float
    verdict: str
    pool_results: List[VeritasResult]
    ipfc: float = Field(default=1.0, description="Inter-pool Fibonacci coherence.")
