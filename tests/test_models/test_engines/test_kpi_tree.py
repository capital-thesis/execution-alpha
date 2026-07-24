import pytest
from src.models.engines.kpi_tree import KPITreeBuilder, KPINode


@pytest.fixture
def saas_kpi_builder():
    return KPITreeBuilder(financial_target=45.0, base_metric="EBITDA")


@pytest.fixture
def logistics_kpi_builder():
    return KPITreeBuilder(financial_target=52.5, base_metric="EBITDA")


def test_kpi_node_creation():
    kpi = KPINode(name="NRR", target=115.0, unit="%", owner="VP Product")
    assert kpi.name == "NRR"
    assert kpi.target == 115.0
    assert kpi.unit == "%"
    
    
def test_saas_kpi_tree_build(saas_kpi_builder):
    tree = saas_kpi_builder.build_saas_kpi_tree(entry_ebitda=15.0)
    assert "Exit EBITDA Target" in tree
    assert "Revenue KPIs" in tree
    assert "Margin KPIs" in tree
    assert "OpEx KPIs" in tree


def test_logistics_kpi_tree_build(logistics_kpi_builder):
    tree = logistics_kpi_builder.build_logistics_kpi_tree(entry_ebitda=30.0)
    assert "Exit EBITDA Target" in tree
    assert "Revenue KPIs" in tree
    assert "Margin KPIs" in tree
    assert "Efficiency KPIs" in tree


def test_flatten_tree(saas_kpi_builder):
    saas_kpi_builder.build_saas_kpi_tree(entry_ebitda=15.0)
    flat = saas_kpi_builder.flatten_tree()
    assert len(flat) > 0
    assert all ("name" in kpi and "target" in kpi for kpi in flat)
    
    
def test_get_summary(saas_kpi_builder):
    saas_kpi_builder.build_saas_kpi_tree(entry_ebitda=15.0)
    summary = saas_kpi_builder.get_summary()
    assert "KPI Tree Summary" in summary
    assert "NRR" in summary or "Margin" in summary 
