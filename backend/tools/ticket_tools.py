"""Custom tools for the SmartTicket AI Agent"""

from typing import Dict, List, Any, Optional
from backend.tools.mock_data import search_tickets, get_ticket_by_id
from backend.tools.gemini_flights import fetch_flights_from_gemini

def search_tickets_tool(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    ticket_type: Optional[str] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for available tickets across flights, trains, buses, and movies.
    For flights, fetches real data from Gemini API.
    
    Args:
        origin: Starting location (for flights, trains, buses)
        destination: Destination location or city for movies
        ticket_type: Type of ticket (flight, train, bus, movie)
        date: Travel or show date in YYYY-MM-DD format
    
    Returns:
        Dictionary with search results and count
    """
    # For flights, fetch from Gemini API
    if ticket_type and ticket_type.lower() == 'flight':
        results = fetch_flights_from_gemini(origin, destination, date)
    else:
        # For other ticket types, use mock data
        results = search_tickets(origin, destination, ticket_type, date)
    
    return {
        "status": "success",
        "count": len(results),
        "results": results,
        "message": f"Found {len(results)} available ticket(s)"
    }


def compare_options_tool(ticket_ids: List[str]) -> Dict[str, Any]:
    """
    Compare multiple ticket options side by side.
    
    Args:
        ticket_ids: List of ticket IDs to compare
    
    Returns:
        Dictionary with comparison data
    """
    tickets = []
    for ticket_id in ticket_ids:
        ticket = get_ticket_by_id(ticket_id)
        if ticket:
            tickets.append(ticket)
    
    if not tickets:
        return {
            "status": "error",
            "message": "No valid tickets found for comparison"
        }
    
    comparison = {
        "status": "success",
        "tickets": tickets,
        "count": len(tickets),
        "price_range": {
            "min": min(t['price'] for t in tickets),
            "max": max(t['price'] for t in tickets),
            "average": sum(t['price'] for t in tickets) / len(tickets)
        }
    }
    
    return comparison


def book_ticket_tool(
    ticket_id: str,
    passenger_name: str,
    passenger_email: str,
    passenger_count: int = 1
) -> Dict[str, Any]:
    """
    Book a ticket for the user.
    
    Args:
        ticket_id: ID of the ticket to book
        passenger_name: Name of the passenger
        passenger_email: Email of the passenger
        passenger_count: Number of passengers (default: 1)
    
    Returns:
        Dictionary with booking confirmation
    """
    ticket = get_ticket_by_id(ticket_id)
    
    if not ticket:
        return {
            "status": "error",
            "message": "Ticket not found"
        }
    
    total_price = ticket['price'] * passenger_count
    booking_reference = f"BK{ticket_id}{passenger_count:02d}"
    
    booking = {
        "status": "success",
        "booking_reference": booking_reference,
        "ticket": ticket,
        "passenger_name": passenger_name,
        "passenger_email": passenger_email,
        "passenger_count": passenger_count,
        "total_price": total_price,
        "message": f"Booking confirmed! Reference: {booking_reference}"
    }
    
    return booking


def send_confirmation_tool(
    booking_reference: str,
    passenger_email: str,
    booking_details: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Send booking confirmation to the passenger.
    
    Args:
        booking_reference: Unique booking reference number
        passenger_email: Email to send confirmation to
        booking_details: Complete booking information
    
    Returns:
        Dictionary with confirmation status
    """
    confirmation = {
        "status": "success",
        "booking_reference": booking_reference,
        "email_sent_to": passenger_email,
        "message": f"Confirmation email sent to {passenger_email}",
        "booking_summary": {
            "reference": booking_reference,
            "total_price": booking_details.get('total_price', 0),
            "ticket_type": booking_details.get('ticket', {}).get('type', 'N/A')
        }
    }
    
    return confirmation
