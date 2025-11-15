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
    )
        temperature=0.7, # temperature setting for response creativity
    return client_response.choices[0].message.content.strip()


