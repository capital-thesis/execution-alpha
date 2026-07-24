from dataclasses import dataclass
from typing import Dict, List


@dataclass
class KPINode:
    """Represents a single KPI in the tree."""
    name: str
    target: float
    current: float = None
    unit: str = ""  # e.g., "£m", "%", "units"
    owner: str = ""
    frequency: str = "weekly"  # tracking frequency


class KPITreeBuilder:
    """Build hierarchical KPI trees for operational targets."""
    
    def __init__(self, financial_target: float, base_metric: str = "EBITDA"):
        """
        Args:
            financial_target: Exit EBITDA or revenue target
            base_metric: "EBITDA" or "Revenue"
        """
        self.financial_target = financial_target
        self.base_metric = base_metric
        self.tree = {}
        
    def build_saas_kpi_tree(self, entry_ebitda: float) -> Dict:
        """
        Build SaaS KPI hierarchy.
        Entry EBITDA £15m → Exit EBITDA £45m (£30m uplift)
        """
        ebitda_uplift = self.financial_target - entry_ebitda
        
        tree = {
            "Exit EBITDA Target": KPINode(
                name="Exit EBITDA Target",
                target=self.financial_target,
                unit="£m",
                owner="CFO"
            ),
            "Revenue KPIs" : {
                "Land (New ARR)": KPINode(
                    name="New Customer ARR",
                    target=15.0,
                    unit="£m",
                    owner="VP Sales",
                    frequency="monthly"
                ),
                "Expand (Exisitng ARR)": KPINode(
                    name="Expansion Revenue",
                    target=10.0,
                    unit="£m",
                    owner="VP CSM",
                    frequency="monthly"
                ),
                "NRR": KPINode(
                    name="Net Revenue Retention",
                    target=115.0,
                    unit="%",
                    owner="VP Product",
                    frequency="monthly"
                ),
            },
            "Margin KPIs" : {
                "Gross Margin": KPINode(
                    name="Gross Margin",
                    target=77.0,
                    unit="%",
                    owner="VP Ops",
                    frequency="monthly"
                ),
                "COGS per Customer": KPINode(
                    name="COGS Efficiency",
                    target=-8.0,  # -8% reduction
                    unit="%",
                    owner="VP Ops",
                    frequency="quarterly"
                ),
            },
            "OpEx KPIs" : {
                "S&M Spend": KPINode(
                    name="Sales & Marketing Spend",
                    target=0.0,  # flat while revenue doubles
                    unit="% growth",
                    owner="CFO",
                    frequency="monthly"
                ),
                "G&A Ratio": KPINode(
                    name="G&A as % of Revenue",
                    target=8.0,  # down from 12%
                    unit="%",
                    owner="CFO",
                    frequency="monthly"
                ),
            },
        }
        
        self.tree = tree
        return tree
    
    def build_logistics_kpi_tree(self, entry_ebitda: float) -> Dict:
        """
        Build Logistics KPI hierarchy.
        Entry EBITDA £30m → Exit EBITDA £52.5m (£22.5m uplift)
        """
        tree = {
            "Exit EBITDA Target": KPINode(                
                name="Exit EBITDA Target",
                target=self.financial_target,
                unit="£m",
                owner="CFO"
            ),
            "Revenue KPIs" : {
                "Organic Growth": KPINode(
                    name="Revenue Growth CAGR",
                    target=5.0,
                    unit="%",
                    owner="VP Sales",
                    frequency="annual"
                ),
                "Pricing": KPINode(
                    name="Average Rate Increase",
                    target=3.0,
                    unit="%",
                    owner="VP Sales",
                    frequency="quarterly"
                ),
            },
            "Margin KPIs" : {
                "EBITDA Margin": KPINode(
                    name="EBITDA Margin",
                    target=20.0,
                    unit="%",
                    owner="CFO",
                    frequency="monthly"
                ),
                "Cost per Shipment": KPINode(
                    name="Cost per Shipment",
                    target=-3.0,  # -3% reduction
                    unit="%",
                    owner="VP Ops",
                    frequency="monthly"
                ),
            },
            "Efficiency KPIs" : {
                "Headcount Productivity": KPINode(
                    name="Revenue per FTE",
                    target=250.0,
                    unit="£k",
                    owner="HR",
                    frequency="quarterly"
                ),
                "Utilization Rate": KPINode(
                    name="Asset/Vehicle Utilization",
                    target=85.0,
                    unit="%",
                    owner="VP Ops",
                    frequency="weekly"
                ),
            },
        }
                        
        self.tree = tree
        return tree
        
    def flatten_tree(self) -> List[Dict]:
        """Flatten tree to list for easier tracking/reporting."""
        flat_list = []
    
        def traverse(node, parent_name=""):
            if isinstance(node, KPINode):
                flat_list.append({
                    "parent": parent_name,
                    "name": node.name,
                    "target": node.target,
                    "current": node.current,
                    "unit": node.unit,
                    "owner": node.owner,
                    "frequency": node.frequency,
                })
            elif isinstance(node, dict):
                for key, value in node.items():
                    traverse(value, parent_name=key)
                
        traverse(self.tree)
        return flat_list
    
    def get_summary(self) -> str:
        """Generate text summary of KPI tree."""
        flat = self.flatten_tree()
        summary = f"KPI Tree Summary ({len(flat)} total KPIs)\n"
        summary += "=" * 50 + "\n"
        
        for kpi in flat:
            summary += f"{kpi['parent']:20} | {kpi['name']:30} | Target: {kpi['target']}{kpi['unit']}\n"
            
        return summary
