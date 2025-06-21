# ai_logic.py
import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import json # Import json for parsing structured responses

# --- Load Environment Variables ---
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

# --- Retrieve Gemini API Key ---
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# --- API Key Validation ---
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
    # Streamlit will display this warning at the top of the app
    import streamlit as st
    st.error(
        "❌ **GEMINI_API_KEY** not found or is the placeholder value in your `.env` file. "
        "Please set it correctly to use AI features. Refer to the README for setup instructions."
    )
    st.stop() # Stop the Streamlit app execution if API key is missing

# --- Gemini Model Initialization ---
_gemini_model_instance = None

def get_gemini_model():
    """
    Initializes and returns a Gemini GenerativeModel.
    Prioritizes cost-effective models. Ensures model is initialized only once.
    """
    global _gemini_model_instance
    if _gemini_model_instance is not None:
        return _gemini_model_instance

    genai.configure(api_key=GOOGLE_API_KEY)

    # List available models and try to pick the most suitable one
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)

    # Prioritize models: gemini-1.5-flash (cost-effective), then gemini-pro (stable), then gemini-1.5-pro
    preferred_order = [
        'models/gemini-1.5-flash',
        'models/gemini-pro',
        'models/gemini-1.5-pro'
    ]

    chosen_model_name = None
    for preferred_model in preferred_order:
        if preferred_model in available_models:
            chosen_model_name = preferred_model
            break
    
    if chosen_model_name is None and available_models:
        chosen_model_name = available_models[0] # Fallback to any available

    if chosen_model_name:
        try:
            _gemini_model_instance = genai.GenerativeModel(chosen_model_name)
            print(f"Gemini model initialized: {chosen_model_name}") # For console logging
            return _gemini_model_instance
        except Exception as e:
            import streamlit as st # Import inside for conditional use
            st.error(f"Failed to initialize Gemini model '{chosen_model_name}'. Please check your API key and network access: {e}")
            st.stop() # Stop app if model fails to load
    else:
        import streamlit as st
        st.error(
            "No suitable Gemini model found that supports 'generateContent'. "
            "Please ensure your API key is correct and valid, or check Google AI Studio for available models."
        )
        st.stop()


def ask_gemini_text(prompt: str) -> str:
    """
    Sends a given prompt to the initialized Gemini model for text generation and returns its text response.
    Returns Markdown-formatted text from the AI.
    """
    try:
        model_instance = get_gemini_model()
    except Exception as e:
        return f"❌ AI Service Error: {e}"

    if not prompt.strip():
        return "❌ Please provide a valid prompt for the AI to process."

    try:
        response = model_instance.generate_content(prompt)

        if response and response.candidates and len(response.candidates) > 0 and \
           response.candidates[0].content and response.candidates[0].content.parts and \
           len(response.candidates[0].content.parts) > 0:
            return response.candidates[0].content.parts[0].text
        else:
            print(f"Gemini API returned an empty or unexpected text response structure: {response}")
            return "❌ AI did not return a valid text response. The AI might have refused the query or an internal error occurred. Please try again with different or simpler code."
    except genai.types.BlockedPromptException as e:
        return f"❌ AI Blocked Content: Your request was blocked due to safety policy. Details: {e.response.prompt_feedback.block_reason.name}."
    except Exception as e:
        print(f"Error during Gemini text API call: {e}")
        return f"❌ Gemini Text API Call Failed: {e}. Possible issues: network problem, rate limit, or invalid API key/model access."


def ask_gemini_structured(prompt: str, response_schema: dict) -> dict:
    """
    Sends a given prompt to the Gemini model requesting a structured JSON response.
    Returns a dictionary parsed from the AI's JSON output.
    """
    try:
        model_instance = get_gemini_model()
    except Exception as e:
        return {"error": f"❌ AI Service Error (Structured): {e}"}

    if not prompt.strip():
        return {"error": "❌ Please provide a valid prompt for structured AI processing."}
    
    if not response_schema:
        return {"error": "❌ A response_schema is required for structured AI output."}

    try:
        response = model_instance.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        if response and response.candidates and len(response.candidates) > 0 and \
           response.candidates[0].content and response.candidates[0].content.parts and \
           len(response.candidates[0].content.parts) > 0:
            
            json_text = response.candidates[0].content.parts[0].text
            try:
                parsed_json = json.loads(json_text)
                return parsed_json
            except json.JSONDecodeError as json_e:
                print(f"Failed to parse AI's JSON response: {json_e}\nRaw AI response: {json_text}")
                return {"error": f"❌ AI returned malformed JSON: {json_e}. Raw: {json_text[:200]}..."}
        else:
            print(f"Gemini API returned an empty or unexpected structured response structure: {response}")
            return {"error": "❌ AI did not return a valid structured response. It might have refused the query or an internal error occurred."}
    except genai.types.BlockedPromptException as e:
        return {"error": f"❌ AI Blocked Content (Structured): Your request for structured generation was blocked due to safety policy. Details: {e.response.prompt_feedback.block_reason.name}."
    }
    except Exception as e:
        print(f"Error during Gemini structured API call: {e}")
        return {"error": f"❌ Gemini Structured API Call Failed: {e}. Possible issues: network problem, rate limit, or invalid API key/model access."}

