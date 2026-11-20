import json
import re
from pathlib import Path

# 1. Qaamuuska jawaabaha iyo ujeeddooyinka (Intent-response dictionary)
DEFAULT_INTENTS = [
    {
        "intent": "greeting",
        "patterns": [r"\b(hi|hello|hey|greetings|salaam|asc|subax wanaagsan)\b"],
        "response": "Hello! Welcome to our support assistant. How can I help you today? (Ask about hours, products, pricing, returns, or shipping).",
    },
    {
        "intent": "business_hours",
        "patterns": [
            r"\b(hours|open|close|closing|schedule|time|when are you open)\b"
        ],
        "response": "Our business hours are Monday through Friday, 9:00 AM to 6:00 PM, and Saturday from 10:00 AM to 4:00 PM. We are closed on Sundays.",
    },
    {
        "intent": "products",
        "patterns": [
            r"\b(products|items|catalog|sell|offer|services|what do you have)\b"
        ],
        "response": "We offer laptops, smartphones, wireless accessories, and software support packages.",
    },
    {
        "intent": "pricing",
        "patterns": [r"\b(price|pricing|cost|how much|fee|rates|discount)\b"],
        "response": "Our accessories start at $15, smartphones from $299, and laptops from $599. Students get a 10% discount with a valid ID!",
    },
    {
        "intent": "shipping",
        "patterns": [r"\b(ship|shipping|delivery|deliver|track|how long)\b"],
        "response": "Standard shipping takes 3–5 business days and is free on orders over $50. Express next-day delivery is available for $15.",
    },
    {
        "intent": "returns",
        "patterns": [r"\b(return|refund|exchange|warranty|broken|policy)\b"],
        "response": "We offer a 30-day money-back return policy for unused items in original packaging, plus a 1-year hardware warranty.",
    },
    {
        "intent": "contact",
        "patterns": [r"\b(contact|support|email|phone|call|human|agent)\b"],
        "response": "You can reach our human support team at support@example.com or call +1-800-555-0199 during business hours.",
    },
]

EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "macsalaama"}


def load_intents(json_path: str = "faq_dataset.json") -> list:
    """Waxay soo akhridaa faylka JSON haddii uu jiro, haddii kalena waxay isticmaashaa DEFAULT_INTENTS."""
    path = Path(json_path)
    if path.is_file():
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    return data
        except (json.JSONDecodeError, OSError) as e:
            print(f"[Warning] Could not load '{json_path}' ({e}). Using built-in FAQs.")
    return DEFAULT_INTENTS


def normalize_input(text: str) -> str:
    """Waxay qoraalka ka dhigtaa xarfo yaryar (lowercase), waxayna ka saartaa calaamadaha dheeraadka ah."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def match_intent(normalized_text: str, intents: list) -> tuple[str | None, str]:
    """Waxay baadhaa ujeeddada ugu dhow iyadoo isticmaalaysa regex keyword matching."""
    best_intent = None
    best_response = (
        "I'm not quite sure I understood that. Could you rephrase? "
        "You can ask me about business hours, products, pricing, shipping, returns, or contact info."
    )
    highest_score = 0

    for item in intents:
        score = 0
        for pattern in item.get("patterns", []):
            matches = re.findall(pattern, normalized_text)
            score += len(matches)

        if score > highest_score:
            highest_score = score
            best_intent = item.get("intent")
            best_response = item.get("response", best_response)

    return best_intent, best_response


def run_chatbot():
    intents = load_intents()
    state = "GREETING"

    print("=" * 55)
    print("  CUSTOMER SUPPORT TERMINAL ASSISTANT (chatbot.py)")
    print("  Type 'bye', 'exit', or 'quit' to end the chat.")
    print("=" * 55)
    print("\nBot: Hello! How can I assist you today?\n")

    while True:
        try:
            user_raw = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session ended. Goodbye!")
            break

        cleaned = normalize_input(user_raw)

        if not cleaned:
            print("Bot: Please type a question or message.\n")
            continue

        # 5. Hubi amarrada bixitaanka (Exit commands)
        if cleaned in EXIT_COMMANDS or any(
            re.search(rf"\b{word}\b", cleaned) for word in EXIT_COMMANDS
        ):
            state = "EXIT"
            print("Bot: Thank you for chatting with us! Have a great day. Goodbye!")
            break

        # 4. Maamulka xaaladda wada-sheekaysiga (State management)
        state = "INTENT_IDENTIFICATION"
        intent, response = match_intent(cleaned, intents)

        if intent:
            state = "RESOLUTION"
            print(f"Bot [{intent}]: {response}\n")
        else:
            state = "FALLBACK"
            print(f"Bot: {response}\n")


if __name__ == "__main__":
    run_chatbot()
