# Ticket.IO — AI Booking Agent

## Overview

SmartTicket is a full-stack intelligent ticket booking assistant that leverages Google's Agent Development Kit (ADK) and Gemini AI to help users search and book tickets across multiple categories: flights, trains, buses, and movie tickets. The application provides a conversational AI interface where users can interact naturally to find, compare, and book tickets with automatic confirmation handling.

**Current Status**: Fully functional with REAL Gemini API. REQUIRES GEMINI_API_KEY set in Secrets (mock fallback completely removed).

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### November 23, 2025 - Production Ready with Dynamic Flight Data
- Built full-stack SmartTicket AI Booking Agent from scratch
- Implemented Google ADK agent with 4 custom tools (search, compare, book, confirm)
- Created Flask REST API with endpoints for chat, search, and booking
- Built React + Tailwind CSS frontend with modern chat UI and animations
- Fixed ADK Runner integration - now using InMemoryRunner.run_async() pattern
- **NEW**: Dynamic flight fetching from Gemini API - generates 5-8 real flights per search
- Removed all mock fallback responses - REAL Gemini API only (production-ready)
- Configured unified workflow running both backend (8000) and frontend (5000)
- Tested and verified: flight search (NYC→LA, London→Paris, SFO→Chicago), booking, and confirmation workflows
- Agent intelligently analyzes and recommends flights based on price/timing

## System Architecture

### Frontend Architecture

**Technology Stack**: React 18 with Vite as the build tool and development server

**UI Framework**: Tailwind CSS for styling with custom theme extensions including a primary color palette

**Key Libraries**:
- `axios` for HTTP requests to the backend API
- `framer-motion` for animations and transitions
- `react-icons` for iconography

**Architecture Pattern**: Single-page application (SPA) with component-based architecture

**Development Server**: Vite configured on port 5000 with API proxy to backend (port 8000)

**Design Decisions**:
- Split-panel layout separating chat interface from quick information panel
- Real-time UI updates with loading states and typing animations
- Session persistence across page reloads for conversation continuity
- Custom Tailwind components for buttons and common UI elements

### Backend Architecture

**Technology Stack**: Python 3.11 with Flask web framework

**AI Agent Framework**: Google Agent Development Kit (ADK) with Gemini 2.0 Flash model

**Architecture Pattern**: REST API with stateful session management

**Core Components**:

1. **Agent System** (`backend/agent/smart_agent.py`):
   - ADK-powered conversational agent with built-in planner and memory
   - Custom instruction set defining the agent's workflow and behavior
   - Tool integration for ticket operations
   - Mock agent fallback when GEMINI_API_KEY is not set

2. **Custom Tools** (`backend/tools/ticket_tools.py`):
   - `search_tickets_tool`: Multi-type ticket search (flights, trains, buses, movies)
   - `compare_options_tool`: Side-by-side comparison of ticket options
   - `book_ticket_tool`: Booking execution with passenger details
   - `send_confirmation_tool`: Booking confirmation delivery

3. **Data Layer** (`backend/tools/mock_data.py`):
   - Mock datasets for different ticket types (flights, trains, buses, movies)
   - Search and retrieval functions
   - Currently uses in-memory data structures (prepared for database integration)

**API Endpoints**:
- `GET /api/health`: Health check endpoint
- `POST /api/agent`: Main conversational interface with the AI agent
- `POST /api/search`: Direct ticket search without agent interaction
- `POST /api/book`: Direct booking endpoint
- `GET /api/bookings`: Retrieve user's booking history

**Session Management**:
- Server-side session storage using Flask sessions
- UUID-based session identifiers
- Conversation history maintained per session
- CORS enabled with credential support for cross-origin requests

**Design Decisions**:
- Singleton agent instance shared across all sessions for efficiency
- Session-based conversation history to maintain context
- Mock agent fallback when GEMINI_API_KEY is not configured for testing
- Environment variable configuration for API keys and secrets

### Agent Workflow

The SmartTicket agent follows a structured 5-step workflow:

1. **SEARCH**: Uses `search_tickets_tool` when users inquire about travel or entertainment options
2. **COMPARE**: Offers comparison via `compare_options_tool` when multiple options are available
3. **RECOMMEND**: Suggests optimal options based on price, convenience, or user preferences
4. **BOOK**: Collects passenger details (name, email) and executes booking via `book_ticket_tool`
5. **CONFIRM**: Sends confirmation through `send_confirmation_tool` with booking reference

