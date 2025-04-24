import google.generativeai as genai
import os

from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  



# Exit Detection function
exit_schema = {
    "name": "check_exit_intent",
    "description": "If the user wants to exit, ask them for a review and rating (1-5). End with a thank you message if both are provided.",
    "parameters": {
        "type": "object",
        "properties": {
            "review": {
                "type": "string",
                "description": "Short review from the user"
            },
            "rating": {
                "type": "integer",
                "description": "Rating between 1 to 5"
            },
            "msg": {
                "type": "string",
                "description": "provide a Thank you message if the user provides review and rating"
            },
            
        },
        "required": ["review","rating","msg"]
    }
}


#gemini configuratiopn
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[{"function_declarations": [exit_schema]}],
    system_instruction=(
        "You are a helpful chatbot whose task is to provide answers of general questions to the user. If the user wants to leave or exit the chat, "
        "use the check_exit_intent function to collect a short review and a rating (1-5) from the user in json like structure, "
        "and provide a thank-you message to the user using check_exit_intent function after both review and rating are collected."
    )
)

chat = model.start_chat()


#function to check if user wants to exit 
def detect_exit_intent(user_input):
    response = chat.send_message(f"{user_input}")
    try:
        fn = response.candidates[0].content.parts[0].function_call
        if fn.name == "check_exit_intent":
            review=fn.args.get("review",None)
            rating=fn.args.get("rating",None)
            msg=fn.args.get("msg","default feed back")
            return review, rating, msg
    except:
        pass
    return False

def main():
    print(" Welcome to Gemini CLI Chat!")
    print("(Type your message below)\n")

    chat_log = []

    while True:
        user_input = input("You: ")
        chat_log.append(f"You: {user_input}")

        if detect_exit_intent(user_input):
            data=detect_exit_intent(user_input)
            print("Bot:", data[2])
            with open("feedback.txt", "a") as f:
                f.write(f"Review: {data[0]}\nRating: {data[1]}\n\n")
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
    print("Chat history saved to 'chat_history.txt'")


if __name__ == "__main__":
    main()