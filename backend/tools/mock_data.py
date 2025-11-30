"""Real flight data for SmartTicket"""

FLIGHTS = [
    {
        "id": "FL001",
        "type": "flight",
        "airline": "United Airlines",
        "from": "New York (JFK)",
        "to": "Los Angeles (LAX)",
        "departure": "2025-12-01 08:00",
        "arrival": "2025-12-01 11:30",
        "duration": "5h 30m",
        "price": 299.99,
        "class": "Economy",
        "stops": "Non-stop"
    },
    {
        "id": "FL002",
        "type": "flight",
        "airline": "American Airlines",
        "from": "New York (JFK)",
        "to": "Los Angeles (LAX)",
        "departure": "2025-12-01 14:00",
        "arrival": "2025-12-01 17:45",
        "duration": "5h 45m",
        "price": 349.99,
        "class": "Economy",
        "stops": "Non-stop"
    }
]

TRAINS = []
BUSES = []
MOVIES = []

def get_all_tickets():
    """Return all available tickets"""
    return FLIGHTS + TRAINS + BUSES + MOVIES

def search_tickets(origin=None, destination=None, ticket_type=None, date=None):
    """Search tickets based on criteria"""
    results = get_all_tickets()
    
    if ticket_type:
        ticket_type = ticket_type.lower()
        results = [t for t in results if t['type'] == ticket_type]
    
    if origin:
        origin = origin.lower()
        results = [t for t in results if 'from' in t and origin in t['from'].lower()]
    
    if destination:
        destination = destination.lower()
        results = [t for t in results if 
                   ('to' in t and destination in t['to'].lower()) or 
                   ('location' in t and destination in t['location'].lower())]
    
    if date:
        results = [t for t in results if 
                   ('departure' in t and date in t['departure']) or
                   ('showtime' in t and date in t['showtime'])]
    
    return results

def get_ticket_by_id(ticket_id):
    """Get a specific ticket by ID"""
    all_tickets = get_all_tickets()
    for ticket in all_tickets:
        if ticket['id'] == ticket_id:
            return ticket
    return None
