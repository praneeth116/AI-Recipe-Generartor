import os
from groq import Groq
from rasa_sdk import Action
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

class ActionGenerateRecipe(Action):
    def name(self):
        return "action_generate_recipe"

    def run(self, dispatcher, tracker, domain):
        ingredient = tracker.get_slot("ingredient")
        cuisine = tracker.get_slot("cuisine")
        
        # Construct prompt
        prompt = f"Suggest a {cuisine if cuisine else 'general'} recipe using {ingredient if ingredient else 'any ingredients'}."

        # Call Groq API
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        recipe = response.choices[0].message.content
        
        dispatcher.utter_message(text=recipe)
        return []
