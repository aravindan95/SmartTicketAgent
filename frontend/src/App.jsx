import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FaPaperPlane, FaPlane, FaTrain, FaBus, FaFilm, FaRobot } from 'react-icons/fa'
import axios from 'axios'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    const storedSessionId = localStorage.getItem('ticketio_session')
    if (storedSessionId) {
      setSessionId(storedSessionId)
    }
    
    setMessages([{
      role: 'assistant',
      content: 'Hello! I\'m Ticket.IO, your AI booking assistant. I can help you find and book flights, trains, buses, and movie tickets. What would you like to book today?'
    }])
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)
    setIsTyping(true)

    try {
      const response = await axios.post('/api/agent', {
        message: userMessage,
        session_id: sessionId
      })

      if (response.data.success) {
        const newSessionId = response.data.session_id
        if (!sessionId) {
          setSessionId(newSessionId)
          localStorage.setItem('ticketio_session', newSessionId)
        }

        setTimeout(() => {
          setMessages(prev => [...prev, {
            role: 'assistant',
            content: response.data.response
          }])
          setIsTyping(false)
        }, 500)
      } else {
        throw new Error(response.data.error || 'Failed to get response')
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
      setIsTyping(false)
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuickReply = (reply) => {
    setInput(reply)
    setTimeout(() => {
      const form = document.querySelector('form')
      if (form) form.dispatchEvent(new Event('submit', { bubbles: true }))
    }, 50)
  }

  const getQuickReplies = (lastMessage) => {
    if (!lastMessage) return []
    
    const text = lastMessage.toLowerCase()
    if (text.includes('book') || text.includes('what would you like')) {
      return [
        'Find flights to LA',
        'Show me trains',
        'Bus tickets',
        'Movie tickets'
      ]
    }
    if (text.includes('flight')) {
      return [
        'Find cheaper options',
        'Show alternative dates',
        'Compare airlines',
        'Book this flight'
      ]
    }
    if (text.includes('compare')) {
      return [
        'I prefer the cheapest',
        'Show direct flights',
        'Book the best option',
        'Tell me more'
      ]
    }
    return []
  }

  const lastMessage = messages.length > 0 ? messages[messages.length - 1].content : ''
  const quickReplies = getQuickReplies(lastMessage)

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Minimal Top Bar */}
      <header className="border-b border-gray-200 bg-white sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white shadow-sm">
            <FaRobot className="text-lg" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-gray-900">Ticket Assistant</h1>
            <p className="text-xs text-gray-500">AI Booking Agent</p>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto w-full px-4 py-6 space-y-5">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.25 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex gap-3 max-w-xs ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  {/* Avatar */}
                  {message.role === 'assistant' && (
                    <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0 mt-1">
                      <FaRobot className="text-sm text-gray-600" />
                    </div>
                  )}
                  
                  {/* Message Bubble */}
                  <div
                    className={`px-4 py-3 rounded-2xl leading-relaxed text-sm ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white rounded-br-md'
                        : 'bg-gray-100 text-gray-900 rounded-bl-md'
                    }`}
                  >
                    <p className="whitespace-pre-wrap break-words">{message.content}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0 mt-1">
                  <FaRobot className="text-sm text-gray-600" />
                </div>
                <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3 flex gap-1.5">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Quick Reply Buttons */}
          {!isTyping && !isLoading && quickReplies.length > 0 && messages.length > 0 && messages[messages.length - 1].role === 'assistant' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="flex gap-2 flex-wrap mt-4 ml-11"
            >
              {quickReplies.map((reply, idx) => (
                <motion.button
                  key={idx}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleQuickReply(reply)}
                  className="px-3 py-1.5 text-xs bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 rounded-full border border-gray-200 hover:border-blue-300 transition-all duration-200 font-medium"
                >
                  {reply}
                </motion.button>
              ))}
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Message Input Bar */}
      <div className="border-t border-gray-200 bg-white sticky bottom-0">
        <div className="max-w-3xl mx-auto px-4 py-4">
          <form onSubmit={sendMessage} className="flex gap-2 items-end">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about flights, trains, buses, or movies..."
              className="flex-1 px-4 py-3 bg-gray-100 border-0 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm placeholder-gray-500"
              disabled={isLoading}
            />
            <motion.button
              type="submit"
              disabled={isLoading || !input.trim()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center justify-center flex-shrink-0 shadow-sm"
            >
              <FaPaperPlane className="text-sm" />
            </motion.button>
          </form>
          <p className="text-center text-xs text-gray-400 mt-3">
            Powered by Google ADK & Gemini AI
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
