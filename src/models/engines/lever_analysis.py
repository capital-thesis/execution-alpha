from src.models.base import LBOModel

class LeverAnalyzer:
    """Analyze impact of each value creation lever"""
    
    def __init__(self, base_model: LBOModel):
        self.base_model = base_model
        self.base_irr = base_model.irr
        
    def analyze_lever(self, lever: str, delta: float) -> dict:
        """
        Shock one lever, measure IRR impact.
        
        Args:
            lever: Name of lever (e.g., "ebitda_growth", "entry_multiple", "exit_multiple", "debt_paydown")
            delta: Change to apply
            
        Returns:
            Dict with lever impact metrics
        """
        
        stressed_model = LBOModel(
            name=f"{self.base_model.name} ({lever})",
            entry_ebitda=self.base_model.entry_ebitda,
            entry_multiple=self.base_model.entry_multiple,
            exit_ebitda=self.base_model.exit_ebitda,
            exit_multiple=self.base_model.exit_multiple,
            debt_raised=self.base_model.debt_raised,
            equity_invested=self.base_model.equity_invested,
            holding_period=self.base_model.holding_period,
            annual_debt_paydown=self.base_model.annual_debt_paydown,
        )
        
        # Apply lever shock
        if lever == "ebitda_growth":
            stressed_model.exit_ebitda = self.base_model.entry_ebitda * (
                (1 + delta) ** self.base_model.holding_period
            )
        
        elif lever == "entry_multiple":
            stressed_model.entry_ebitda = self.base_model.entry_multiple + delta
        
        elif lever == "exit_multiple":
            stressed_model.exit_ebitda = self.base_model.exit_multiple + delta
        
        elif lever == "debt_paydown":
            stressed_model.annual_debt_paydown = (
                self.base_model.annual_debt_paydown or 0
            )    + delta
        
        stressed_irr = stressed_model.irr
        irr_impact_bps = (stressed_irr - self.base_irr) * 100
        
        return {
            "lever": lever,
            "baseline_irr": round(self.base_irr, 2),
            "stressed_irr": round(stressed_irr, 2),
            "irr_impact_bps": round(irr_impact_bps, 0),
            "moic_baseline": round(self.base_model.moic, 2),
            "moic_stressed": round(stressed_model.moic, 2),
        }
    
    def analyze_all_levers(self) -> list:
        """Analyze all major levers."""
        levers = [
            ("ebitda_growth", 0.05),       # +5 CAGR
            ("entry_multiple", 0.05),       # +0.5x
            ("exit_multiple", 0.05),       # +0.5x
            ("debt_paydown", 10.0),       # +£10m
        ]
        
        results = [self.analyze_lever(lever, delta) for lever, delta in levers]
        return sorted(results, key=lambda x: x["irr_impact_bps"], reverse=True)