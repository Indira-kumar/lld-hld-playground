from app.models.base_model import BaseModel
from app.models.spot_availability_status import SpotAvailabilityStatus

class Spot(BaseModel):
    def __init__(self, spot_id, spot_type: SpotAvailabilityStatus):
        super().__init__(spot_id)
        self.spot_type = spot_type
        self.is_occupied = False