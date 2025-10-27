"""
Financial Document Classification Package

A workflow-based system for classifying financial documents (PDFs) into:
- Cash Flow Statement
- Income Statement
- Balance Sheet
"""

from financial_document_classification.workflow import (
    FinancialDocumentClassifier,
    workflow,
)
from financial_document_classification.models import ClassificationResult
from financial_document_classification.events import ClassifyEvent

__all__ = [
    "FinancialDocumentClassifier",
    "workflow",
    "ClassificationResult",
    "ClassifyEvent",
]

__version__ = "0.1.0"
