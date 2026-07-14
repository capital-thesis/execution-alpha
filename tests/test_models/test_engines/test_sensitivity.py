import pytest
import pandas as pd
from src.models.base import LBOModel
from src.models.engines.sensitivity import SensitivityAnalyzer


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
    return SensitivityAnalyzer(ltg_model)


def test_sensitivity_analyzer_init(analyzer):
    assert analyzer.base_model.name == "LTG Analytics"
    assert analyzer.scenarios is None


def test_generate_scenarios_returns_dataframe(analyzer):
    scenarios = analyzer.generate_scenarios(num_scenarios=100)
    assert isinstance(scenarios, pd.DataFrame)
    assert len(scenarios) == 100


def test_generate_scenarios_has_required_columns(analyzer):
    scenarios = analyzer.generate_scenarios(num_scenarios=100)
    required_cols = ["scenario_id", "entry_multiple", "growth_cagr", "exit_multiple", "irr", "moic"]
    assert all(col in scenarios.columns for col in required_cols)


def test_generate_scenarios_irr_range(analyzer):
    scenarios = analyzer.generate_scenarios(num_scenarios=100)
    irr_min = scenarios["irr"].min()
    irr_max = scenarios["irr"].max()
    assert irr_max > irr_min


def test_generate_scenarios_moic_range(analyzer):
    scenarios = analyzer.generate_scenarios(num_scenarios=100)
    moic_min = scenarios["moic"].min()
    moic_max = scenarios["moic"].max()
    assert moic_max > moic_min


def test_top_scenarios(analyzer):
    analyzer.generate_scenarios(num_scenarios=100)
    top_10 = analyzer.top_scenarios(n=10, sort_by="irr")
    assert len(top_10) == 10
    assert top_10["irr"].iloc[0] >= top_10["irr"].iloc[1]


def test_sensitivity_table(analyzer):
    analyzer.generate_scenarios(num_scenarios=100)
    pivot = analyzer.sensitivity_table("entry_multiple", "growth_cagr", metric="irr")
    assert isinstance(pivot, pd.DataFrame)
    assert pivot.shape[0] > 0
    assert pivot.shape[1] > 0


def test_error_if_no_scenarios_generated(analyzer):
    with pytest.raises(ValueError):
        analyzer.top_scenarios()


def test_error_sensitivity_no_scenarios(analyzer):
    with pytest.raises(ValueError):
        analyzer.sensitivity_table("entry_multiple", "growth_cagr")


def test_1000_scenario_generation(analyzer):
    scenarios = analyzer.generate_scenarios(num_scenarios=1000)
    assert len(scenarios) == 1000
    assert scenarios["irr"].mean() > 0
