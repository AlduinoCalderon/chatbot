# app.py

import streamlit as st
from chatbot_logic import FriendlyBot, TeacherBot, AlduinoBot

# --- Page Configuration ---
st.set_page_config(
    page_title="AlduinoBot - Your AI Companion",
    page_icon="🐢",
    layout="centered"
)

st.title("🐢 AlduinoBot: Your AI Companion")
st.write("Choose a personality from the sidebar and start chatting!")

# --- Sidebar for Bot Selection and Control ---
with st.sidebar:
    st.header("🤖 AlduinoBot Configuration")

    # Initialize bot in session state if not present
    if 'bot' not in st.session_state:
        st.session_state.bot = None

    bot_choice = st.radio(
        "Choose your AlduinoBot personality:",
        ('Friendly', 'Teacher', 'Creative'),
        key="bot_choice_radio",
        disabled=(st.session_state.bot is not None) # Disable after selection
    )

    subject = ""
    bot_name = ""
    
    if bot_choice == 'Teacher':
        subject = st.text_input(
            "What subject should the teacher focus on?",
            "Computer Science",
            key="subject_input",
            disabled=(st.session_state.bot is not None)
        )
        bot_name = st.text_input(
           "What is the teacher's name?",
           "Professor Alduino",
           key="name_input",
           disabled=(st.session_state.bot is not None)
        )
    elif bot_choice == 'Creative':
        bot_name = st.text_input(
           "What is the creative bot's name?",
           "Alduino",
           key="creative_name_input",
           disabled=(st.session_state.bot is not None)
        )

    if st.button("Start Chat", key="start_button", disabled=(st.session_state.bot is not None)):
        if bot_choice == 'Friendly':
            st.session_state.bot = FriendlyBot(name="Joy")
        elif bot_choice == 'Teacher':
            if subject and bot_name:
                st.session_state.bot = TeacherBot(name=bot_name, subject=subject)
            else:
                st.warning("Please enter BOTH a subject and a name for the Teacher Bot.")
                st.stop()
        elif bot_choice == 'Creative':
            if bot_name:
                st.session_state.bot = AlduinoBot(name=bot_name)
            else:
                st.warning("Please enter a name for the Creative Bot.")
                st.stop()
        
        # Initialize chat history
        st.session_state.messages = [{"role": "assistant", "content": f"Hello! I'm your {st.session_state.bot.personality_type} companion. How can I help you today?"}]
        st.rerun()

    if st.session_state.bot is not None:
        if st.button("Reset Conversation", key="reset_button"):
            st.session_state.bot = None
            st.session_state.messages = []
            st.rerun()
        
        # Show bot info
        st.subheader("🤖 Bot Information")
        st.write(f"**Name:** {st.session_state.bot.name}")
        st.write(f"**Personality:** {st.session_state.bot.personality_type}")
        
        # Show special commands help
        with st.expander("📚 Special Commands"):
            st.markdown("""
            **Available Commands:**
            - `/help` - Show all commands
            - `/remember [fact]` - Remember something about you
            - `/preference [key] [value]` - Store your preferences
            - `/facts` - Show remembered facts
            - `/preferences` - Show your preferences
            - `/personality` - Show current personality
            
            **Creative Bot Only:**
            - `/creative [mode]` - Switch creative modes
            - `/inspire` - Get inspired!
            """)

# --- Main Chat Interface ---
if 'bot' in st.session_state and st.session_state.bot is not None:
    # Display chat messages
    for message in st.session_state.get('messages', []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to say?"):
        # Add user message to display history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                response = st.session_state.bot.generate_response(prompt)
                st.markdown(response)
        
        # Add assistant response to display history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("🎯 Please configure your AlduinoBot in the sidebar and click 'Start Chat' to begin!")
    
    st.subheader("🌟 Personality Types")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤗 Friendly Bot**
        - Warm and enthusiastic
        - Uses emojis and exclamations
        - Supportive and empathetic
        - Great for casual conversations
        """)
    
    with col2:
        st.markdown("""
        **📚 Teacher Bot**
        - Educational and structured
        - Clear explanations with examples
        - Encourages critical thinking
        - Perfect for learning sessions
        """)
    
    with col3:
        st.markdown("""
        **🎨 Creative Bot**
        - Innovative and artistic
        - Thinks outside the box
        - Inspires creativity
        - Great for brainstorming
        """)