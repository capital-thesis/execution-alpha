from src.models.base import LBOModel

def create_saas_case() -> LBOModel:
    """
    SaaS Platform LBO Case
    
    Assumptions:
    - Entry EBITDA: £15.0m (SaaS, high margins)
    - Entry Multiple: 7.0x (SaaS trades lower on growth)
    - Exit EBITDA: £45.0m (30% CAGR growth)
    - Exit Multiple: 9.0x
    - Debt: £80.0m
    - Equity: £105.0m
    - Hold: 5 years
    - Debt paydown: £10.0m/year
    
    Returns:
        LBOModel instance for SaaS case
    """
    
    return LBOModel(
        name="SaaS Platform LBO",
        entry_ebitda=15.0,
        entry_multiple=7.0,
        exit_ebitda=45.0,
        exit_multiple=9.0,
        debt_raised=80.0,
        equity_invested=105.0,
        holding_period=5,
        annual_debt_paydown=10.0,
    )