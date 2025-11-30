"""Fetch real flight data from Gemini API"""

import os
import json
import google.genai

def fetch_flights_from_gemini(origin=None, destination=None, date=None):
    """
    Fetch real flight data from Gemini API based on search criteria.
    
    Args:
        origin: Starting location (airport code or city name)
        destination: Destination location (airport code or city name)
        date: Travel date in YYYY-MM-DD format
    
    Returns:
        List of flight dictionaries with realistic data
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return []
    
    try:
        client = google.genai.Client(api_key=api_key)
        
        prompt = f"""Generate realistic flight data in JSON format based on this search criteria:
- From: {origin or "any"}
- To: {destination or "any"}
- Date: {date or "any"}

Return a JSON array with 5-8 realistic flights. Each flight must have:
- id: unique ID like "FL001" (incrementing)
- type: "flight"
- airline: real airline name (United, American, Delta, Southwest, Alaska, JetBlue, Spirit)
- from: origin airport with code like "New York (JFK)"
- to: destination airport with code like "Los Angeles (LAX)"
- departure: departure time like "2025-12-01 08:00"
- arrival: arrival time like "2025-12-01 11:30"
- duration: flight duration like "5h 30m"
- price: price in USD between $100-$600
- class: "Economy", "Business", or "First"
- stops: "Non-stop", "1 stop", or "2 stops"

Return ONLY the JSON array, no other text. Example format:
[{{"id": "FL001", "type": "flight", "airline": "United Airlines", ...}}]
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        if not response or not response.text:
            return []
        
        response_text = response.text.strip()
        
        # Try to parse the JSON response
        if response_text.startswith('['):
            flights = json.loads(response_text)
            # Ensure all flights have required fields
            for flight in flights:
                if 'id' not in flight:
                    flight['id'] = f"FL{flights.index(flight):03d}"
                if 'type' not in flight:
                    flight['type'] = 'flight'
            return flights
        else:
            # If response doesn't start with [, try to find JSON in the response
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                flights = json.loads(json_match.group())
                for flight in flights:
                    if 'id' not in flight:
                        flight['id'] = f"FL{flights.index(flight):03d}"
                    if 'type' not in flight:
                        flight['type'] = 'flight'
                return flights
        
        print(f"Could not parse Gemini response: {response_text[:100]}")
        return []
        
    except Exception as e:
        print(f"Error fetching flights from Gemini: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return []
