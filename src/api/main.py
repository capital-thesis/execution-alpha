from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.models.base import LBOModel
from src.cases.saas_platform import create_saas_case
from src.cases.logistics_services import create_logistics_case
from src.cases.ltg_analytics import create_ltg_case


app = FastAPI(
    title="execution-alpha",
    description="Production LBO Modeling Engine",
    version="1.0.0",
)


class LBORequest(BaseModel):
    name: str
    entry_ebitda: float
    entry_multiple: float
    exit_ebitda: float
    exit_multiple: float
    debt_raised: float
    equity_invested: float
    holding_period: int = 5
    annual_debt_paydown: float = None


class LBOResponse(BaseModel):
    name: str
    entry_ev: float
    exit_ev: float
    equity_uplift: float
    moic: float
    irr: float


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "execution-alpha"}


@app.post("/models/scenario", response_model=LBOResponse)
def run_scenario(request: LBORequest):
    """Run a single LBO scenario."""
    try:
        model = LBOModel(
            name=request.name,
            entry_ebitda=request.entry_ebitda,
            entry_multiple=request.entry_multiple,
            exit_ebitda=request.exit_ebitda,
            exit_multiple=request.exit_multiple,
            debt_raised=request.debt_raised,
            equity_invested=request.equity_invested,
            holding_period=request.holding_period,
            annual_debt_paydown=request.annual_debt_paydown,
        )
        
        return LBOResponse(
            name=model.name,
            entry_ev=model.entry_enterprise_value,
            exit_ev=model.exit_enterprise_value,
            equity_uplift=model.equity_uplift,
            moic=model.moic,
            irr=model.irr,
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/cases/ltg")
def get_ltg_case():
    """Get LTG Analytics case summary."""
    model = create_ltg_case()
    return {
        "name": model.name,
        "entry_ev": model.entry_enterprise_value,
        "exit_ev": model.exit_enterprise_value,
        "irr": model.irr,
        "moic": model.moic,
    }


@app.get("/cases/saas")
def get_saas_case():
    """Get SaaS case summary."""
    model = create_saas_case()
    return {
        "name": model.name,
        "entry_ev": model.entry_enterprise_value,
        "exit_ev": model.exit_enterprise_value,
        "irr": model.irr,
        "moic": model.moic,
    }


@app.get("/cases/logistics")
def get_logistics_case():
    """Get Logistics case summary."""
    model = create_logistics_case()
    return {
        "name": model.name,
        "entry_ev": model.entry_enterprise_value,
        "exit_ev": model.exit_enterprise_value,
        "irr": model.irr,
        "moic": model.moic,
    }
