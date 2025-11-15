from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import os


# for OpenAI support 
try:
    from openai import OpenAI
    _OPENAI_IS_AVAILABLE = True
except ImportError:
    _OPENAI_IS_AVAILABLE = False
    OpenAI = None # ignoring 
    raise ImportError("Error‼️ OpenAI library is not installed. Please install the dependency to use OpenAI features. ")

# for Google Gemini support
try:
    import google.generativeai as gemini
    _GEMINI_IS_AVAILABLE = True
except ImportError:
    _GEMINI_IS_AVAILABLE = False
    gemini = None # ignoring 
    raise ImportError("Error‼️ Google Gemini library is not installed. Please install the dependency to use Gemini features. ")

@dataclass
class FlashcardGen:
    question: str
    answer: str


''' LLM Helpers for Content Analysis'''
def openai_client():
    if not _OPENAI_IS_AVAILABLE:
        raise ImportError("Error‼️ OpenAI is not available.")
        return None
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Error‼️ OpenAI API key not found in environment variables.")
        return None
    return OpenAI(api_key=api_key)

def gemini_client():
    if not _GEMINI_IS_AVAILABLE:
        raise ImportError("Error‼️ Google Gemini is not available.")
        return None
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Error‼️ Google API key not found in environment variables.")
        return None
    gemini.configure(api_key=api_key)
    return gemini.GenrativeModel("gemini-1.5-flash")

def call_openai(prompt:str, system: str) -> str | None:
    client = openai_client()
    if client is None:
        return None
    client_response = client.chat.completions.create(
        model = "gpt-5-chat-latest", 
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7, # temperature setting for response creativity
    )
    return client_response.choices[0].message.content.strip()

def call_gemini(prompt:str, system: str) -> str | None:
    model = gemini_client()
    if model is None:
        return None
    full_prompt = f"System:  {system} \n\nUser:  {prompt}"
    client_response = model.generate_content(full_prompt)

    if not client_response or not getattr(client_response, "text", None):
        return None
    return client_response.text.strip()

# help function to call LLM based on provider chosen
def llm_call(prompt: str, system: str, provider: str = "openai") -> str:
    ''' If a user has chosen a specific LLM provider, try to use that one. If specified provider is unavailable, fall back to the othe provider.
    '''

    text: str | None = None
    if provider == "openai":
        text = call_openai(prompt, system)
        if text is None:
            text = call_gemini(prompt, system)
    elif provider == "gemini":
        text = call_gemini(prompt, system)
        if text is None:
            text = call_openai(prompt, system)
    
    return text

# Returns a student-friendly summary of the uploaded content
def summarize_content(content: str, provider: str = "gemini") -> str:
    system_prompt = "You are an educational assistant that creates clear, concise student-friendly summaries of educational content."

    prompt_text = ("Summarize the following content in a way that is easy for a college student to understand:\n\n"
                f""" Requirements:
                - Focus on key concepts/main ideas, define important terms, and explain relationships between ideas.
                - Use simple, clear language and avoid jargon.
                - Keep the summary concise (around 400 - 600 words).
                - Structure the summary with short paragraphs or bullet points for readability.
                \n\nContent:\n{content}""")
    
    summary_result = llm_call(prompt_text, system_prompt, provider = provider)
    return summary_result