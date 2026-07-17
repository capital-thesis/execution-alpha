from src.models.base import LBOModel


def create_ltg_case() -> LBOModel:
    """
    LTG Analytics LBO Case
    
    Assumptions:
    - Entry EBITDA: £24.8m
    - Entry Multiple: 9.0x
    - Exit EBITDA: £49.6m (100% growth, 15% CAGR)
    - Exit Multiple: 11.0x
    - Debt: £150.0m
    - Equity: £181.3m
    - Hold: 5 years
    - Debt paydown: £15.0m/year
    
    Returns:
        LBOModel instance for LTG case
    """
    return LBOModel(
        name="LTG Analytics LBO",
        entry_ebitda=24.8,
        entry_multiple=9.0,
        exit_ebitda=49.6,
        exit_multiple=11.0,
        debt_raised=150.0,
        equity_invested=181.3,
        holding_period=5,
        annual_debt_paydown=15.0,
    )
