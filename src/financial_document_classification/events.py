"""
Workflow events for financial document classification.
"""

from workflows.events import Event
from financial_document_classification.models import ClassificationResult


class ClassifyEvent(Event):
    """Event containing classification results"""

    results: list[ClassificationResult]
