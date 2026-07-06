import os
import logging
import traceback

import streamlit as st


# -----------------------------
# Logging
# -----------------------------

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger("BizPilot")


# -----------------------------
# Config
# -----------------------------

GEMINI_MODEL = "gemini-2.5-flash"

GROQ_MODEL = "llama-3.3-70b-versatile"

TEMPERATURE = 0.3


# -----------------------------
# Secret Loader
# -----------------------------

def get_secret(name):

    # Streamlit Cloud
    try:
        return st.secrets[name]

    except Exception:
        pass


    # Local .env
    return os.getenv(name)



# -----------------------------
# Gemini Provider
# -----------------------------

def call_gemini(prompt):

    from google import genai
    from google.genai import types

    key = get_secret(
        "GEMINI_API_KEY"
    )

    if not key:
        raise ValueError(
            "Gemini key missing"
        )


    client = genai.Client(
        api_key=key
    )


    logger.info(
        "Calling Gemini"
    )


    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
            top_p=0.95,
            max_output_tokens=4096,
        )
    )


    if not response.text:
        raise Exception(
            "Empty Gemini response"
        )


    return response.text



# -----------------------------
# Groq Provider
# -----------------------------

def call_groq(prompt):

    from groq import Groq


    key = get_secret(
        "GROQ_API_KEY"
    )


    if not key:
        raise ValueError(
            "Groq key missing"
        )


    client = Groq(
        api_key=key,
        timeout=120.0
    )


    logger.info(
        "Calling Groq fallback"
    )


    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are BizPilot AI.

You help entrepreneurs with:
- business entity decisions
- accounting stack selection
- tax readiness
- workforce planning
- integrations

Give practical recommendations.
Avoid pretending to provide legal advice.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=4096
    )


    return response.choices[0].message.content



# -----------------------------
# Final Fallback
# -----------------------------

def fallback_response(prompt):

    logger.warning(
        "Using deterministic fallback"
    )


    return f"""
BizPilot AI Analysis

Input:
{prompt}


AI provider unavailable.

The system can still provide:
- workflow analysis
- compliance checklist generation
- accounting architecture mapping

Please configure an AI provider key.
"""



# -----------------------------
# Main LLM Router
# -----------------------------

def call_llm(prompt: str):

    errors = []

    # Priority 1: Gemini
    gemini_key = get_secret("GEMINI_API_KEY")
    if gemini_key:
        try:
            return call_gemini(prompt)
        except Exception as e:
            logger.error(f"Gemini failed: {e}")
            logger.error(traceback.format_exc())
            errors.append(f"Gemini Error: {str(e)}")

    # Priority 2: Groq
    groq_key = get_secret("GROQ_API_KEY")
    if groq_key:
        try:
            return call_groq(prompt)
        except Exception as e:
            logger.error(f"Groq failed: {e}")
            logger.error(traceback.format_exc())
            errors.append(f"Groq Error: {str(e)}")

    # Priority 3: Error
    if errors:
        st.error("AI Provider failed to generate a response:\n\n" + "\n\n".join(errors))
        st.stop()

    st.error("No API key found. Please enter your API key")
    st.stop()