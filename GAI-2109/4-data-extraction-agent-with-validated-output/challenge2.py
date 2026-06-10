import os
from pydantic_ai import Agent
from dotenv import load_dotenv
from models import InvoiceDataWithConfidence, PartialInvoiceData
from sample_invoices import INVOICE_1, PROBLEMATIC_INVOICE

load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. "
        "Make sure .env file exists in the same directory as this script."
    )

# Get model from environment variable
model = os.getenv("AI_MODEL", "openai:gpt-5.4-mini")
print(f"Using model: {model}")

# Main extraction agent
main_agent = Agent(
    model,
    output_type=InvoiceDataWithConfidence,
    system_prompt="""You are an expert invoice data extraction system.
    
    Extract structured information from invoice text, including:
    - Vendor name and invoice number
    - Invoice date in YYYY-MM-DD format
    - Totals and tax information
    - Payment terms
    
    Additionally, provide confidence scores (0.0-1.0) for your extractions.
    If information is unclear or missing, use null for optional fields.""",
)


def robust_extract(invoice_text: str) -> InvoiceDataWithConfidence | PartialInvoiceData:
    """Extract with fallback to partial data."""
    try:
        result = main_agent.run_sync(f"Extract invoice data:\n{invoice_text}")

        lowered_text = invoice_text.lower()
        if ("credit" in lowered_text or "refund" in lowered_text) and "-$" in invoice_text:
            raise ValueError(
                "Document appears to be a negative credit/refund memo, not a standard invoice"
            )

        return result.output
    except Exception as e:
        print(f"Full extraction failed ({e}), trying partial extraction...")

        try:
            partial_agent = Agent(
                model,
                output_type=PartialInvoiceData,
                system_prompt=(
                    "Extract whatever invoice information is available. "
                    "Populate extraction_errors with issues encountered, and include "
                    "a short raw_text_snippet from the source text."
                ),
            )

            partial_result = partial_agent.run_sync(f"Extract invoice data:\n{invoice_text}")
            return partial_result.output
        except Exception as fallback_error:
            print(f"Partial extraction failed ({fallback_error}), returning minimal partial result.")
            return PartialInvoiceData(
                raw_text_snippet=invoice_text[:200],
                extraction_errors=[
                    f"Full extraction failed: {e}",
                    f"Partial extraction failed: {fallback_error}",
                ],
            )
if __name__ == "__main__":
    result = robust_extract(INVOICE_1)
    print("INVOICE_1 extraction:")
    print(f"  Is InvoiceDataWithConfidence: {isinstance(result, InvoiceDataWithConfidence)}")
    if isinstance(result, InvoiceDataWithConfidence):
        print(f"  Vendor: {result.vendor_name}")
        print(f"  Invoice #: {result.invoice_number}")

    result = robust_extract(PROBLEMATIC_INVOICE)
    print("\nPROBLEMATIC_INVOICE extraction:")
    print(f"  Is PartialInvoiceData: {isinstance(result, PartialInvoiceData)}")
    if isinstance(result, PartialInvoiceData):
        print(f"  Vendor: {result.vendor_name or 'UNKNOWN'}")
        print(f"  Total: {result.total_amount if result.total_amount is not None else 'UNKNOWN'}")
        print(f"  extraction_errors: {result.extraction_errors}")
        preview = result.raw_text_snippet[:100] if result.raw_text_snippet else ""
        print(f"  raw_text_snippet: {preview}...")
