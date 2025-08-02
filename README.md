# 🐢 AlduinoBot - Your AI Companion

A multi-personality chatbot built with Python, Streamlit, and Groq's LLM API. AlduinoBot features three distinct personalities, memory capabilities, and an intuitive web interface for seamless interaction.

## 🤖 How AlduinoBot Works

### Core Architecture
AlduinoBot is built on a modular architecture with the following key components:

- **Base Chatbot Class**: Provides core functionality including message handling, memory management, and LLM integration
- **Personality System**: Three specialized bot classes that inherit from the base class, each with unique behavioral patterns
- **Memory System**: Stores conversation history, user preferences, and remembered facts for context-aware responses
- **Web Interface**: Streamlit-based UI for easy interaction and personality selection

### Technical Implementation
- **LLM Integration**: Uses Groq's Llama 3.3 70B model via OpenAI-compatible API
- **Memory Management**: Maintains conversation context with the last 6 messages and persistent user data
- **Command System**: Special commands for enhanced functionality (e.g., `/remember`, `/preference`)
- **Session Management**: Streamlit session state for maintaining conversation continuity

## 🎭 Personality Types

### 🤗 Friendly Bot
**Personality Traits:**
- Warm and enthusiastic communication style
- Uses emojis and exclamation marks naturally
- Shows genuine interest and empathy
- Encourages positive interactions
- Adds humor when appropriate

**Best For:** Casual conversations, emotional support, and general chit-chat

### 📚 Teacher Bot
**Personality Traits:**
- Structured and educational approach
- Clear explanations with practical examples
- Encourages critical thinking and deeper understanding
- Asks follow-up questions to reinforce learning
- Patient and supportive teaching style

**Best For:** Learning sessions, educational content, and structured knowledge sharing

### 🎨 Creative Bot (AlduinoBot)
**Personality Traits:**
- Innovative and artistic thinking
- Connects ideas across different domains
- Uses vivid, descriptive language
- Encourages creative experimentation
- Inspires with metaphors and analogies

**Extra Features:**
- Creative mode switching (`/creative [mode]`)
- Inspiration command (`/inspire`)
- Enhanced artistic and innovative responses

**Best For:** Brainstorming, creative projects, and innovative problem-solving

## ✨ Extra Features

### 🧠 Memory System
- **Conversation History**: Maintains context from the last 6 messages
- **User Preferences**: Store and recall user preferences (`/preference`)
- **Fact Memory**: Remember important facts about users (`/remember`)
- **Context Awareness**: Uses stored information to provide personalized responses

### 🎮 Special Commands
- `/help` - Display all available commands
- `/remember [fact]` - Store important information about the user
- `/preference [key] [value]` - Save user preferences
- `/facts` - View all remembered facts
- `/preferences` - View stored preferences
- `/personality` - Show current personality type
- `/creative [mode]` - Switch creative modes (Creative Bot only)
- `/inspire` - Get creative inspiration (Creative Bot only)

### 🎨 Web Interface Features
- **Personality Selection**: Easy switching between bot personalities
- **Customizable Names**: Personalize bot names for Teacher and Creative personalities
- **Subject Specialization**: Teacher bot can focus on specific subjects
- **Real-time Chat**: Streamlit chat interface with message history
- **Reset Functionality**: Clear conversation and start fresh
- **Command Help**: Built-in help system accessible via sidebar

### 🔧 Technical Features
- **Session Persistence**: Maintains conversation state across interactions
- **Error Handling**: Graceful handling of API errors and invalid inputs
- **Environment Configuration**: Secure API key management via `.env` files
- **Responsive Design**: Clean, modern UI that works across devices

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Groq API key

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Groq API key:
   ```
   API_KEY=your_groq_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Usage
1. Select your preferred personality from the sidebar
2. Configure additional settings (name, subject for Teacher bot)
3. Click "Start Chat" to begin your conversation
4. Use special commands to enhance your experience
5. Reset the conversation anytime to try different personalities

## 🛠️ Technology Stack
- **Backend**: Python 3.7+
- **Web Framework**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **API Integration**: OpenAI-compatible client
- **Environment Management**: python-dotenv
