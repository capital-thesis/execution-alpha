from src.models.base import LBOModel

def create_logistics_case() -> LBOModel:
    """
    Logistics Services LBO Case
    
    Assumptions:
    - Entry EBITDA: £30.0m (asset-light model)
    - Entry Multiple: 6.5x (industrials multiple)
    - Exit EBITDA: £52.5m (15% CAGR growth)
    - Exit Multiple: 8.5x
    - Debt: £150.0m
    - Equity: £145.0m
    - Hold: 5 years
    - Debt paydown: £20.0m/year (aggressive)
    
    Returns:
        LBOModel instance for Logistics case
    """
    
    return LBOModel(
        name="Logistics Services LBO",
        entry_ebitda=30.0,
        entry_multiple=6.5,
        exit_ebitda=52.5,
        exit_multiple=8.5,
        debt_raised=150.0,
        equity_invested=145.0,
        holding_period=5,
        annual_debt_paydown=20.0,
    )
    