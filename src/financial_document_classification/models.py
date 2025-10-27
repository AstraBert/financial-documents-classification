"""
Pydantic models for financial document classification.
"""

from pydantic import BaseModel


class ClassificationResult(BaseModel):
    """Result of classifying a single document"""

    file_path: str
    document_type: str
    confidence: float
    reasoning: str
