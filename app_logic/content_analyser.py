from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import re
import textwrap
import os


# for OpenAI support 
try:
    from openai import OpenAI
    _OPENAI_IS_AVAILABLE = True
except ImportError:
    _OPENAI_IS_AVAILABLE = False
    OpenAI = None  # Will raise error if actually used

# for Google Gemini support
try:
    import google.generativeai as gemini
    _GEMINI_IS_AVAILABLE = True
except ImportError:
    _GEMINI_IS_AVAILABLE = False
    gemini = None  # Will raise error if actually used

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
    return gemini.GenerativeModel("gemini-flash-latest")

def call_openai(prompt:str, system: str) -> str | None:
    client = openai_client()
    if client is None:
        return None
    client_response = client.chat.completions.create(
        model = "gpt-4o-mini",  # Using gpt-4o-mini for cost-effectiveness
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
def llm_call(prompt: str, system: str, provider: str = "gemini") -> str:
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

    else:
        if text is None:
            raise ValueError("Error‼️ No valid LLM provider available.")
        return textwrap.shorten(prompt, width = 600, placeholder = "...")       # Last resort fallback to limit crashes
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

def extract_concepts(
    text: str,
    max_concepts: int = 12,
    provider: str = "gemini",
) -> List[str]:
    """
    Extract key concepts/terms from the text.
    """
    system = (
        "You extract key concepts and terms from study materials for college students."
    )
    prompt = (
        "List the most important concepts, terms, or ideas from the following text.\n"
        "Return them as a simple bullet list, one concept per line.\n"
        f"Text:\n{text}"
    )

    raw = llm_call(prompt, system, provider=provider)
    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    concepts: List[str] = []
    for line in lines:
        # Strip bullet characters
        line = re.sub(r"^[\-\*\d\.\)\s]+", "", line)
        if line and line not in concepts:
            concepts.append(line)

    return concepts[:max_concepts]


def generate_flashcards(
    text: str,
    concepts: List[str],
    max_cards: int = 8,
    provider: str = "gemini",
) -> List[FlashcardGen]:
    """
    Generate flashcards based on the text and extracted concepts.
    """
    if not concepts:
        return []

    system = (
        "You are an expert at making flashcards for college students. "
        "You create short, focused questions and answers."
    )
    concept_str = ", ".join(concepts)
    prompt = (
        "Create flashcards for a college student based on the following text and key concepts.\n\n"
        f"Concepts: {concept_str}\n\n"
        "Text:\n"
        f"{text}\n\n"
        "Return them in the format:\n"
        "Q1: ...\nA1: ...\nQ2: ...\nA2: ...\n"
        "Keep questions short and specific. Answers should be 1–3 sentences.\n"
        f"Generate at most {max_cards} cards."
    )

    raw = llm_call(prompt, system, provider=provider)

    # Parse Q/A pairs
    cards: List[FlashcardGen] = []
    pattern = re.compile(r"Q\d+:\s*(.+?)\s*A\d+:\s*(.+?)(?=Q\d+:|$)", re.DOTALL)
    for match in pattern.finditer(raw):
        q = match.group(1).strip()
        a = match.group(2).strip()
        if q and a:
            cards.append(FlashcardGen(question=q, answer=a))

    # If parsing failed, fall back to a simple template
    if not cards:
        for i, c in enumerate(concepts[:max_cards], start=1):
            cards.append(
                FlashcardGen(
                    question=f"What is {c}?",
                    answer=(
                        f"{c} is a key concept discussed in the material. "
                        "(Replace with a better answer using the LLM.)"
                    ),
                )
            )

    return cards[:max_cards]