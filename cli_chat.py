import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  



# Exit Detection function
exit_schema = {
    "name": "check_exit_intent",
    "description": "Check if the user wants to end the chat.",
    "parameters": {
        "type": "object",
        "properties": {
            "exit": {
                "type": "boolean",
                "description": "True if the user wants to leave or exit."
            }
        },
        "required": ["exit"]
    }
}

# 2. Feedback Collection function
feedback_schema = {
    "name": "collect_feedback",
    "description": "Collect a short review and a rating from the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "review": {
                "type": "string",
                "description": "Short review of the chat experience."
            },
            "rating": {
                "type": "integer",
                "description": "Rating from 1 to 5."
            }
        },
        "required": ["review", "rating"]
    }
}

#gemini configuratiopn
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[{"function_declarations": [exit_schema, feedback_schema]}],
    system_instruction="You are a helpful chatbot. First, answer the user's question normally. Also, if needed, you can detect if they want to exit or give feedback using the tools."
)

chat = model.start_chat()


#function to check if user wants to exit 
def detect_exit_intent(user_input):
    response = chat.send_message(
        f"Analyze this message and call the function if it is an exit message: '{user_input}'"
    )
    try:
        fn = response.candidates[0].content.parts[0].function_call
        if fn.name == "check_exit_intent":
            return fn.args.get("exit", False)
    except:
        pass
    return False


#function to collect feedback
def collect_feedback():
    print("\nBot: Before you go, could you please share a short review and rate me from 1 to 5?")

    response = chat.send_message(
        "Please ask the user for a short review and rating (1 to 5) and call the collect_feedback function."
    )

    try:
        fn = response.candidates[0].content.parts[0].function_call
        if fn.name == "collect_feedback":
            review = fn.args.get("review", "No review provided.")
            rating = fn.args.get("rating", "N/A")
        else:
            raise ValueError("Function not called")
    except:
        review = input("Please enter your review: ")
        while True:
            try:
                rating = int(input("Please give a rating (1 to 5): "))
                if 1 <= rating <= 5:
                    break
                else:
                    print("Rating must be between 1 and 5.")
            except:
                print("Please enter a valid number.")

    with open("feedback.txt", "a") as f:
        f.write(f"Review: {review}\nRating: {rating}\n")

    print("✅ Feedback saved to 'feedback.txt'")

def main():
    print("🧠 Welcome to Gemini CLI Chat!")
    print("(Type your message below. Say something like 'bye' to exit.)\n")

    chat_log = []

    while True:
        user_input = input("You: ")
        chat_log.append(f"You: {user_input}")

        if detect_exit_intent(user_input):
            collect_feedback()
            break

        try:
            response = chat.send_message(user_input)
            bot_reply = response.text
            print("Bot:", bot_reply)
            chat_log.append(f"Bot: {bot_reply}")
        except Exception as e:
            print("❌ Error from Gemini:", e)

   
    with open("chat_history.txt", "a") as f:
        f.write("\n".join(chat_log))
    print("💾 Chat history saved to 'chat_history.txt'")

# === RUN APP ===
if __name__ == "__main__":
    main()