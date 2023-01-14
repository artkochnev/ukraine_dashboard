from datetime import date, timedelta
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
SOURCE_METRICS = "assets/metrics.csv"
SOURCE_NEWS = "assets/tf_google_news.csv"

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)

def read_texts(source = SOURCE_TEXTS, sheet_name = 0):
    df = pd.read_excel(source, sheet_name=sheet_name)
    logging.info('Loaded texts')
    return df

def write_expander(df, title='summary_short_effects', title_col='title', text_col = 'text', expander_title='Explainer'):
    text = df[text_col][df[title_col]==title].iloc[0]
    with st.expander(expander_title):
        st.write(text)

def read_metrics(source = SOURCE_METRICS):
    df = pd.read_csv(source, encoding='utf-16')
    logging.info('Loaded metrics')
    return df

def read_news(source = SOURCE_NEWS):
    df = pd.read_csv(source, encoding='utf-16', index_col=False)
    df = df[:5]
    df = df.to_html(escape=False, index=False, render_links=True, justify='justify')
    df = df.replace('border="1"','border="0"')
    logging.info('Loaded news')
    return df

def get_metric(df, title, value_col, title_col = 'Title', unit='default', digits = 0, digits_unit = 'default'):
    df = df
    value = df[value_col][df[title_col]==title].iloc[0]
    if unit == 'pct':
        value = "{:.1%}".format(value)
    elif unit == '%':
        value = "{:.1f}".format(value)
        value = f'{value}%'
    elif unit == 'k':
        value = "{:.1f}".format(value)
        value = f'{value}k'
    elif unit == 'mn':
        value = "{:.1f}".format(value)
        value = f'{value}mn'
    elif unit == 'bn':
        value = "{:.0f}".format(value)
        value = f'{value}bn'
    elif unit == 'default':
        if digits == 0:
            value = "{:.1f}".format(value)
            if digits_unit == 'default':
                value = f'{value}'
            else:
                value = f'{value}{digits_unit}'
        elif digits == 3:
            value = value / (10**3)
            value = "{:.1f}".format(value)
            if digits_unit == 'default':
                value = f'{value}k'
            else:
                value = f'{value}{digits_unit}'
        elif digits == 6:
            value = value / (10**6)
            value = "{:.1f}".format(value)
            if digits_unit == 'default':
                value = f'{value}mn'
            else:
                value = f'{value}{digits_unit}'
        elif digits == 9:
            value = value / (10**9)
            value = "{:.0f}".format(value)
            if digits_unit == 'default':
                value = f'{value}'
            else:
                value = f'{value}{digits_unit}bn'
    return value

