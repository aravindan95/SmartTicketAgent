"""SmartTicket AI Agent using Google ADK"""

import os
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
from backend.tools import (
    search_tickets_tool,
    compare_options_tool,
    book_ticket_tool,
    send_confirmation_tool
)

# Global runner instance
_runner = None

def create_smart_ticket_agent():
    """
    Create and configure the SmartTicket AI Agent with custom tools.
    
    Returns:
        tuple: (Agent, Runner) or (None, None) for real API mode
    """
    global _runner
    
    agent_instruction = """You are SmartTicket, an intelligent booking assistant that helps users find and book tickets for flights, trains, buses, and movies.

Your workflow:
1. SEARCH: When users ask about travel or entertainment, use search_tickets_tool to find available options
2. COMPARE: If multiple options exist, offer to compare them using compare_options_tool
3. RECOMMEND: Suggest the best option based on price, convenience, or user preferences
4. BOOK: Once user chooses, collect passenger details (name, email) and book using book_ticket_tool
5. CONFIRM: Send confirmation using send_confirmation_tool

Guidelines:
- Be friendly, helpful, and conversational
- Ask clarifying questions if details are missing (origin, destination, date, passenger count)
- Present options clearly with key details (price, time, duration)
- Highlight the best value or fastest option
- Always confirm booking details before finalizing
- After booking, provide the booking reference number

Available ticket types: flight, train, bus, movie
Date format: YYYY-MM-DD (e.g., 2025-12-01)
"""
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: GEMINI_API_KEY is required. Please set it in the Secrets tab.")
        return None, None
    
    try:
        agent = Agent(
            model='gemini-2.0-flash',
            name='smart_ticket_agent',
            description='AI-powered ticket booking assistant for flights, trains, buses, and movies',
            instruction=agent_instruction,
            tools=[
                search_tickets_tool,
                compare_options_tool,
                book_ticket_tool,
                send_confirmation_tool
            ]
        )
        
        runner = InMemoryRunner(agent=agent, app_name="smartticket")
        _runner = runner
        print("✓ SmartTicket Agent successfully initialized with Gemini API (REAL API - NO MOCK)")
        return agent, runner
    except Exception as e:
        print(f"ERROR creating agent: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None, None


def run_agent_conversation(agent_and_runner, user_message, session_history=None, session_id=None):
    """
    Run a conversation turn with the agent using REAL Gemini API only.
    
    Args:
        agent_and_runner: tuple of (agent, runner) or (None, None)
        user_message: User's message
        session_history: Optional conversation history
        session_id: Session ID for the runner
    
    Returns:
        dict: Agent response with message
    """
    if session_history is None:
        session_history = []
    
    session_history.append({
        'role': 'user',
        'content': user_message
    })
    
    agent, runner = agent_and_runner if isinstance(agent_and_runner, tuple) else (agent_and_runner, None)
    
    if agent is None or runner is None:
        raise Exception("Agent not initialized. GEMINI_API_KEY is required.")
    
    async def get_agent_response():
        if session_id is None:
            raise Exception("Session ID is required")
        
        # Ensure session exists
        try:
            await runner.session_service.create_session(
                app_name="smartticket",
                user_id="default_user",
                session_id=session_id
            )
        except:
            pass  # Session might already exist
        
        final_response = None
        async for event in runner.run_async(
            user_id="default_user",
            session_id=session_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
        
        return final_response
    
    try:
        response = asyncio.run(get_agent_response())
        
        if response:
            agent_message = response
        else:
            raise Exception("Agent returned empty response")
        
        session_history.append({
            'role': 'assistant',
            'content': agent_message
        })
        
        return {
            'success': True,
            'message': agent_message,
            'history': session_history
        }
    
    except Exception as e:
        print(f"Agent error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        return {
            'success': False,
            'message': f'Error: {str(e)}',
            'history': session_history,
            'error': True
        }
