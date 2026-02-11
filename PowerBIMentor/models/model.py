"""Abstract base model for PowerBIMentor evaluators."""

from abc import ABC, abstractmethod
from typing import Any, Dict


def build_content(question: str, answer: str, prompt: str) -> str:
    """Build the evaluation prompt for text-based evaluations.

    Args:
        question: The assignment question
        answer: The student's answer
        prompt: Evaluation instructions

    Returns:
        Formatted prompt string
    """
    return f"""
            Instruction:
            {prompt.strip()}

            Question:
            {question.strip()}

            Answer:
            {answer.strip()}

            Return ONLY valid JSON in the following format.
            DO NOT add explanations, markdown, or extra text.
            DO NOT wrap in ```.

            JSON schema:
            {{
              "score": number (0-100),
              "feedback": string
            }}
    """.strip()


def build_visual_content(question: str, prompt: str) -> str:
    """Build the evaluation prompt for visual/PDF evaluations.

    Args:
        question: The assignment question
        prompt: Evaluation instructions

    Returns:
        Formatted prompt string
    """
    return f"""
        Instruction:
        {prompt.strip()}

        Question:
        {question.strip()}

        Use ONLY the provided visual document (PDF or images) to answer.
        Do NOT rely on prior knowledge.
        If information is missing, reflect that in the feedback.

        Return ONLY valid JSON in the following format.
        DO NOT add explanations, markdown, or extra text.
        DO NOT wrap in ```.

        JSON schema:
        {{
          "score": number (0-100),
          "feedback": string
        }}
    """.strip()


class Model(ABC):
    """Abstract base class for AI model evaluators.

    All model implementations must inherit from this class and implement
    the evaluate method.
    """

    def __init__(self):
        """Initialize the model."""
        pass

    @abstractmethod
    def evaluate(self, question: str, answer: str, prompt: str) -> Dict[str, Any]:
        """Evaluate an answer to a question using the AI model.

        Args:
            question: The question or assignment prompt
            answer: The student's answer or solution
            prompt: Evaluation criteria and instructions for the model

        Returns:
            Dictionary with 'score' (0-100) and 'feedback' (string)
        """
        pass
