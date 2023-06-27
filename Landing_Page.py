import streamlit as st
import pandas as pd
st.title("CRA Score 1.0")

st.write("""
The Customer Risk Assessment (CRA) Score encapsulates the money laundering, criminal and political risk posed by Dojo Merchants.\n
It is composed of grouped risk factors, each with an individual risk banding: Standard | Medium | High | Prohibited which each equate to a numerical score.
The groups of risk factors each have a weight and proportion, where the overall score and rank can be calculated.

The CRA formular:
""")

st.image("CRA_formula.png")

st.write("""
### Group Proportions and Weightings
""")

group_weights = pd.DataFrame(columns=['Group','Group Proportion','Group Weight','Risk Factor','Standard Score','Medium Score','High Score','Prohibited Score'])
group_weights.loc[0] = ['Customer Risk Factors','32%',3,'PEP and Sanctions Status',0,0,50,100]
group_weights.loc[1] = ['Customer Risk Factors','32%',3,'Adverse Media',0,0,50,0]
group_weights.loc[2] = ['Customer Risk Factors','32%',3,'Business Vertical MCC',0,1,2,0]
group_weights.loc[3] = ['Customer Risk Factors','32%',3,'Historic Merchant Records',0,0,50,100]
group_weights.loc[4] = ['Customer Risk Factors','32%',3,'Length of Time in Business',0,0.5,1,0]
group_weights.loc[5] = ['Customer Risk Factors','32%',3,'Home Trading',0,0,1,0]
group_weights.loc[6] = ['Customer Risk Factors','32%',3,'Entity Type',0,0,0,0]
group_weights.loc[7] = ['','','','','','','','']
group_weights.loc[8] = ['Country or Geographic Risk Factors','25%',2,'Signatory and/or UBOs Country of Residence',0,0,50,100]
group_weights.loc[9] = ['Country or Geographic Risk Factors','25%',2,'Overseas Ownership Structure',0,0,50,100]
group_weights.loc[10] = ['','','','','','','','']
group_weights.loc[11] = ['Product, Service and Transaction Risk Factors','22%',3,'Customers Proposed usage of MOTO',0,1,2,0]
group_weights.loc[12] = ['Product, Service and Transaction Risk Factors','22%',3,'Customers Proposed Use of Ecommerce',0,0,0,0]
group_weights.loc[13] = ['Product, Service and Transaction Risk Factors','22%',3,'Annual Turnover (TO)',0,1,2,0]
group_weights.loc[14] = ['Product, Service and Transaction Risk Factors','22%',3,'Highest Transaction Value',0,1,2,0]
group_weights.loc[15] = ['','','','','','','','']
group_weights.loc[16] = ['Channel or Distribution Risk Factors','21%',2,'Onboarding Channel',0,1,2,0]
group_weights.loc[17] = ['Channel or Distribution Risk Factors','21%',2,'Status of sire visit',0,1,0,0]

st.dataframe(group_weights,
             hide_index=True)