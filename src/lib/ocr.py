from abc import ABC, abstractmethod
from typing import Optional
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
import os

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
# Create processor before running sample
PROCESSOR_ID = os.environ.get("PROCESSOR_ID")

# Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
MIME_TYPE = "application/pdf"
# Optional. The fields to return in the Document object.
FIELD_MASK = "text,entities,pages.pageNumber"
# Optional. Processor version to use
PROCESSOR_VERSION_ID = "pretrained-ocr-v2.0-2023-06-02"


class OCRBase(ABC):
    @abstractmethod
    def process_pdf(self, pdf_path, *args, **kwargs) -> str:
        pass


class OCRDocumentAI(OCRBase):
    def __init__(
        self,
        project_id: str = PROJECT_ID,
        location: str = LOCATION,
        processor_id: str = PROCESSOR_ID,
        mime_type: str = MIME_TYPE,
        field_mask: Optional[str] = FIELD_MASK,
        processor_version_id: Optional[str] = PROCESSOR_VERSION_ID,
    ):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.mime_type = mime_type
        self.field_mask = field_mask
        self.processor_version_id = processor_version_id

    def process_pdf(self, pdf_path) -> str:
        # You must set the `api_endpoint` if you use a location other than "us".
        opts = ClientOptions(api_endpoint=f"{self.location}-documentai.googleapis.com")

        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        if self.processor_version_id:
            # The full resource name of the processor version, e.g.:
            # `projects/{project_id}/self.s/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
            name = client.processor_version_path(
                self.project_id, self.location, self.processor_id, self.processor_version_id
            )
        else:
            # The full resource name of the processor, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}`
            name = client.processor_path(
                self.project_id, self.location, self.processor_id)

        # Read the file into memory
        with open(pdf_path, "rb") as image:
            image_content = image.read()

        # Load binary data
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=self.mime_type)

        # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
        # Optional: Additional configurations for processing.
        process_options = documentai.ProcessOptions(
            # Process only specific pages
            individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
                pages=[1]
            )
        )

        # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=raw_document,
            field_mask=self.field_mask,
            process_options=process_options
        )

        result = client.process_document(request=request)

        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        document = result.document

        # Read the text recognition output from the processor
        return document.text
