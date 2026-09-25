import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_fitness_plan(user_data):
    # Latest stable model name use pannunga
    model = genai.GenerativeModel('gemini-3.6-flash')

    prompt = f"Create a workout and diet plan for: {user_data}"
    response = model.generate_content(prompt)
    return response.text