from pydantic import BaseModel
from typing import Dict, Optional

class StatisticsResponse(BaseModel):
    total_incidents: int
    by_severity: Dict[str, int]
    by_category: Dict[str, int]
    average_downtime: Optional[float] = None