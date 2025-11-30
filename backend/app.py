"""Flask backend for SmartTicket AI Agent"""

import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from backend.agent import create_smart_ticket_agent, run_agent_conversation
from backend.tools.mock_data import search_tickets, get_ticket_by_id
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'smartticket-secret-key-12345')

CORS(app, supports_credentials=True)

agent_and_runner = None
user_sessions = {}

def get_agent():
    """Get or create the ADK agent instance"""
    global agent_and_runner
    if agent_and_runner is None:
        agent_and_runner = create_smart_ticket_agent()
    return agent_and_runner


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'SmartTicket AI Agent'})


@app.route('/api/agent', methods=['POST'])
def chat_with_agent():
    """
    Main endpoint for conversing with the AI agent.
    
    Expects JSON: { "message": "user message", "session_id": "optional-session-id" }
    Returns: { "response": "agent response", "session_id": "session-id", "history": [...] }
    """
    try:
        data = request.json or {}
        user_message = data.get('message', '')
        session_id = data.get('session_id') or str(uuid.uuid4())
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'history': [],
                'bookings': []
            }
        
        session_data = user_sessions[session_id]
        
        agent_instance = get_agent()
        
        result = run_agent_conversation(
            agent_instance,
            user_message,
            session_data['history'],
            session_id=session_id
        )
        
        session_data['history'] = result['history']
        
        if result.get('error'):
            return jsonify({
                'success': False,
                'response': result['message'],
                'session_id': session_id,
                'error': result['message']
            }), 400
        
        return jsonify({
            'success': result['success'],
            'response': result['message'],
            'session_id': session_id,
            'message_count': len(session_data['history'])
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'response': str(e)
        }), 500


@app.route('/api/search', methods=['POST'])
def search_tickets_endpoint():
    """
    Direct search endpoint for tickets.
    
    Expects JSON: { "origin": "...", "destination": "...", "type": "...", "date": "..." }
    Returns: { "results": [...], "count": N }
    """
    try:
        data = request.json or {}
        origin = data.get('origin')
        destination = data.get('destination')
        ticket_type = data.get('type')
        date = data.get('date')
        
        results = search_tickets(origin, destination, ticket_type, date)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/book', methods=['POST'])
def book_ticket_endpoint():
    """
    Direct booking endpoint.
    
    Expects JSON: {
        "ticket_id": "...",
        "passenger_name": "...",
        "passenger_email": "...",
        "passenger_count": N,
        "session_id": "..."
    }
    Returns: { "booking": {...}, "reference": "..." }
    """
    try:
        data = request.json or {}
        ticket_id = data.get('ticket_id')
        passenger_name = data.get('passenger_name')
        passenger_email = data.get('passenger_email')
        passenger_count = data.get('passenger_count', 1)
        session_id = data.get('session_id')
        
        if not all([ticket_id, passenger_name, passenger_email]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        ticket = get_ticket_by_id(ticket_id)
        if not ticket:
            return jsonify({
                'success': False,
                'error': 'Ticket not found'
            }), 404
        
        total_price = ticket['price'] * passenger_count
        booking_reference = f"BK{ticket_id}{passenger_count:02d}"
        
        booking = {
            'booking_reference': booking_reference,
            'ticket': ticket,
            'passenger_name': passenger_name,
            'passenger_email': passenger_email,
            'passenger_count': passenger_count,
            'total_price': total_price
        }
        
        if session_id and session_id in user_sessions:
            user_sessions[session_id]['bookings'].append(booking)
        
        return jsonify({
            'success': True,
            'booking': booking,
            'reference': booking_reference
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """
    Get booking history for a session.
    
    Query param: session_id
    Returns: { "bookings": [...] }
    """
    session_id = request.args.get('session_id')
    
    if not session_id or session_id not in user_sessions:
        return jsonify({
            'success': True,
            'bookings': []
        })
    
    return jsonify({
        'success': True,
        'bookings': user_sessions[session_id]['bookings']
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
