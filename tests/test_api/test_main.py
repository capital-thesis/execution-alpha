import pytest
from fastapi.testclient import TestClient
from src.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_ltg_case():
    response = client.get("/cases/ltg")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "LTG Analytics LBO"
    assert data["irr"] > 20


def test_get_saas_case():
    response = client.get("/cases/saas")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SaaS Platform LBO"


def test_get_logistics_case():
    response = client.get("/cases/logistics")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Logistics Services LBO"


def test_run_scenario():
    payload = {
        "name": "Test Scenario",
        "entry_ebitda": 24.8,
        "entry_multiple": 9.0,
        "exit_ebitda": 49.6,
        "exit_multiple": 11.0,
        "debt_raised": 150.0,
        "equity_invested": 181.3,
        "holding_period": 5,
        "annual_debt_paydown": 15.0,
    }
    response = client.post("/models/scenario", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["irr"] > 20
    assert data["moic"] > 2.0
