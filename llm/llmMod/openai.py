
import openai
from langchain_community.chat_message_histories import ChatMessageHistory

# Initialize OpenAI API key
openai.api_key = ""

class OpenAiUtils:
    # In-memory store for session histories
    store = {}

    @staticmethod
    def get_session_history(session_id: str) -> ChatMessageHistory:
        if session_id not in OpenAiUtils.store:
            OpenAiUtils.store[session_id] = ChatMessageHistory()
        return OpenAiUtils.store[session_id]

    @staticmethod
    def call_openai_model(messages):
        # Example system prompt
        systemPrompt = {
            "role": "system",
            "content": (
                "You are a helpful code generator with good understanding of python and java. Generate code based on the instruction mentioned by user. "
                "If the user has mentioned the language, generate code in the given language otherwise generate in python without any comments. "
                "Just provide the code with no explanation."
            )
        }

        # Prepare the messages array
        formatted_messages = [systemPrompt] + messages

        # Call OpenAI's ChatCompletion.create
        response = openai.chat.completions.create(
            model="gpt-4-32k",
            messages=formatted_messages,
            temperature=0.0,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Extract the generated text (response content)
        return response.choices[0].message.content.strip()

    @staticmethod
    def globalSearch(userPrompt, session_id):
        # Get the current session's message history
        session_history = OpenAiUtils.get_session_history(session_id)

        # Add the new user prompt to the session history
        session_history.add_message({"role": "user", "content": userPrompt})

        # Prepare the list of messages in the format expected by OpenAI API
        all_messages = session_history.messages

        # Get the model's response to the current input and context
        ai_response_content = OpenAiUtils.call_openai_model(all_messages)

        # Add the model’s response back to session history
        session_history.add_message({"role": "assistant", "content": ai_response_content})

        return ai_response_content