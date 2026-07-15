import pytest
from src.models.base import LBOModel
from src.models.engines.lever_analysis import LeverAnalyzer

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

@pytest.fixture
def analyzer(ltg_model):
    return LeverAnalyzer(ltg_model)

def test_lever_analyzer_init(analyzer, ltg_model):
    assert analyzer.base_model.name == "LTG Analytics"
    assert analyzer.base_irr == ltg_model.irr

def test_analyze_ebitda_growth_lever(analyzer):
    result = analyzer.analyze_lever("ebitda_growth", 0.10)
    assert result["lever"] == "ebitda_growth"
    assert "irr_impact_bps" in result

def test_analyze_entry_multiple_lever(analyzer):
    result = analyzer.analyze_lever("entry_multiple", 0.5)
    assert result["lever"] == "entry_multiple"
    assert "irr_impact_bps" in result

def test_analyze_exit_multiple_lever(analyzer):
    result = analyzer.analyze_lever("exit_multiple", 0.5)
    assert result["lever"] == "exit_multiple"
    assert "irr_impact_bps" in result

def test_analyze_debt_paydown_lever(analyzer):
    result = analyzer.analyze_lever("debt_paydown", 10.0)
    assert result["lever"] == "debt_paydown"
    assert result["irr_impact_bps"] > 0

def test_analyze_all_levers_returns_list(analyzer):
    results = analyzer.analyze_all_levers()
    assert isinstance(results, list)
    assert len(results) == 4

def test_analyze_all_levers_sorted_by_impact(analyzer):
    results = analyzer.analyze_all_levers()
    for i in range(len(results) - 1):
        assert results[i]["irr_impact_bps"] >= results[i + 1]["irr_impact_bps"]
        