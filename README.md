# execution-alpha

Production LBO modeling engine for capital-thesis positioning.

## Quick Start

```bash
python -m pytest tests/
```

## Cases

- LTG Analytics (25.1% IRR)
- SaaS Platform (coming week 2)
- Logistics (coming week 2)

## Run Model

```python
from src.models.base import LBOModel

ltg = LBOModel(
    name="LTG Analytics",
    entry_ebitda=24.8,
    entry_multiple=9.0,
    exit_ebitda=49.6,
    exit_multiple=11.0,
    debt_raised=150.0,
    equity_invested=181.3,
    annual_debt_paydown=15.0,
)

print(f"IRR: {ltg.irr:.1f}%")
print(f"MoIC: {ltg.moic:.2f}x")
```
