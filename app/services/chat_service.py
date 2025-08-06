from app.repositories.chat_repo import ChatRepository
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
load_dotenv()


class ChatService:

    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    async def add_chat(self, user_id, role, user_query):
        print(role)

        system_instruction = """
            You are an AI teacher. Only answer questions related to AI.
            Always return the response in the exact JSON structure below.
            Do not include any extra text, code fences, or explanations outside of the JSON.

            {
            "title": "short answer title as string",
            "explanation": "detailed explanation as a string without markdown or code fences",
            "points": ["point 1", "point 2", "point 3"]
            }

            Rules:
            - Never return markdown or code blocks
            - 'points' must be a list of strings
            - All values must be plain text
            """

        prompt = f"""User question: {user_query}"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            ),
        )

        raw_output = response.text.strip()

        try:
            parsed_output = json.loads(raw_output)

            title = parsed_output.get("title", "")
            explanation = parsed_output.get("explanation", "")
            points = parsed_output.get("points", [])

            print("printed in try block \n\n\n\n\n\n\n")
            print("title", title)
            print("explanation", explanation)
            print("points", points)
        except json.JSONDecodeError:

            # Retry by asking Gemini to fix the format
            correction_prompt = f"""
            The following response is not valid JSON. 
            Fix it so it matches the required JSON format exactly:
            {raw_output}
            """
            correction_response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[correction_prompt],
            )
            corrected_text = (
                correction_response.text.strip() if correction_response.text else ""
            )
            try:
                parsed_output = json.loads(corrected_text)
            except (json.JSONDecodeError, TypeError):
                # Last fallback → store as plain explanation
                parsed_output = {"title": "", "explanation": raw_output, "points": []}

        print("parsed_output : ", parsed_output)

        print("\n")
        print(parsed_output.get("title"))

        print("\n")
        print(parsed_output.get("explanation"))
        print("\n")
        # Saving user message first
        await self.chat_repo.save_user_message(user_id, "user", message=user_query)

        await self.chat_repo.save_ai_message(
            user_id,
            "assistant",
            user_query=user_query,
            title=parsed_output.get("title"),
            explanation=parsed_output.get("explanation"),
            point=parsed_output.get("points"),
        )

        return parsed_output

    async def get_chats(self, user_id):

        return await self.chat_repo.get_all_messages(user_id)
