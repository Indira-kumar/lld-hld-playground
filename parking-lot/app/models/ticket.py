from app.models.base_model import BaseModel

class Ticket(BaseModel):
    def __init__(self, ticket_id, vehicle_number, parking_spot_id):
        super().__init__(ticket_id)
        self.vehicle_number = vehicle_number
        self.spot = parking_spot_id
        self.generated_by = None
        self.entry_time = None

    def close_ticket(self):
        self.is_active = False