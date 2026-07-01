from pydantic import BaseModel
from typing import List


class BusinessBlueprint(BaseModel):

    business_summary: str

    entity_recommendation: str

    workforce_plan: str

    accounting_stack: List[str]

    tax_plan: List[str]

    integration_map: dict

    risk_score: int

    risk_level: str