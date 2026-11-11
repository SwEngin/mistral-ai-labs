"""Invoice models for the document annotation exercise."""

from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    description: str
    quantity: float
    # TODO 1 (Required): Add unit_price and total_price as floats.


class Invoice(BaseModel):
    invoice_number: str
    supplier_name: str
    invoice_date: str
    due_date: str | None = None
    currency: str
    items: list[InvoiceItem]
    # TODO 2 (Required): Add nullable subtotal and tax_amount fields with
    # defaults of None, and a required total_amount field.
    supplier_vat_id: str | None = Field(
        default=None, description="VAT ID if explicitly present"
    )
    # TODO 5 (Exploration): Add an optional purchase_order_number field.
