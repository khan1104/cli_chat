import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

exit_schema = {
    "name": "check_exit_intent",
    "description": "If the user wants to exit, collect a short review and rating from 1–5. End with a thank you message if both are provided.",
    "parameters": {
        "type": "object",
        "properties": {
            "msg": {
                "type": "string",
                "description": "Thank you message if the user provides review and rating"
            },
            "review": {
                "type": "string",
                "description": "Short review from the user"
            },
            "rating": {
                "type": "integer",
                "description": "Rating between 1 to 5"
            }
        },
        "required": ["review", "rating","msg"]
    }
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[{"function_declarations": [exit_schema]}],
    system_instruction=(
        "You are a helpful chatbot. If the user wants to leave, use the check_exit_intent function. "
        "First ask for a short review. Then ask for a rating (1–5)in a json like structure. Once both are received, say thank you."
    )
)

chat = model.start_chat()

def detect_exit_intent(user_input):
    response = chat.send_message(user_input)

    # Step 1: Check if Gemini tries to call exit function
    try:
        fn = response.candidates[0].content.parts[0].function_call
        if fn.name == "check_exit_intent":
            review = fn.args.get("review")
            rating = fn.args.get("rating")
            thank_you = fn.args.get("msg", "")

            print(f"\n📝 Review: {review}")
            print(f"⭐ Rating: {rating}")
            print(f"🙏 {thank_you}")

            with open("feedback.txt", "a") as f:
                f.write(f"Review: {review}\nRating: {rating}\n\n")

            return True
    except Exception:
        pass

    return False

def main():
    print("🧠 Welcome to Gemini CLI Chat!")
    print("(Type your message below. Say 'exit' or 'I want to leave' to quit.)\n")

    chat_log = []

    while True:
        user_input = input("You: ")
        chat_log.append(f"You: {user_input}")

        if detect_exit_intent(user_input):
            break

        try:
            response = chat.send_message(user_input)
            print("Bot:", response.text)
            chat_log.append(f"Bot: {response.text}")
        except Exception as e:
            print("❌ Error from Gemini:", e)

    with open("chat_history.txt", "a") as f:
        f.write("\n".join(chat_log))
    print("💾 Chat history saved to 'chat_history.txt'")

if __name__ == "__main__":
    main()
