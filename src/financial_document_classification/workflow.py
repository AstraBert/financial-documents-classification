"""
Financial Document Classification Workflow

Classifies PDF financial documents into:
- Cash Flow Statement
- Income Statement
- Balance Sheet
"""

import os
from workflows import Workflow, step, Context
from workflows.events import StartEvent, StopEvent
from llama_cloud.types import ClassifierRule
from llama_cloud_services.beta.classifier.client import ClassifyClient

from financial_document_classification.models import ClassificationResult
from financial_document_classification.events import ClassifyEvent


class FinancialDocumentClassifier(Workflow):
    """
    Workflow for classifying financial documents.

    Input: file_paths (list of PDF paths)
    Output: List of ClassificationResult objects
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        if not api_key:
            raise ValueError("LLAMA_CLOUD_API_KEY environment variable must be set")
        self.classifier = ClassifyClient.from_api_key(api_key)

        # Define classification rules for financial documents
        self.rules = [
            ClassifierRule(
                type="cash_flow_statement",
                description="A financial statement showing cash inflows and outflows from operating, investing, and financing activities over a period of time",
            ),
            ClassifierRule(
                type="income_statement",
                description="A financial statement showing revenues, expenses, and profit or loss over a specific period, also known as profit and loss statement or P&L",
            ),
            ClassifierRule(
                type="balance_sheet",
                description="A financial statement showing assets, liabilities, and shareholders' equity at a specific point in time",
            ),
        ]

    @step
    async def classify_documents(
        self, ev: StartEvent, ctx: Context
    ) -> ClassifyEvent:
        """Classify all input documents"""
        file_paths = ev.file_paths
        if not isinstance(file_paths, list):
            file_paths = [file_paths]

        results = []
        for file_path in file_paths:
            # Classify the document
            classification = await self.classifier.aclassify_file_path(
                rules=self.rules,
                file_input_path=file_path,
            )

            # Extract result
            result = classification.items[0].result
            results.append(
                ClassificationResult(
                    file_path=file_path,
                    document_type=result.type,
                    confidence=result.confidence,
                    reasoning=result.reasoning,
                )
            )

        return ClassifyEvent(results=results)

    @step
    async def finalize_results(
        self, ev: ClassifyEvent, ctx: Context
    ) -> StopEvent:
        """Return final classification results"""
        return StopEvent(result=ev.results)


# Create workflow instance
workflow = FinancialDocumentClassifier(timeout=300)
