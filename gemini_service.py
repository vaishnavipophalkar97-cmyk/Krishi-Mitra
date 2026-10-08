import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

# Initializes the optimized SDK client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

def analyze_crop_disease(image: Image.Image, crop_name: str, language: str) -> str:
    """Uses Gemini Vision to identify diseases from a PIL Image."""
    prompt = f"""
    You are an expert plant pathologist. Analyze this image of a {crop_name} plant.
    Provide a concise report detailing:
    1. Possible Disease or Issue found.
    2. Concrete steps the farmer can take to treat it.
    3. Preventive measures for the next cycle.
    
    CRITICAL: Respond completely in {language}. Keep the answer brief and actionable.
    """
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[image, prompt]
        )
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def get_weather_advisory(location: str, crop: str, condition: str, language: str) -> str:
    """Generates immediate tactical agricultural instructions based on local weather conditions."""
    prompt = f"""
    A farmer growing {crop} in {location} reports current weather is {condition}.
    Give them exactly 3 hyper-localized, smart actions they should take today regarding watering, fertilization, or harvesting.
    Respond entirely in {language}.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

def farm_chat(history_context: list, user_message: str, farmer_profile: dict, language: str):
    """Contextual multi-turn chat assistant knowing the farmer's distinct profile metrics."""
    system_instruction = f"""
    You are KrishiAI, a wise, empathetic companion for farmers. 
    The farmer you are talking to has this profile: {str(farmer_profile)}.
    Always contextualize your answers based on their soil type and region.
    You must talk and respond strictly in {language}. Keep text concise.
    """
    
    # We construct a swift combined conversation block for a quick hackathon loop
    formatted_prompt = f"{system_instruction}\n\nConversation History:\n{str(history_context)}\n\nFarmer: {user_message}\nKrishiAI:"
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=formatted_prompt
    )
    return response.text