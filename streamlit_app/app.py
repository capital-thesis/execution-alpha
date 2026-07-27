import streamlit as st
from src.models.base import LBOModel
from src.cases.ltg_analytics import create_ltg_case
from src.cases.saas_platform import create_saas_case
from src.cases.logistics_services import create_logistics_case


# Password auth gate
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if not st.session_state.authenticated:
    st.title("🔐 execution-alpha")
    st.write("Enter password to access the LBO modeling engine.")
    
    password = st.text_input("Password:", type="password", key="login_password")
    
    if password:
        if password == "execution-alpha":  # Change this to your own password
            st.session_state.authenticated = True
            st.success("✓ Access granted!")
            st.rerun()
        else:
            st.error("❌ Incorrect password. Try again.")

    st. stop()


st.set_page_config(page_title="execution-alpha", layout="wide")

st.title("⭐ execution-alpha: LBO Model Explorer")
st.markdown("Production-grade LBO modeling for capital-thesis positioning.")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select:", ["Case Studies", "Custom Scenario", "About"])

if page == "Case Studies":
    st.header("Case Studies")
    
    tab1, tab2, tab3 = st.tabs(["LTG Analytics", "SaaS Platform", "Logistics"])
    
    with tab1:
        ltg = create_ltg_case()
        col1, col2, col3 = st.columns(3)
        col1.metric("Entry EV (£m)", f"£{ltg.entry_enterprise_value:.1f}m")
        col2.metric("Exit EV (£m)", f"£{ltg.exit_enterprise_value:.1f}m")
        col3.metric("Equity Uplift (£m)", f"£{ltg.equity_uplift:.1f}m")
        
        col1, col2 = st.columns(2)
        col1.metric("MoIC", f"{ltg.moic:.2f}x")
        col2.metric("IRR", f"{ltg.irr:.1f}%")
    
    with tab2:
        saas = create_saas_case()
        col1, col2, col3 = st.columns(3)
        col1.metric("Entry EV (£m)", f"£{saas.entry_enterprise_value:.1f}m")
        col2.metric("Exit EV (£m)", f"£{saas.exit_enterprise_value:.1f}m")
        col3.metric("Equity Uplift (£m)", f"£{saas.equity_uplift:.1f}m")
        
        col1, col2 = st.columns(2)
        col1.metric("MoIC", f"{saas.moic:.2f}x")
        col2.metric("IRR", f"{saas.irr:.1f}%")
    
    with tab3:
        logistics = create_logistics_case()
        col1, col2, col3 = st.columns(3)
        col1.metric("Entry EV (£m)", f"£{logistics.entry_enterprise_value:.1f}m")
        col2.metric("Exit EV (£m)", f"£{logistics.exit_enterprise_value:.1f}m")
        col3.metric("Equity Uplift (£m)", f"£{logistics.equity_uplift:.1f}m")
        
        col1, col2 = st.columns(2)
        col1.metric("MoIC", f"{logistics.moic:.2f}x")
        col2.metric("IRR", f"{logistics.irr:.1f}%")

elif page == "Custom Scenario":
    st.header("Run Custom Scenario")
    
    col1, col2, col3 = st.columns(3)
    entry_ebitda = col1.number_input("Entry EBITDA (£m)", value=24.8, min_value=1.0)
    entry_mult = col2.number_input("Entry Multiple (x)", value=9.0, min_value=1.0)
    exit_ebitda = col3.number_input("Exit EBITDA (£m)", value=49.6, min_value=1.0)
    
    col1, col2, col3 = st.columns(3)
    exit_mult = col1.number_input("Exit Multiple (x)", value=11.0, min_value=1.0)
    debt = col2.number_input("Debt (£m)", value=150.0, min_value=0.0)
    equity = col3.number_input("Equity (£m)", value=181.3, min_value=1.0)
    
    if st.button("Run Model"):
        model = LBOModel(
            name="Custom Scenario",
            entry_ebitda=entry_ebitda,
            entry_multiple=entry_mult,
            exit_ebitda=exit_ebitda,
            exit_multiple=exit_mult,
            debt_raised=debt,
            equity_invested=equity,
            holding_period=5,
            annual_debt_paydown=15.0,
        )
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Entry EV (£m)", f"£{model.entry_enterprise_value:.1f}m")
        col2.metric("Exit EV (£m)", f"£{model.exit_enterprise_value:.1f}m")
        col3.metric("Equity Uplift (£m)", f"£{model.equity_uplift:.1f}m")
        
        col1, col2 = st.columns(2)
        col1.metric("MoIC", f"{model.moic:.2f}x")
        col2.metric("IRR", f"{model.irr:.1f}%")

else:
    st.header("About execution-alpha")
    st.write("""
    **Production LBO Modeling Engine**
    
    - 3 real case studies (LTG, SaaS, Logistics)
    - Sensitivity analysis (1000+ scenarios)
    - Lever analysis (value driver quantification)
    - 100-day playbooks by sector
    - FastAPI backend + Streamlit UI
    - 98%+ test coverage
    
    **GitHub:** https://github.com/capital-thesis/execution-alpha
    """)

st.sidebar.markdown("---")
st.sidebar.write("**execution-alpha v1.0** | [GitHub](https://github.com/capital-thesis/execution-alpha)")
