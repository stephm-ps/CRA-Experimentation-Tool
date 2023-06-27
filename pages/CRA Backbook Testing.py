import streamlit as st
import pandas as pd
from google.cloud import bigquery
from streamlit_extras.colored_header import colored_header
from streamlit_extras.mandatory_date_range import date_range_picker
import plotly.express as px
import numpy as np
from Calculator.cracalc import score_to_rank
from BigQueries import cra_backbook

st.set_page_config(
    page_title="CRA Back Book Testing",
    page_icon=":chart_with_upwards_trend:",
    layout="wide")

# connect and import query
project_id = 'analytics-hub-proj'
client = bigquery.Client()
cust_query = cra_backbook()

@st.cache_data ## caching data here from bq
def query_from_bq(_client,query):
    df = client.query(query).to_dataframe()
    return df

cust_cra = query_from_bq(client,cust_query)

colored_header(
    label="Backbook CRA Test",
    description="Filter through Dojo backbook CRA scored customers.",
    color_name="red-70",
)
# create date filter
dates = date_range_picker("Customer Live Date Range:")
cust_cra_updated = cust_cra[cust_cra.live_date.between(dates[0], dates[1])]

# create mcc filter
st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: blue !important;
}
</style>
""",
    unsafe_allow_html=True,
)
primary_mcc_cats = list(cust_cra.primary_mcc_industry_category.unique())
mccs_select = st.multiselect('Primary MCC Categories:',
                             primary_mcc_cats,
                             )
if len(mccs_select) == 0:
    cust_cra_updated = cust_cra_updated
else:
    cust_cra_updated = cust_cra_updated[cust_cra_updated.primary_mcc_industry_category.isin(mccs_select)]

# legal type filter
legal_types = list(cust_cra.registered_company_legal_type.unique())
legal_select = st.multiselect('Registered Company Legal Type:', legal_types)

if len(legal_select) == 0:
    cust_cra_updated = cust_cra_updated
else:
    cust_cra_updated = cust_cra_updated[cust_cra_updated.registered_company_legal_type.isin(legal_select)]

# final dataframe, filters
cust_cra_final = cust_cra_updated

# calculate rank percentages
def rank_percentages(df):
    score_only = df[['customer_id','overall_risk_score_rating']].drop_duplicates()
    rank_counts = score_only.overall_risk_score_rating.value_counts()
    rank_countsdf = pd.DataFrame(rank_counts).reset_index()
    total = rank_countsdf['count'].sum()
    rank_countsdf['perc'] = round(rank_countsdf['count']/total*100,1)
    return rank_countsdf

rank_perc = rank_percentages(cust_cra_final)

# display results
mean_cra_score = cust_cra_final.overall_score.mean()
mean_rank = score_to_rank(mean_cra_score)
cust_count = cust_cra_final.customer_id.nunique()

# calculate button
# result = st.button('Calculate')
# st.write(result)

st.write("""
# Results
""")

if st.button('Calculate'):
    # st.balloons()
    # st.snow()
    # display total count, mean score and mean rank
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Total Customers",
                value=cust_count,
                delta=1000)
    col2.metric(label="Mean Overall CRA Score",
                value=round(mean_cra_score,2),
                delta=round(mean_cra_score-np.mean(cust_cra.overall_score),2)
                )
    col3.metric(label="Mean Overall CRA Score",
                value=mean_rank,
                )

    col4.dataframe(rank_perc,
                 column_config={
                     "overall_risk_score_rating": "Risk",
                     "count": "Count",
                     "perc": "%"
                 },
                 hide_index=True,
                 )

    fig = px.bar(rank_perc,
                 x="perc",
                 y="overall_risk_score_rating",
                 color='overall_risk_score_rating',
                 color_discrete_map={'Standard': 'green',
                                     'Medium': 'yellow',
                                     'High': 'orange',
                                     'Prohibited': 'red'},
                 labels={'perc': 'Percentage of Sample %',
                         'overall_risk_score_rating': ''}
                 )
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(cust_cra_final, use_container_width=True)

