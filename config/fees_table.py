from pydantic import BaseModel


class ColumnConfig(BaseModel):
    column_name: str
    column_values: list[str]


TYPE_OF_FEES_CONFIG = ColumnConfig(
    column_name="Type of fees",
    column_values=[
        "Entrance fee",
        "Distrbution fee",
        "Franchise fee",
        "Termination fee",
        "Sales & Marketing fee",
        "Trademarkroyalty fee",
        "Insurance fee"
    ]
)

BASIS_CONFIG = ColumnConfig(
    column_name="Basis",
    column_values=[
        "Gross Room Revenue",
        "Room Revenue",
        "Web Acquisition Revenue",
        "GDS / IDS Revenue",
        "Total Revenue"
    ]
)

VAT_ON_BASIC_CONFIG = ColumnConfig(
    column_name="VAT on Basis",
    column_values=[
        "INCLUDE",
        "EXCLUDE"
    ]
)

CURRENCY_CODE_CONFIG = ColumnConfig(
    column_name="Currency code",
    column_values=[
        "USD",
        "EUR",
        "GBP",
    ]
)

COLUMNS_CONFIG = [
    TYPE_OF_FEES_CONFIG,
    BASIS_CONFIG,
    VAT_ON_BASIC_CONFIG,
    CURRENCY_CODE_CONFIG
]
