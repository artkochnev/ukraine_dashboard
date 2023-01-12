from datetime import date
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pydeck as pdk
import logging
import data_pull_transform as dp

# --- GLOBALS
START_DATE = dp.START_DATE
END_DATE = dp.END_DATE
UNHCR_APP = dp.UNHCR_APP
SOURCE_TEXTS = "assets/text.xlsx"

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)

def main():
    st.experimental_singleton.clear()

    # DATA AND FIGURES
    fig_ccy = dp.plot_ccy_data()
    fig_refugees = dp.plot_hum_data(series = 'Refugees', title='Refugees')
    fig_idps = dp.plot_hum_data(series = 'Internally Displaced', title='Internally Displaced')
    fig_civs_dead = dp.plot_hum_data(series = 'Civilian deaths, confirmed', title='Civilian deaths, confirmed')
    fig_civs_injured = dp.plot_hum_data(series = 'Civilians injured, confirmed', title='Civilians injured, confirmed')
    fig_reconstruction_damage = dp.plot_reconstruction_sectors(series = 'Damage', title = 'Damage assessment as of August 2022, USD bn')
    fig_reconstruction_needs = dp.plot_reconstruction_sectors(series = 'Needs', title = 'Reconstruction needs assessment as of August 2022, USD bn')
    fig_reconstruction_regions = dp.plot_reconstruction_regions()
    fig_ukraine_support_committed = dp.plot_ukraine_support(series='Value committed', title = 'Support publicly announced, USD bn')
    fig_ukraine_support_delivered = dp.plot_ukraine_support(series='Value delivered', title = 'Support delivered in cash and kind, USD bn')
    fig_grain_destinations = dp.plot_grain_destinations()
    fig_delivery_rate = dp.plot_delivery_rate()
    fig_cpi_last = dp.plot_cpi_last()
    fig_cpi_12m = dp.plot_cpi_12m()
    fig_international_reserves = dp.plot_international_reserves()
    fig_bond_yields = dp.plot_bond_yields()
    fig_policy_rates = dp.plot_policy_rate()
    fig_interest_rates = dp.plot_interest_rates()
    fig_fiscal_income = dp.plot_fiscal_income()
    fig_fiscal_expenses = dp.plot_fiscal_expenses()
    fig_fiscal_finance = dp.plot_fiscal_finance()
    fig_fsi_npl = dp.plot_financial_soundness(series='Nonperforming loans net of provisions to capital')
    fig_fsi_liquidity = dp.plot_financial_soundness(series='Liquid assets to total assets')
    fig_fatalities_count = dp.plot_fatalities_series(series = 'FATALITIES', title = 'Number of Fatalities')
    fig_battle_count = dp.plot_fatalities_series(series='COUNT', title = 'Number of conflict events')
    fig_fatalities_geo = dp.plot_fatalities_geo()

    # FINAL REPORT
    st.title('Humanitarian and Economic Situation in Ukraine')
    
    st.header("War and People")
    # Put key metrics
    st.subheader('Conflict intensity')
    col1, col2 = st.columns(2)
    st.plotly_chart(fig_fatalities_geo, use_container_height=800)
    col1.plotly_chart(fig_fatalities_count, use_container_height=600, use_container_width=300)
    col2.plotly_chart(fig_battle_count, use_container_height=600, use_container_width=300)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_civs_dead, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_civs_injured, use_container_height=400, use_container_width=300)
    st.subheader('Displacement')
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_idps, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_refugees, use_container_height=400, use_container_width=300)
    st.markdown('**Distribution of Refugees**')
    st.components.v1.iframe(UNHCR_APP, width=800, height=800, scrolling=True)

    st.header("War and Economics")
    # Put key metrics
    st.subheader('Monetary sector')
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_cpi_12m, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_ccy, use_container_height=400, use_container_width=300)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_cpi_last, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_interest_rates, use_container_height=400, use_container_width=300)
    st.subheader('National bank tools')
    col1, col2 = st.columns(2)    
    col1.plotly_chart(fig_policy_rates, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_international_reserves, use_container_height=400, use_container_width=300)
    st.subheader('Financial system')
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fsi_npl, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_fsi_liquidity, use_container_height=400, use_container_width=300)
    st.subheader('Government finance')
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fiscal_income, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_fiscal_expenses, use_container_height=400, use_container_width=300)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fiscal_finance, use_container_height=400, use_container_width=150)
    col2.plotly_chart(fig_bond_yields, use_container_height=400, use_container_width=450)

    st.header('War and cooperation')
#   st.plotly_chart(fig_ukraine_support_committed, use_container_height=800, use_container_width=800)
    st.plotly_chart(fig_ukraine_support_delivered, use_container_height=800, use_container_width=300)
    st.plotly_chart(fig_delivery_rate)
    st.plotly_chart(fig_grain_destinations)

    st.header('War and reconstruction')
    # Put key metrics
    st.plotly_chart(fig_reconstruction_damage)
    st.plotly_chart(fig_reconstruction_regions, use_container_height=800)
    st.plotly_chart(fig_reconstruction_needs)    

    #st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='summary_short_effects'))
    #  cmet11, cmet12 = st.columns(2)
    #cmet11.metric("Refugees, mn people", round(df_unhcr_casualties['Refugees']/10**6,1))
    #cmet21.metric("IDPs, mn people", round(df_unhcr_casualties['IDPs']/10**6,1))
    #fp.plot_figure(intro_fig1.plotly_chart(fig_unhcr_casualties, height = 400, width = 400))
    # st.markdown('---')
    # fp.plot_figure(components.iframe("https://datawrapper.dwcdn.net/EQ9IF/3/", height=800, scrolling=True))
    # fx_select = st.selectbox(
    #     'Choose a currency pair',
    #     ("USD/HUF", "USD/PLN", "USD/CZK", "USD/RSD", "USD/TRY", "USD/RON"))
    
    # fig_cee_currency = fp.fig_investing_data(df_investing_data, fx_select, bench_date=CUT_OFF_DATE, height=400, width=400)
    #st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='europe_energy'))

if __name__ == '__main__':
    main()
