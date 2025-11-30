# SmartTicket — AI Booking Agent

A full-stack intelligent ticket booking assistant powered by Google's Agent Development Kit (ADK) and Gemini AI. SmartTicket helps users find and book flights, trains, buses, and movie tickets through natural conversation.

## Architecture

### Backend (Python + Flask + Google ADK)
- **Agent System**: ADK-powered conversational agent with planner, memory, and context management
- **Custom Tools**: 
  - `searchTicketsTool`: Search across multiple ticket types (flights, trains, buses, movies)
  - `compareOptionsTool`: Compare ticket options side-by-side
  - `bookTicketTool`: Book selected tickets with passenger details
  - `sendConfirmationTool`: Send booking confirmations

- **REST API Endpoints**:
  - `POST /api/agent`: Main chat interface with the AI agent
  - `POST /api/search`: Direct ticket search
  - `POST /api/book`: Direct booking endpoint
  - `GET /api/bookings`: Retrieve booking history

### Frontend (React + Tailwind CSS + Vite)
- **Modern Chat UI**: Clean, responsive chat interface with typing animations
- **Split-Panel Layout**: Chat on the left, quick info panel on the right
- **Real-time Updates**: Smooth transitions and loading states
- **Session Management**: Persistent sessions across page reloads

## Project Structure

```
smartticket/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── smart_agent.py          # ADK agent configuration
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── mock_data.py            # Mock datasets for tickets
│   │   └── ticket_tools.py         # Custom tool implementations
│   ├── __init__.py
│   └── app.py                      # Flask REST API
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main React component
│   │   ├── main.jsx                # React entry point
│   │   └── index.css               # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js              # Vite configuration with proxy
│   ├── tailwind.config.js
│   └── postcss.config.js
├── main.py                         # Backend entry point
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 20+
- Google Gemini API Key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd smartticket
```

2. **Backend Setup**
```bash
# Install Python dependencies from pyproject.toml (recommended)
pip install .

# Alternative: Install manually
# pip install google-adk flask flask-cors google-genai

# Set environment variables (optional for testing with mock mode)
export GEMINI_API_KEY="your-gemini-api-key"  # Get from https://ai.google.dev/
export SESSION_SECRET="your-secret-key"

# Note: The app works without GEMINI_API_KEY using a mock agent for testing
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

### Running the Application

The application uses a unified workflow that runs both backend and frontend:

```bash
# From the root directory
python main.py &
cd frontend && npm run dev
```

Or use the configured   workflow that starts both services automatically.

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5000

## Features

### Intelligent Booking Workflow
1. **Search**: Users describe their travel or entertainment needs
2. **Compare**: Agent presents multiple options with key details
3. **Recommend**: Suggests best option based on price, convenience
4. **Book**: Collects passenger details and confirms booking
5. **Confirm**: Provides booking reference and confirmation

### Multi-Service Support
- **Flights**: Domestic and international flight bookings
- **Trains**: Train ticket reservations
- **Buses**: Bus ticket bookings
- **Movies**: Movie ticket purchases with showtime selection

### AI-Powered Features
- Natural language understanding
- Context-aware conversations
- Multi-turn dialogue support
- Session memory for personalized experience
- Intelligent price comparisons

## Mock Data

The application includes realistic mock datasets for:
- Multiple airlines, train operators, and bus services
- Various routes and schedules
- Different price points and service classes
- Movie theaters with multiple showtimes

## Technology Stack

**Backend:**
- Python 3.11
- Flask (REST API framework)
- Google ADK (Agent Development Kit)
- Gemini 2.0 Flash (LLM model)
- Flask-CORS (Cross-origin support)

**Frontend:**
- React 18
- Tailwind CSS (Styling)
- Vite (Build tool)
- Framer Motion (Animations)
- Axios (HTTP client)
- React Icons

## API Usage Examples

### Chat with Agent
```bash
curl -X POST http://localhost:8000/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a flight from New York to Los Angeles on December 1st",
    "session_id": "optional-session-id"
  }'
```

### Direct Search
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New York",
    "destination": "Los Angeles",
    "type": "flight",
    "date": "2025-12-01"
  }'
```

## Future Enhancements

### Phase 2 (Planned)
- Persistent database integration (Firestore/Supabase)
- Real ticket booking API integrations
- Payment processing (Stripe)
- Email/SMS confirmations
- User authentication
- Booking history and user profiles
- Real-time price tracking
- Multi-language support
- Analytics dashboard

## Development

### Adding New Ticket Types
1. Add mock data to `backend/tools/mock_data.py`
2. Update search filters in `search_tickets()` function
3. Update frontend icons and UI in `App.jsx`

### Extending the Agent
1. Create new tool functions in `backend/tools/ticket_tools.py`
2. Register tools in `backend/agent/smart_agent.py`
3. Update agent instructions for new capabilities

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key from https://ai.google.dev/ | No (mock mode available) |
| `SESSION_SECRET` | Flask session secret | No (default provided) |
| `PORT` | Backend port | No (default: 8000) |

**Mock Mode**: If `GEMINI_API_KEY` is not set, the application runs in mock mode with pre-programmed responses. This allows you to test the UI and application flow without requiring an API key. Set the key for real AI-powered conversations.

## License

MIT License - Feel free to use this project as a learning resource or starting point for your own AI agent applications.

## Acknowledgments

- Built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
- Powered by [Gemini AI](https://ai.google.dev/)
- UI inspired by modern chat applications

---

**Note**: This is a demonstration project using mock data. For production use, integrate with real ticket booking APIs and implement proper authentication, payment processing, and data persistence.