def main():
    st.experimental_singleton.clear()

    # --- LOAD DATA
    df_t = read_texts()
    df_m = read_metrics()
    df_news = read_news()

    # --- LOAD TABLES
    # tab_google_news = dp.plot_google_news(df_news)

    # --- LOAD FIGURES
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
    st.header('Key indicators')
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Fatalities, estimated", 
        value = get_metric(df_m, 'Fatalities count', 'Last value', digits=3),
        )
    m2.metric(
        "Refugees", 
        value = get_metric(df_m, 'Refugees', 'Last value', digits=6),
        delta = get_metric(df_m, 'Refugees', 'Change', digits=6),
        delta_color = 'inverse' 
        )
    m3.metric(
        "Internally displaced", 
        value = get_metric(df_m, 'Internally displaced', 'Last value', digits=6),
        delta = get_metric(df_m, 'Internally displaced', 'Change', digits=6),
        delta_color = 'inverse' 
        )
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Reconstruction needs estimated, USD", 
        value = get_metric(df_m, 'Reconstruction needs', 'Last value', unit='bn'),
        )
    m2.metric(
        "Support delivered to Ukraine, USD bn", 
        value = get_metric(df_m, 'Delivered', 'Last value', unit='bn'),
        )
    m3.metric(
        "UA International Reserves, USD bn", 
        value = get_metric(df_m, 'International Reserves', 'Last value', unit='bn'),
        )
    write_expander(df_t,title='summary_short_effects', expander_title='Summary')
    st.markdown('---')
    st.subheader('Latest news')
    st.markdown('**Source: Google News**')
    st.markdown(df_news, unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.header("War and People")
    # Put key metrics
    st.subheader('Conflict intensity')
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Violence events", 
        value = get_metric(df_m, 'Violence events', 'Last value', digits=3),
        )
    m2.metric(
        "Explosions count", 
        value = get_metric(df_m, 'Explosions count', 'Last value', digits=3),
        )
    m3.metric(
        "Battle count", 
        value = get_metric(df_m, 'Battle count', 'Last value', digits=3),
        )
    st.plotly_chart(fig_fatalities_geo, use_container_height=800)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fatalities_count, use_container_height=600, use_container_width=300)
    col2.plotly_chart(fig_battle_count, use_container_height=600, use_container_width=300)
    st.markdown('---')
    st.subheader('Civilian casualties')
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Fatalities, estimated", 
        value = get_metric(df_m, 'Fatalities count', 'Last value', digits=3),
        )
    m2.metric(
        "Civilians killed, confirmed", 
        value = get_metric(df_m, 'Civilians killed, confirmed', 'Last value', digits=3),
        delta = get_metric(df_m, 'Civilians killed, confirmed', 'Change', digits=3),
        delta_color = 'inverse' 
        )
    m3.metric(
        "Civilians injured, confirmed", 
        value = get_metric(df_m, 'Civilians injured, confirmed', 'Last value', digits=3),
        delta = get_metric(df_m, 'Civilians injured, confirmed', 'Change', digits=3),
        delta_color = 'inverse' 
        )
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_civs_dead, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_civs_injured, use_container_height=400, use_container_width=300)
    st.markdown('---')
    st.subheader('Displacement')
    m1, m2 = st.columns(2)
    m1.metric(
        "Refugees", 
        value = get_metric(df_m, 'Refugees', 'Last value', digits=6),
        delta = get_metric(df_m, 'Refugees', 'Change', digits=6),
        delta_color = 'inverse' 
        )
    m2.metric(
        "Internally displaced", 
        value = get_metric(df_m, 'Internally displaced', 'Last value', digits=6),
        delta = get_metric(df_m, 'Internally displaced', 'Change', digits=6),
        delta_color = 'inverse' 
        )    
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_idps, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_refugees, use_container_height=400, use_container_width=300)
    st.subheader('Distribution of Refugees')
    st.components.v1.iframe(UNHCR_APP, width=800, height=800, scrolling=True)
    st.markdown('---')
    st.header("War and Economics")
    # Put key metrics
    st.subheader('Monetary sector')
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Inflation, yoy", 
        value = get_metric(df_m, 'Inflation rate', 'Last value', unit='%'),
        delta = get_metric(df_m, 'Inflation rate', 'Change', unit='%'),
        delta_color = 'inverse' 
        )
    m2.metric(
        "Lending rate, households", 
        value = get_metric(df_m, 'Lending rate, households', 'Last value', unit='%'),
        )
    m3.metric(
        "Lending rate, corporates", 
        value = get_metric(df_m, 'Lending rate, corporates', 'Last value', unit='%'),
        )
    m4.metric(
        "FX rate: UAH/USD", 
        value = get_metric(df_m, 'FX rate: UAH/USD', 'Last value'),
        delta = get_metric(df_m, 'FX rate: UAH/USD', 'Change'),
        delta_color = 'inverse',
        )
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_cpi_12m, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_ccy, use_container_height=400, use_container_width=300)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_cpi_last, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_interest_rates, use_container_height=400, use_container_width=300)
    st.markdown('---')
    st.subheader('National bank tools')
    m1, m2 = st.columns(2)
    m1.metric(
        "Key rate", 
        value = get_metric(df_m, 'Key rate', 'Last value', unit='%'),
        )    
    m2.metric(
        "International reserves, USD", 
        value = get_metric(df_m, 'International Reserves', 'Last value', unit='bn'),
        )
    col1, col2 = st.columns(2)    
    col1.plotly_chart(fig_policy_rates, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_international_reserves, use_container_height=400, use_container_width=300)
    st.markdown('---')
    st.subheader('Financial system')
    m1, m2 = st.columns(2)
    m1.metric(
        "NPL ratio", 
        value = get_metric(df_m, 'NPL ratio', 'Last value', unit='%'),
        delta = get_metric(df_m, 'NPL ratio', 'Change', unit='%'),
        delta_color = 'inverse',
        )    
    m2.metric(
        "Liquid asset ratio", 
        value = get_metric(df_m, 'Liquid asset ratio', 'Last value', unit='%'),
        delta = get_metric(df_m, 'Liquid asset ratio', 'Change', unit='%'),
        delta_color='normal'
        )
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fsi_npl, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_fsi_liquidity, use_container_height=400, use_container_width=300)
    st.markdown('---')
    st.subheader('Government finance')
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Yield, UAH govt, bonds", 
        value = get_metric(df_m, 'Yield, UAH govt bonds', 'Last value', unit='%'),
        delta = get_metric(df_m, 'Yield, UAH govt bonds', 'Change', unit='%'),
        delta_color = 'inverse',
        )    
    m2.metric(
        "Fiscal income, UAH", 
        value = get_metric(df_m, 'Fiscal income, total', 'Last value', digits=6, digits_unit='tn'),
        )
    m3.metric(
        "Fiscal expenses, UAH", 
        value = get_metric(df_m, 'Fiscal expenses, total', 'Last value', digits=6, digits_unit='tn'),
        )
    m4.metric(
        "Domestic finance of deficit", 
        value = get_metric(df_m, 'Fiscal finance, total', 'Last value', unit='pct'),
        )
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fiscal_income, use_container_height=400, use_container_width=300)
    col2.plotly_chart(fig_fiscal_expenses, use_container_height=400, use_container_width=300)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_fiscal_finance, use_container_height=400, use_container_width=150)
    col2.plotly_chart(fig_bond_yields, use_container_height=400, use_container_width=450)

    st.header('War and cooperation')
    st.subheader('Ukraine support')
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Support announced, USD",
        value = get_metric(df_m, 'Commitment', 'Last value', unit='bn')
    )
    m2.metric(
        "Support delivered, USD",
        value = get_metric(df_m, 'Delivered', 'Last value', unit='bn')
    )
    m3.metric(
        "Military support sent, USD",
        value = get_metric(df_m, 'Delivered military help', 'Last value', unit='bn')
    )
