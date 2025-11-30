"""Main entry point for SmartTicket Backend"""

import os
os.environ.setdefault('GEMINI_API_KEY', os.environ.get('GEMINI_API_KEY', ''))

from backend.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting SmartTicket Backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