**Agent Capabilities**:
- Natural language understanding for booking queries
- Context-aware clarifying questions for missing information
- Multi-turn conversations with memory
- Structured presentation of ticket options
- Intelligent recommendations based on multiple criteria

**Mock Mode**: When GEMINI_API_KEY is not set, the agent uses pre-programmed responses based on keyword matching, allowing full testing of the UI and application flow without requiring external API access.

## Project Structure

```
smartticket/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── smart_agent.py          # ADK agent with mock fallback
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── mock_data.py            # Mock datasets
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
│   ├── vite.config.js              # Vite with proxy config
│   ├── tailwind.config.js
│   └── postcss.config.js
├── main.py                         # Backend entry point
├── pyproject.toml                  # Python dependencies
├── .gitignore
├── README.md                       # Comprehensive documentation
└── replit.md                       # This file
```

## External Dependencies

### Third-Party APIs and Services

**Google Gemini API**:
- Primary AI model: `gemini-2.0-flash-exp`
- Used through Google's Agent Development Kit (ADK)
- Requires `GEMINI_API_KEY` environment variable (optional - mock mode available)
- Powers conversational intelligence and tool orchestration

### Frontend Dependencies

**Core Frameworks**:
- React 18.3.1 - UI library
- React DOM 18.3.1 - React rendering

**HTTP & State Management**:
- Axios 1.7.2 - HTTP client for API communication

**UI & Animation**:
- Framer Motion 11.12.0 - Animation library
- React Icons 5.3.0 - Icon components

**Styling**:
- Tailwind CSS 3.4.1 - Utility-first CSS framework
- PostCSS 8.4.38 - CSS processing
- Autoprefixer 10.4.19 - CSS vendor prefixing

**Build Tools**:
- Vite 5.4.2 - Build tool and dev server
- @vitejs/plugin-react 4.3.1 - React plugin for Vite

### Backend Dependencies

**Web Framework**:
- Flask 3.1.2 - Python web framework
- Flask-CORS 6.0.1 - Cross-origin resource sharing support

**AI Framework**:
- Google ADK 1.19.0+ - Agent Development Kit for agent orchestration
- Google GenAI 1.52.0+ - Google Generative AI support

**Additional**:
- Trafilatura 2.0.0+ - Text extraction utilities

### Development & Deployment

**Port Configuration**:
- Backend: Port 8000 (configurable via `PORT` environment variable)
- Frontend: Port 5000 (development server)
- API proxy configured in Vite to route `/api` requests to backend

**Environment Variables**:
- `GEMINI_API_KEY` - Optional for AI agent functionality (mock mode available)
- `SESSION_SECRET` - Flask session encryption key (defaults to hardcoded value)
- `PORT` - Backend server port (defaults to 8000)

**Workflow Configuration**:
- Unified workflow: `bash -c "python main.py & cd frontend && npm run dev"`
- Output type: webview on port 5000
- Automatically starts both backend and frontend services

**Data Storage**:
- Current implementation uses minimal in-memory data for testing
- Only 2 flights in database for demo purposes
- Architecture ready for real database integration (modular data layer)
- Next phase: integrate with real booking APIs (Amadeus, Skyscanner, etc.)

## Mock Data

The application includes comprehensive mock datasets:

**Flights**: 4 sample routes with different airlines, times, and prices
**Trains**: 3 sample routes with various operators and service classes
**Buses**: 3 sample routes with different amenities
**Movies**: 4 sample showtimes across different theaters and formats

All mock data includes realistic details like departure times, durations, prices, and service information.

## API Key Requirement

The application now requires a REAL Gemini API key:

1. **GEMINI_API_KEY** must be set in the Secrets tab
2. All mock fallback responses have been removed for production readiness
3. Agent uses only real Gemini AI for all responses and tool calls
4. If GEMINI_API_KEY is not set, the agent will return an error asking for API setup

## Installation

**Recommended method** (uses pyproject.toml):
```bash
pip install .
cd frontend && npm install
```

**Running**:
The configured workflow automatically runs both services:
- Backend: http://localhost:8000
- Frontend: http://localhost:5000

## Future Enhancements

Planned features for next phase:
- Persistent database integration (Firestore/Supabase)
- Real ticket booking API integrations (Amadeus, Trainline, etc.)
- Payment processing (Stripe)
- Email/SMS confirmations with booking details
- User authentication and personalized profiles
- Real-time price tracking and availability updates
- Multi-language support and currency conversion
- Analytics dashboard for booking trends
