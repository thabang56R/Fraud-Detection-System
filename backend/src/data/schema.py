from pydantic import BaseModel, Field


class TransactionRecord(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID")
    customer_id: str = Field(..., description="Unique customer ID")
    merchant_id: str = Field(..., description="Unique merchant ID")
    amount: float = Field(..., ge=0, description="Transaction amount")
    currency: str = Field(..., min_length=3, max_length=3)
    country: str = Field(..., min_length=2, max_length=2)
    device_type: str
    ip_address: str
    timestamp: str
    is_fraud: int = Field(..., ge=0, le=1)