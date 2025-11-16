from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StudyTask:
    title: str
    estimated_time: str
    description: str = ""


@dataclass
class QuizQuestion:
    text: str


def generate_study_plan(
    concepts: List[str],
    mastery: Dict[str, float],
    max_tasks: int = 6,
) -> List[StudyTask]:
    """
    Generate a simple, prioritized study plan based on concept mastery.
    Lower mastery concepts are prioritized.
    """
    # Ensure we have mastery scores for all concepts
    working_mastery = {c: mastery.get(c, 0.3) for c in concepts}

    # Sort by ascending mastery (weaker first)
    sorted_concepts = sorted(
        working_mastery.items(),
        key=lambda kv: kv[1],
    )

    tasks: List[StudyTask] = []

    for concept, score in sorted_concepts[:max_tasks]:
        strength = int(score * 100)
        tasks.append(
            StudyTask(
                title=f"Review: {concept}",
                estimated_time="10–15 min",
                description=(
                    f"Revisit notes, examples, and explanations for **{concept}** "
                    f"(current mastery ~{strength}%)."
                ),
            )
        )
        tasks.append(
            StudyTask(
                title=f"Practice problems: {concept}",
                estimated_time="10–20 min",
                description=f"Find or create 3–5 practice questions involving **{concept}**.",
            )
        )

    # Cap number of tasks
    return tasks[:max_tasks]


def generate_quiz(
    concepts: List[str],
    text: str,
    num_questions: int = 5,
) -> List[QuizQuestion]:
    """
    Generate simple open-ended questions from concepts.
    This version is rule-based (no LLM needed).
    """
    questions: List[QuizQuestion] = []

    base_templates = [
        "Analyze the key principles underlying {concept} and discuss their theoretical foundations.",
        "Compare and contrast {concept} with alternative approaches in the field.",
        "Critically evaluate the strengths and limitations of {concept} in contemporary applications.",
        "Synthesize how {concept} integrates with other major theories or frameworks in this domain.",
        "Propose a research question or hypothesis that could advance our understanding of {concept}.",
        "Examine the historical development of {concept} and its impact on current practices.",
        "Design an experiment or case study to demonstrate the practical implications of {concept}.",
        "Evaluate how {concept} addresses real-world problems and assess its efficacy.",
        "Discuss the ethical implications and societal impact of applying {concept}.",
        "Deconstruct the assumptions embedded in {concept} and analyze their validity.",
        "Explain how {concept} can be applied to solve interdisciplinary challenges.",
        "Assess the empirical evidence supporting or refuting the claims of {concept}.",
        "Formulate a counterargument to the prevailing interpretations of {concept}.",
        "Trace the evolution of {concept} from foundational theory to modern implementation.",
        "Analyze a case where {concept} failed to achieve expected outcomes and explain why.",
        "Justify the relevance of {concept} in addressing current societal or technological trends.",
        "Predict future developments in {concept} based on current research trajectories.",
        "Articulate how {concept} challenges or reinforces existing paradigms in the discipline.",
    ]

    # Cycle through templates for each concept
    for concept in concepts:
        for template in base_templates:
            if len(questions) >= num_questions:
                break
            q_text = template.format(concept=concept)
            questions.append(QuizQuestion(text=q_text))
        if len(questions) >= num_questions:
            break

    # Fallback if no concepts
    if not questions:
        questions.append(
            QuizQuestion(
                text="Summarize the main idea of the material in 3–5 sentences."
            )
        )

    return questions[:num_questions]


def update_mastery(
    mastery: Dict[str, float],
    studied_concepts: List[str],
    delta: float = 0.05,
) -> Dict[str, float]:
    """
    Very simple mastery update rule:
    - For each studied concept, increase mastery slightly.
    - Cap between 0.0 and 1.0.

    In a real system, this would use quiz results instead of a flat increment.
    """
    updated = mastery.copy()
    for concept in studied_concepts:
        current = updated.get(concept, 0.3)
        new_score = max(0.0, min(current + delta, 1.0))
        updated[concept] = new_score
    return updated
