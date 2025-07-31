from typing import List, Dict
from utils import query_llm
import re

class Memory:
    """Stores conversation history and user preferences"""
    def __init__(self):
        # Store last 5 messages (increased from 3 for better context)
        self.messages: List[Dict] = []
        # Store user preferences and facts
        self.user_preferences: Dict = {}
        self.remembered_facts: List[str] = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a new message to memory
        Args:
            role: Either "user" or "bot" 
            content: The message content
        """
        # Create a dictionary to store the message
        message_dict = {"role": role, "content": content}
        
        # Add it to self.messages
        self.messages.append(message_dict)
        
        # Keep only the last 5 messages for context
        if len(self.messages) > 5:
            self.messages = self.messages[-5:]
    
    def get_recent_messages(self) -> str:
        """
        Get string of recent messages for context
        Returns:
            A string containing the last few messages
        """
        if not self.messages:
            return ""
        
        # Build output string from recent messages
        output_lines = []
        for message in self.messages:
            role = message["role"].capitalize()
            content = message["content"]
            output_lines.append(f"{role}: {content}")
        
        return "\n".join(output_lines).strip()
    
    def add_preference(self, key: str, value: str) -> None:
        """Store user preferences"""
        self.user_preferences[key] = value
    
    def add_fact(self, fact: str) -> None:
        """Store important facts about the user"""
        if fact not in self.remembered_facts:
            self.remembered_facts.append(fact)
    
    def get_preferences_summary(self) -> str:
        """Get a summary of user preferences"""
        if not self.user_preferences:
            return ""
        return "User preferences: " + ", ".join([f"{k}: {v}" for k, v in self.user_preferences.items()])
    
    def get_facts_summary(self) -> str:
        """Get a summary of remembered facts"""
        if not self.remembered_facts:
            return ""
        return "Remembered facts: " + "; ".join(self.remembered_facts)

class Chatbot:
    """Base chatbot class with core functionality"""
    def __init__(self, name: str):
        self.name: str = name
        self.memory: Memory = Memory()
        self.personality_type: str = "base"
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create a prompt for the LLM
        Args:
            user_input: The user's message
        Returns:
            A formatted prompt string
        """
        # Get conversation history
        recent_messages = self.memory.get_recent_messages()
        preferences = self.memory.get_preferences_summary()
        facts = self.memory.get_facts_summary()
        
        # Build comprehensive prompt
        prompt_parts = [
            f"You are {self.name}, a helpful AI assistant.",
            f"Personality: {self.personality_type}",
            f"Recent conversation:\n{recent_messages}",
        ]
        
        if preferences:
            prompt_parts.append(preferences)
        if facts:
            prompt_parts.append(facts)
        
        prompt_parts.append(f"User says: {user_input}")
        prompt_parts.append("Please respond naturally and helpfully.")
        
        return "\n".join(prompt_parts)
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input
        Args:
            user_input: The user's message
        Returns:
            The chatbot's response
        """
        # Check for special commands first
        if user_input.startswith("/"):
            return self._handle_special_commands(user_input)
        
        # Store the user's message in memory
        self.memory.add_message("user", user_input)
        
        # Create a prompt using _create_prompt() method
        prompt = self._create_prompt(user_input)
        
        # Use query_llm() to get a response
        response = query_llm(prompt)
        
        # Store the bot's response in memory
        self.memory.add_message("bot", response)
        
        return response
    
    def _handle_special_commands(self, command: str) -> str:
        """Handle special commands like /help, /remember, etc."""
        cmd_parts = command.split(" ", 1)
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        if cmd == "/help":
            return """Special Commands:
/help - Show this help message
/remember [fact] - Remember something about the user
/preference [key] [value] - Store a user preference
/facts - Show remembered facts
/preferences - Show user preferences
/personality - Show current personality type"""
        
        elif cmd == "/remember" and args:
            self.memory.add_fact(args)
            return f"I'll remember that: {args}"
        
        elif cmd == "/preference" and args:
            parts = args.split(" ", 1)
            if len(parts) == 2:
                key, value = parts
                self.memory.add_preference(key, value)
                return f"I've stored your preference: {key} = {value}"
            else:
                return "Usage: /preference [key] [value]"
        
        elif cmd == "/facts":
            facts = self.memory.get_facts_summary()
            return facts if facts else "No facts remembered yet."
        
        elif cmd == "/preferences":
            prefs = self.memory.get_preferences_summary()
            return prefs if prefs else "No preferences stored yet."
        
        elif cmd == "/personality":
            return f"Current personality: {self.personality_type}"
        
        else:
            return "Unknown command. Type /help for available commands."

class FriendlyBot(Chatbot):
    """A casual and friendly personality with enthusiasm and humor"""
    def __init__(self, name: str):
        super().__init__(name)
        self.personality_type = "Friendly"
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create friendly-style prompts with enthusiasm and humor
        """
        recent_messages = self.memory.get_recent_messages()
        preferences = self.memory.get_preferences_summary()
        facts = self.memory.get_facts_summary()
        
        prompt_parts = [
            f"You are {self.name}, a super friendly and enthusiastic AI assistant!",
            "Personality traits:",
            "- Always positive and encouraging",
            "- Use exclamation marks and emojis when appropriate",
            "- Show genuine interest in the user",
            "- Use casual, warm language",
            "- Add humor when suitable",
            "- Be supportive and empathetic",
            f"Recent conversation:\n{recent_messages}",
        ]
        
        if preferences:
            prompt_parts.append(preferences)
        if facts:
            prompt_parts.append(facts)
        
        prompt_parts.append(f"User says: {user_input}")
        prompt_parts.append("Respond in a friendly, enthusiastic way that matches this personality!")
        
        return "\n".join(prompt_parts)

