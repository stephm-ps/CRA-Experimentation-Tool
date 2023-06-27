import streamlit as st
from streamlit_extras.colored_header import colored_header
from Calculator import cracalc

st.set_page_config(
    page_title="CRA Calculator",
    page_icon=":abacus:",
    layout="wide")

colored_header(
    label="CRA Score Calculator",
    description="This calculator is used to calculate the overall CRA Score from selecting the risk rank of individual risk factors.",
    color_name="orange-70",
)

outcomes = ('Standard',
            'Medium',
            'High',
            'Prohibited')

risk_factors = {
    1:'PEP and Sanctions Status',
    2:'Adverse Media Risk',
    3:'Business Vertical MCC',
    4:'Historic Merchant Records',
    5:'Length of Time in Business',
    6:'Home Trading',
    7:'Entity Type',
    8:'Signatory and/or UBO’s Country of Residence',
    9:'Overseas Ownership Structure',
    10:'Customers Proposed usage of MOTO',
    11:'Customer Proposed Use of Ecommerce',
    13:'Annual Turnover (TO)',
    14:'Highest Transaction Value',
    15:'Onboarding Channel',
    16:'Status of site visit'

}

st.write("""
### Select Risk Factor Rating:
""")

st.write('Customer Risk Factors')
col1,col2,col3 = st.columns(3)
with col1:
    rule1_choice = st.selectbox(risk_factors[1],outcomes)
    rule4_choice = st.selectbox(risk_factors[4], outcomes)
    rule7_choice = st.selectbox(risk_factors[7], outcomes)

with col2:
    rule2_choice = st.selectbox(risk_factors[2],outcomes)
    rule5_choice = st.selectbox(risk_factors[5], outcomes)

with col3:
    rule3_choice = st.selectbox(risk_factors[3],outcomes)
    rule6_choice = st.selectbox(risk_factors[6], outcomes)


st.write('\n Country or Georgraphic Risk Factors')
col1,col2 = st.columns(2)
with col1:
    rule8_choice = st.selectbox(risk_factors[8],outcomes)

with col2:
    rule9_choice = st.selectbox(risk_factors[9],outcomes)

st.write('Product, Service and Transaction Risk Factors')
col1,col2 = st.columns(2)
with col1:
    rule10_choice = st.selectbox(risk_factors[10],outcomes)
    rule13_choice = st.selectbox(risk_factors[13], outcomes)
with col2:
    rule11_choice = st.selectbox(risk_factors[11],outcomes)
    rule14_choice = st.selectbox(risk_factors[14],outcomes)

st.write('Channel or Distribution Risk Factors')
col1,col2 = st.columns(2)
with col1:
    rule15_choice = st.selectbox(risk_factors[15],outcomes)
    rule16_choice = st.selectbox(risk_factors[16],outcomes)

# result = st.button('Calculate')
# st.write(result)

if st.button('Calculate'):
    calc_score = cracalc.overall_score(rule1_choice,
                                       rule2_choice,
                                       rule3_choice,
                                       rule4_choice,
                                       rule5_choice,
                                       rule6_choice,
                                       rule7_choice,
                                       rule8_choice,
                                       rule9_choice,
                                       rule10_choice,
                                       rule11_choice,
                                       rule13_choice,
                                       rule14_choice,
                                       rule15_choice,
                                       rule16_choice)
    col1, col2 = st.columns(2)
    col1.metric(label="Overall CRA Score",
                value=round(calc_score[0],2)
                )
    col2.metric(label="Overall CRA Risk",
                value=calc_score[1]
                )
