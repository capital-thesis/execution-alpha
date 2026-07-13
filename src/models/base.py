from dataclasses import dataclass
from scipy.optimize import newton

@dataclass
class LBOModel:
    name: str
    entry_ebitda: float
    entry_multiple: float
    exit_ebitda: float
    exit_multiple: float
    debt_raised: float
    equity_invested: float
    holding_period: int = 5
    annual_debt_paydown: float = None
    
    @property
    def entry_enterprise_value(self) -> float:
        return self.entry_ebitda * self.entry_multiple
    
    @property
    def exit_enterprise_value(self) -> float:
        return self.exit_ebitda * self.exit_multiple
    
    @property
    def exit_debt_remaining(self) -> float:
        if self.annual_debt_paydown:
            return max(0, self.debt_raised - (self.annual_debt_paydown * self.holding_period))
        return self.debt_raised
    
    @property
    def exit_equity_value(self) -> float:
        return self.exit_enterprise_value - self.exit_debt_remaining
    
    @property
    def equity_uplift(self) -> float:
        return self.exit_equity_value - self.equity_invested
    
    @property
    def moic(self) -> float:
        if self.equity_invested <= 0:
            return 0
        return self.exit_equity_value / self.equity_invested
    
    @property
    def irr(self) -> float:
        cash_flows = [-self.equity_invested] + [0] * (self.holding_period - 1) + [self.exit_equity_value]
        
        def npv(rate):
            return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))
        
        try:
            return newton(npv, 0.15) * 100
        except:
            return 0
