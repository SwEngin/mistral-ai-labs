"""
Data Models for Structured Product Extraction

Define the schema for structured product specifications.
Pydantic validates that responses match this schema.
"""

from typing import Optional, Literal
from pydantic import BaseModel


class ProductSpecifications(BaseModel):
    """
    Structured representation of product specifications.
    
    Category is required and must be one of the allowed values.
    All other fields are optional—use None to represent missing information.
    
    Do not invent specifications. If a field is not explicitly stated 
    in the product description, it should be None.
    """
    # TODO 1: Complete this schema by adding the fields below
    
    # Required: category must be one of these exact values
    category: Literal["battery", "charger", "other"]
    
    # Optional fields: define all of these with Optional[str] = None
    # TODO: Add fields for:
    # - product_name (e.g., "BX-3000 Ultra Lithium")
    # - manufacturer (e.g., "TechPower Industries")
    # - capacity (e.g., "5000 mAh")
    # - voltage (e.g., "3.7V")
    # - weight (e.g., "185g")
    # - operating_temperature_range (e.g., "0°C to 45°C")
    # - certifications (e.g., "CE, FCC, RoHS")
    #
    # Example of correct syntax in Python 3.10+:
    # product_name: str | None = None
    # 
    # Or with older Python:
    # from typing import Optional
    # product_name: Optional[str] = None


# You can optionally define additional schemas for bonus challenges:
# - SolarPanelSpecifications
# - ChargerSpecifications
# - BaseProductSchema (parent class)
# But these are not required for Lab 4.
