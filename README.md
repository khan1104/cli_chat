#Setup instruction 
1> https://aistudio.google.com/apikey go to this link and get your api key

2> after getting your api key create a .env file and paste your api key
eg (GEMINI_API_KEY="your_api_key")

#To run the application

>open the terminal and type "python cli_chat.py"

#Example chat sessions


You: define crm
Bot: CRM stands for Customer Relationship Management. It is a system for managing a company's interactions with current and future customers. It often involves using technology to organize, automate and synchronize sales, marketing, customer service, and technical support.

You: what is the capital of japan
Bot: The capital of Japan is Tokyo.

You: i want to leave
Bot: I understand you want to leave. Could you please provide a short review of our conversation and a rating between 1 and 5, with 5 being the best?

You: {"review":"really good","rating":4}
Bot: Thank you for the review and rating!
Chat history saved to 'chat_history.txt'


#two files named as chat_history.txt and feedback.txt was created after you exit or leave the chat
