import pytest
from src.cases.saas_platform import create_saas_case
from src.cases.logistics_services import create_logistics_case

@pytest.fixture
def saas_case():
    return create_saas_case()

@pytest.fixture
def logistics_case():
    return create_logistics_case()

def test_saas_case_creation(saas_case):
    assert saas_case.name == "SaaS Platform LBO"
    assert saas_case.entry_ebitda == 15.0
    assert saas_case.entry_multiple == 7.0
    
def test_saas_case_entry_ev(saas_case):
    expected = 15.0 * 7.0
    assert saas_case.entry_enterprise_value == expected
    
def test_saas_case_irr(saas_case):
    irr = saas_case.irr
    assert 15 < irr < 35  # SaaS should have higher IRR (growth)
    
def test_saas_case_moic(saas_case):
    moic = saas_case.moic
    assert moic > 2.0  # SaaS growth should drive good returns
    
def test_logistics_case_creation(logistics_case):
    assert logistics_case.name == "Logistics Services LBO"
    assert logistics_case.entry_ebitda == 30.0
    assert logistics_case.entry_multiple == 6.5
    
def test_logistics_case_entry_ev(logistics_case):
    expected = 30.0 * 6.5
    assert logistics_case.entry_enterprise_value == expected

def test_logistics_case_irr(logistics_case):
    irr = logistics_case.irr
    assert 15 < irr < 30

def test_logistics_case_moic(logistics_case):
    moic = logistics_case.moic
    assert moic > 2.0