#   st.plotly_chart(fig_ukraine_support_committed, use_container_height=800, use_container_width=800)
    st.plotly_chart(fig_ukraine_support_delivered, use_container_height=800, use_container_width=300)
    st.plotly_chart(fig_delivery_rate)
    st.markdown('---')
    st.subheader('Grain deal')
    m1, m2 = st.columns(2)
    m1.metric(
        'Grain sent (all), tons',
        value = get_metric(df_m, 'Total amount delivered', 'Last value', digits=6)
    )
    m2.metric(
        'Grain sent (high-income) countries, tons',
        value = get_metric(df_m, 'Amount to high-income countries', 'Last value', digits=6)
    )
    st.plotly_chart(fig_grain_destinations)
    st.markdown('---')
    st.header('War and reconstruction')
    # Put key metrics
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Damage estimated, USD", 
        value = get_metric(df_m, 'Damage caused', 'Last value', unit='bn'),
        )
    m2.metric(
        "Reconstruction needs estimated, USD", 
        value = get_metric(df_m, 'Reconstruction needs', 'Last value', unit='bn'),
        )
    m3.metric(
        "Ukraine GDP (2021), current USD", 
        value = get_metric(df_m, 'GDP Ukraine, current USD', 'Last value', unit='bn'),
        )
    st.plotly_chart(fig_reconstruction_damage)
    st.plotly_chart(fig_reconstruction_regions, use_container_height=800)
    st.plotly_chart(fig_reconstruction_needs)    
    st.markdown('___')
    #st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='summary_short_effects'))
    # fp.plot_figure(components.iframe("https://datawrapper.dwcdn.net/EQ9IF/3/", height=800, scrolling=True))
    # fx_select = st.selectbox(
    #     'Choose a currency pair',
    #     ("USD/HUF", "USD/PLN", "USD/CZK", "USD/RSD", "USD/TRY", "USD/RON"))
    
    # fig_cee_currency = fp.fig_investing_data(df_investing_data, fx_select, bench_date=CUT_OFF_DATE, height=400, width=400)
    #st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='europe_energy'))

if __name__ == '__main__':
    main()
