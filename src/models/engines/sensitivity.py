import pandas as pd
import numpy as np
from src.models.base import LBOModel

class SensitivityAnalyzer:
    """Generate and analyze sensitivity scenarios."""
    
    def __init__(self, base_model: LBOModel):
        self.base_model = base_model
        self.scenarios = None
    
    def generate_scenarios(
        self,
        entry_multiple_range: tuple = None,
        growth_cagr_range: tuple = (-5, 10),
        exit_multiple_range: tuple = None,
        debt_paydown_range: tuple = (10, 20),
        num_scenarios: int = 1000,
    ) -> pd.DataFrame:
        """
        Generate random scenarios within specified ranges.
        
        Args:
            entry_multiple_range: (min, max) for entry multiple
            growth_cagr_range: (min, max) for EBITDA growth CAGR %
            exit_multiple_range: (min, max) for exit multiple
            debt_paydown_range: (min, max) annual debt paydown £m
            num_scenarios: number of random scenarios
            
        Returns:
            DataFrame with scenario results
        """
        
        # Set defaults
        entry_min, entry_max = entry_multiple_range or (
            self.base_model.entry_multiple - 0.5,
            self.base_model.entry_multiple + 0.5,
        )
        exit_min, exit_max = exit_multiple_range or (
            self.base_model.exit_multiple - 0.5,
            self.base_model.exit_multiple + 0.5,
        )
        
        scenarios = []
        
        for i in range(num_scenarios):
            # Random parameters
            entry_mult = np.random.uniform(entry_min, entry_max)
            growth_cagr = np.random.uniform(*growth_cagr_range) / 10
            exit_mult = np.random.uniform(exit_min, exit_max)
            debt_paydown = np.random.uniform(*debt_paydown_range)
            
            # Calculate exit EBITDA based on growth
            exit_ebitda = self.base_model.entry_ebitda * (
                (1 + growth_cagr) ** self.base_model.holding_period
            )
            
            # Run scenario
            scenario_model = LBOModel(
                name=f"Scenario_{i}",
                entry_ebitda=self.base_model.entry_ebitda,
                entry_multiple=entry_mult,
                exit_ebitda=exit_ebitda,
                exit_multiple=exit_mult,
                debt_raised=self.base_model.debt_raised,
                equity_invested=self.base_model.equity_invested,
                holding_period=self.base_model.holding_period,
                annual_debt_paydown=debt_paydown,
            )
            
            scenarios.append({
                "scenario_id": i,
                "entry_multiple": entry_mult,
                "growth_cagr": growth_cagr * 100,
                "exit_multiple": exit_mult,
                "debt_paydown": debt_paydown,
                "irr": scenario_model.irr,
                "moic": scenario_model.moic,
                "equity_uplift": scenario_model.equity_uplift,
            })
        
        self.scenarios = pd.DataFrame(scenarios)
        return self.scenarios

    def sensitivity_table(
        self, param1: str, param2: str, metric: str = "irr"
    ) -> pd.DataFrame:
        """
        Create 2D sensitivity table.
        
        Args:
            param1: Column header (e.g., "entry_multiple")
            param2: Row header (e.g., "growth_cagr")
            metric: Output metric ("irr" or "moic")
        
        Returns:
            Pivot table with metric as values
        """
        if self.scenarios is None or self.scenarios.empty:
            raise ValueError("No scenarios generated. Run generate_scenarios() first.")
        
        pivot = self.scenarios.pivot_table(
            values=metric, index=param2, columns=param1, aggfunc="mean"
        )
        return pivot
    
    def top_scenarios(self, n: int = 10, sort_by: str = "irr") -> pd.DataFrame:
        """Return top N scenarios by metric."""
        if self.scenarios is None or self.scenarios.empty:
            raise ValueError("No scenarios generated. Run generate_scenarios() first.")
        return self.scenarios.nlargest(n, sort_by)
