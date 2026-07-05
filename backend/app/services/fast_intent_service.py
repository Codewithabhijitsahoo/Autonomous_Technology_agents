import re
from typing import Dict, Any, Optional

class FastIntentClassifier:
    """
    Ultra Fast Rule Engine executed BEFORE any Gemini call.
    Instantly classifies Greetings, Casual Conversation, and Simple Requests.
    """
    
    GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    CASUAL = ["how are you", "thanks", "thank you", "bye", "goodbye", "good night", "see you"]
    SIMPLE_REQUESTS = ["tell me a joke", "who are you", "what can you do", "help"]
    
    STATIC_RESPONSES = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What can I research for you?",
        "hey": "Hey! How can I assist you?",
        "thanks": "You're welcome! Let me know if you need anything else.",
        "thank you": "You're very welcome!",
        "bye": "Goodbye! Have a great day.",
        "who are you": "I am the Deep Technology Agent, an AI research assistant.",
        "help": "I can help you research complex topics, analyze trends, or just chat. What do you need?",
        "good morning": "Good morning! Ready to do some research?",
        "good night": "Good night! See you next time."
    }

    def _normalize(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text.lower().strip())

    def _estimate_complexity(self, query: str) -> str:
        words = query.split()
        if len(words) <= 5:
            return "Simple"
        if any(w in query.lower() for w in ["compare", "analyze", "research", "latest"]):
            return "Complex"
        if " and " in query.lower() and len(words) > 15:
            return "Very Complex"
        return "Medium"

    def classify(self, query: str) -> Optional[Dict[str, Any]]:
        norm = self._normalize(query)
        
        # 1. Exact or partial match for static casual responses
        matched_category = None
        static_response = None
        
        for g in self.GREETINGS:
            if norm == g or norm.startswith(g + " "):
                matched_category = "Greeting"
                static_response = self.STATIC_RESPONSES.get(g, self.STATIC_RESPONSES["hello"])
                break
                
        if not matched_category:
            for c in self.CASUAL:
                if norm == c or norm.startswith(c + " "):
                    matched_category = "Casual Chat"
                    static_response = self.STATIC_RESPONSES.get(c, "I'm here to help!")
                    break
                    
        if not matched_category:
            for s in self.SIMPLE_REQUESTS:
                if norm == s or norm.startswith(s + " "):
                    matched_category = "Simple Request"
                    static_response = self.STATIC_RESPONSES.get(s, "I'm a research assistant. Ask me to research something!")
                    break

        if matched_category:
            return {
                "fast_path_activated": True,
                "rule_matched": matched_category,
                "response": static_response,
                "intent": "casual_chat",
                "complexity": "Simple",
                "needs_research": False,
                "confidence": 1.0,
                "mode": "casual_chat"
            }
            
        # Fast Complexity Detection
        est_complex = self._estimate_complexity(query)
        
        return {
            "fast_path_activated": False,
            "estimated_complexity": est_complex
        }

fast_intent_classifier = FastIntentClassifier()