class TeacherBot(Chatbot):
    """A formal, educational personality with structured teaching approach"""
    def __init__(self, name: str, subject: str):
        super().__init__(name)
        self.subject = subject
        self.personality_type = f"Teacher ({subject})"
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create teaching-style prompts with educational focus
        """
        recent_messages = self.memory.get_recent_messages()
        preferences = self.memory.get_preferences_summary()
        facts = self.memory.get_facts_summary()
        
        prompt_parts = [
            f"You are {self.name}, a knowledgeable and patient teacher specializing in {self.subject}.",
            "Teaching style:",
            "- Clear, structured explanations",
            "- Use examples and analogies",
            "- Encourage critical thinking",
            "- Ask follow-up questions to deepen understanding",
            "- Provide educational context",
            "- Be patient and supportive of learning",
            f"Recent conversation:\n{recent_messages}",
        ]
        
        if preferences:
            prompt_parts.append(preferences)
        if facts:
            prompt_parts.append(facts)
        
        prompt_parts.append(f"User says: {user_input}")
        prompt_parts.append(f"Respond as an expert teacher in {self.subject}, helping the user learn and understand.")
        
        return "\n".join(prompt_parts)

class AlduinoBot(Chatbot):
    """A creative, artistic personality with a love for innovation and imagination"""
    def __init__(self, name: str):
        super().__init__(name)
        self.personality_type = "Creative Innovator"
        self.creative_mode = "artistic"
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create creative, innovative prompts with artistic flair
        """
        recent_messages = self.memory.get_recent_messages()
        preferences = self.memory.get_preferences_summary()
        facts = self.memory.get_facts_summary()
        
        prompt_parts = [
            f"You are {self.name}, a creative and innovative AI with a passion for art, technology, and imagination!",
            "Creative personality traits:",
            "- Think outside the box and suggest innovative solutions",
            "- Use vivid, descriptive language",
            "- Draw connections between different fields and ideas",
            "- Encourage creative thinking and experimentation",
            "- Share interesting facts and trivia",
            "- Use metaphors and analogies",
            "- Be inspiring and motivational",
            f"Creative mode: {self.creative_mode}",
            f"Recent conversation:\n{recent_messages}",
        ]
        
        if preferences:
            prompt_parts.append(preferences)
        if facts:
            prompt_parts.append(facts)
        
        prompt_parts.append(f"User says: {user_input}")
        prompt_parts.append("Respond with creativity, innovation, and artistic flair!")
        
        return "\n".join(prompt_parts)
    
    def _handle_special_commands(self, command: str) -> str:
        """Handle AlduinoBot-specific commands"""
        cmd_parts = command.split(" ", 1)
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        if cmd == "/creative":
            if args:
                self.creative_mode = args
                return f"Switched to creative mode: {args}"
            else:
                return f"Current creative mode: {self.creative_mode}"
        
        elif cmd == "/inspire":
            return "🌟 Let's create something amazing together! What's on your mind?"
        
        else:
            # Call parent method for other commands
            return super()._handle_special_commands(command)

def main():
    """Main interaction loop with personality switching"""
    print("🤖 Welcome to AlduinoBot - Your AI Companion!")
    print("=" * 50)
    
    # Let user choose personality
    print("Choose your AlduinoBot personality:")
    print("1. Friendly Bot - Warm and enthusiastic")
    print("2. Teacher Bot - Educational and structured")
    print("3. Creative Bot - Innovative and artistic")
    
    choice = input("Enter 1, 2, or 3: ")
    
    if choice == "1":
        bot = FriendlyBot("Joy")
    elif choice == "2":
        subject = input("What subject should I teach? ")
        bot = TeacherBot("Prof. Smith", subject)
    elif choice == "3":
        bot = AlduinoBot("Alduino")
    else:
        print("Invalid choice, defaulting to Friendly Bot")
        bot = FriendlyBot("Joy")
    
    print(f"\n{bot.name}: Hello! I'm your {bot.personality_type} companion. How can I help you today?")
    print("Type /help for special commands, or 'quit' to exit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print(f"{bot.name}: Goodbye! It was wonderful chatting with you! 👋")
            break
        
        response = bot.generate_response(user_input)
        print(f"{bot.name}: {response}")

if __name__ == "__main__":
    main()