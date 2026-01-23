"""Fetch real flight data from Gemini API"""

import os
import json
import re

try:
    import google.genai  # type: ignore
except ImportError:  # pragma: no cover
    google = None


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
        print("No api key")
        return []

    if google is None or not hasattr(google, "genai") or not hasattr(google.genai, "Client"):
        print("Error fetching flights from Gemini.")  # Fixed: do not log exception details
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
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        if not response or not getattr(response, "text", None):
            return []

        response_text = response.text.strip()

        flights = None

        # Try to parse the JSON response
        if response_text.startswith('['):
            try:
                flights = json.loads(response_text)
            except Exception:
                flights = None

        if flights is None:
            # If response doesn't start with [, try to find JSON in the response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                try:
                    flights = json.loads(json_match.group())
                except Exception:
                    flights = None

        if isinstance(flights, list):
            # Ensure all flights have required fields
            for idx, flight in enumerate(flights):
                if isinstance(flight, dict):
                    if 'id' not in flight:
                        flight['id'] = f"FL{idx:03d}"
                    if 'type' not in flight:
                        flight['type'] = 'flight'
            return flights

        # 🔒 VOTAL.AI Security Fix: Verbose exception and response logging may leak sensitive information [CWE-532] - LOW
        print("Could not parse Gemini response.")  # Fixed: do not log sensitive response data
        return []

    except Exception:
        print("Error fetching flights from Gemini.")  # Fixed: do not log exception details
        return []