# Parking Lot

## Requirements
- can have multiple floors
- can have multiple entry and exit gates
- each floor can have multiple spots
- at entry, a ticket is to be provided, and at exit, a fare shall be collected
- vehicles can be of different types (small, medium, large)
- spot for vehicle can also be different sizes
- the cost is based on type of vehicle, time taken, but there can be other ways as well in future
- when a ticket is issued, it has a parking lot assigned
- a vehicle can be parked only its spot size
- if parking cant be given due to limit etc, a display will say not available on the cars entry
- payment can be online (UPI, card, net banking) or cash. In this case, you can assume you use 3rd party services for payment
- no monthly passes etc for now, no max time for now
- A person goes to the exit gate, gets a bill, and thats how its paid
- unless told, always assume, the behaviour can change, like price calculation can change in future etc,. So dont hardcode them
- a spot can be there for electric vehicles, and the cost there is calculated by electricity used also.