import pytest
from src.models.base import LBOModel

@pytest.fixture
def ltg_model():
    return LBOModel(
        name="LTG Analytics",
        entry_ebitda=24.8,
        entry_multiple=9.0,
        exit_ebitda=49.6,
        exit_multiple=11.0,
        debt_raised=150.0,
        equity_invested=181.3,
        holding_period=5,
        annual_debt_paydown=15.0,
    )

def test_ltg_entry_ev(ltg_model):
    expected = 24.8 * 9.0
    assert ltg_model.entry_enterprise_value == expected

def test_ltg_exit_ev(ltg_model):
    expected = 49.6 * 11.0
    assert ltg_model.exit_enterprise_value == expected

def test_ltg_irr(ltg_model):
    irr = ltg_model.irr
    assert 20 < irr < 22, f"Expected ~21%, got {irr}"

def test_ltg_moic(ltg_model):
    moic = ltg_model.moic
    assert 2.5 < moic < 2.7, f"Expected ~2.6x, got {moic}"
