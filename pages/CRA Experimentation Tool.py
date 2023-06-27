import streamlit as st
import pandas as pd
from google.cloud import bigquery
from streamlit_extras.colored_header import colored_header
from streamlit_extras.mandatory_date_range import date_range_picker
import plotly.express as px
import numpy as np
from Calculator.cracalc import score_to_rank
from BigQueries import cra_backbook

# set screen configurations
st.set_page_config(layout="wide")

# connect and import query
project_id = 'analytics-hub-proj'
client = bigquery.Client()
cust_query = cra_backbook()


@st.cache_data  ## caching data here from bq
def query_from_bq(_client, query):
    df = client.query(query).to_dataframe()
    return df


cust_cra = query_from_bq(client, cust_query)

## FILTER DATA

colored_header(
    label="Backbook CRA Test",
    description="Filter through Dojo backbook CRA scored customers.",
    color_name="red-70",
)
st.write("""
### Filter Sample For Testing
""")

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

# ADJUST WEIGHTING AND PROPORTIONS
st.write("""
### Adjust Rule Group Proportion % and Group Weight
""")
# store the risk factor group proportions and weights
RiskFactorGroups = {
    'Customer Risk Factors': {
        'Proportion': 32,
        'Weight': 3
    },
    'Country or Geographic Risk Factors': {
        'Proportion': 25,
        'Weight': 2
    },
    'Product, Service and Transaction Risk Factors': {
        'Proportion': 22,
        'Weight': 3
    },
    'Channel or Distribution Risk Factors': {
        'Proportion': 21,
        'Weight': 2
    }
}

# make a copy where the values can be changed with input
RiskFactorGroups_update = {
    'Customer Risk Factors': {
        'Proportion': 32,
        'Weight': 3
    },
    'Country or Geographic Risk Factors': {
        'Proportion': 25,
        'Weight': 2
    },
    'Product, Service and Transaction Risk Factors': {
        'Proportion': 22,
        'Weight': 3
    },
    'Channel or Distribution Risk Factors': {
        'Proportion': 21,
        'Weight': 2
    }
}
# select rule group to adjust
group_select1 = st.selectbox('Risk Factor Group:',
                             RiskFactorGroups.keys()
                             )

proportions = ['Default']
for w in range(0, 101):
    proportions.append(str(w))
group_proportion = st.selectbox('Select Group Proportion % *',
                                proportions
                                )

weights = ['Default']
for w in range(0, 11):
    weights.append(str(w))
group_weight = st.selectbox('Select Group Weight ',
                            weights
                            )
st.write("""
\* Selecting a proportion % adjustment for a risk group will mean the proportions of the remaining groups will sum to 100 minus the selection for the change group, where this remainder will be divided up by the default percentages as proportions, so all proportions still reach 100%.
""")

# CALCULATION
def return_score(data,
                 Rule1Score,
                 Rule2Score,
                 Rule3Score,
                 Rule4Score,
                 Rule5Score,
                 Rule6Score,
                 Rule7Score,
                 Rule8Score,
                 Rule9Score,
                 Rule10Score,
                 Rule11Score,
                 Rule13Score,
                 Rule14Score,
                 Rule15Score,
                 Rule16Score,
                 Weight1,
                 Weight2,
                 Weight3,
                 Weight4,
                 Proportion1,
                 Proportion2,
                 Proportion3,
                 Proportion4
                 ):
    # need to add in if 0 cases option
    data['Group1Sum'] = data[Rule1Score] + data[Rule2Score] + data[Rule3Score] + data[Rule4Score] + data[Rule5Score] + data[Rule6Score] + data[Rule7Score]
    data['Group2Sum'] = data[Rule8Score] + data[Rule9Score]
    data['Group3Sum'] = data[Rule10Score] + data[Rule11Score] + data[Rule13Score] + data[Rule14Score]
    data['Group4Sum'] = data[Rule15Score] + data[Rule16Score]

    data['Group1SumWeighted'] = np.where(data['Group1Sum'] > 0, \
                                             (data['Group1Sum'] / float(Weight1) \
                                              * float(Proportion1) / 100), \
                                              0)
    data['Group2SumWeighted'] = np.where(data['Group2Sum'] > 0, \
                                              (data['Group2Sum'] / float(Weight2) \
                                               * float(Proportion2) / 100), \
                                              0)
    data['Group3SumWeighted'] = np.where(data['Group3Sum'] > 0, \
                                              (data['Group3Sum'] / float(Weight3) \
                                               * float(Proportion3) / 100), \
                                              0)
    data['Group4SumWeighted'] = np.where(data['Group4Sum'] > 0, \
                                              (data['Group4Sum'] / float(Weight4) \
                                               * float(Proportion4) / 100), \
                                              0)

    data['overall_score'] = data['Group1SumWeighted']+data['Group2SumWeighted']+data['Group3SumWeighted']+data['Group4SumWeighted']

def score_to_rank(sc):
    if sc <= 0.46:
        return 'Standard'
    elif (sc > 0.46) & (sc <= 0.92):
        return 'Medium'
    elif (sc > 0.92) & (sc <= 11.99):
        return 'High'
    elif sc > 11.99:
        return 'Prohibited'
    else:
        print('Error')


def convert_to_rank_category(column):
    thresholds = [0, 0.46, 0.92, 11.99, 1000]
    labels = ['Standard', 'Medium', 'High', 'Prohibited']
    ranks = pd.cut(column, bins=thresholds, labels=labels, right=False)
    return ranks


# store the rules and scores
rules_scores = {
    # 1
    'PEPAndSanctionsStatusRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 50,
        'Prohibited': 100
    },
    # 2
    'AdverseMediaRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 50,
        'Prohibited': 0
    },
    # 3
    'BusinessVerticalMccRiskFactor': {
        'Standard': 0,
        'Medium': 1,
        'High': 2,
        'Prohibited': 0
    },
    # 4
    'HistoricMerchantRecordsRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 50,
        'Prohibited': 100
    },
    # 5
    'LengthOfTimeInBusinessRiskFactor': {
        'Standard': 0,
        'Medium': 0.5,
        'High': 1,
        'Prohibited': 0
    },
    # 6
    'HomeTradingRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 1,
        'Prohibited': 0
    },
    # 7
    'EntityTypeRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 0,
        'Prohibited': 0
    },
    # 8
    'SignatoryUboCountryOfResidenceRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 50,
        'Prohibited': 100
    },
    # 9
    'OverseasOwnershipStructureRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 50,
        'Prohibited': 100
    },
    # 10
    'ProposedMotoUsageRiskFactor': {
        'Standard': 0,
        'Medium': 1,
        'High': 2,
        'Prohibited': 0
    },
    # 11
    'ProposedEcommerceUsageRiskFactor': {
        'Standard': 0,
        'Medium': 0,
        'High': 0,
        'Prohibited': 0
    },
    # 13
    'AnnualTurnoverRiskFactor': {
        'Standard': 0,
        'Medium': 1,
        'High': 2,
        'Prohibited': 0
    },
    # 14
    'HighestTransactionValueRiskFactor': {
        'Standard': 0,
        'Medium': 1,
        'High': 2,
        'Prohibited': 0
    },
    # 15
    'OnboardingChannelSourcesRiskFactor': {
        'Standard': 0,
        'Medium': 1,
        'High': 2,
        'Prohibited': 0
    },
    # 16
    'SiteVisitRiskFactor': {
        'Standard': 0,
        'Medium': 1,
        'High': 0,
        'Prohibited': 0
    }
}

# CALCULATE
if st.button('Calculate'):
    RiskFactorGroups_update = {
        'Customer Risk Factors': {
            'Proportion': 32,
            'Weight': 3
        },
        'Country or Geographic Risk Factors': {
            'Proportion': 25,
            'Weight': 2
        },
        'Product, Service and Transaction Risk Factors': {
            'Proportion': 22,
            'Weight': 3
        },
        'Channel or Distribution Risk Factors': {
            'Proportion': 21,
            'Weight': 2
        }
    }
    # update the rule group proportions and weights from the input
    try:
        if group_proportion != 'Default':
            RiskFactorGroups_update[group_select1]['Proportion'] = float(group_proportion)
            rest = 100 - float(group_proportion)
            rest_groups = []
            for key in RiskFactorGroups_update.keys():
                if key != group_select1:
                    rest_groups.append(key)

            if rest == 0:
                for j in [0, 1, 2]:
                    RiskFactorGroups_update[rest_groups[j]]['Proportion'] = 0
            else:
                divide = float(rest) / (float(RiskFactorGroups[rest_groups[0]]['Proportion']) + \
                                        float(RiskFactorGroups[rest_groups[1]]['Proportion']) + \
                                        float(RiskFactorGroups[rest_groups[2]]['Proportion']))
                for j in [0, 1, 2]:
                    RiskFactorGroups_update[rest_groups[j]]['Proportion'] = round(
                        RiskFactorGroups_update[rest_groups[j]]['Proportion'] * divide, 1)
        elif group_proportion == 'Default':
            pass
    except Exception as E:
        st.write('Error with group proportion: {}'.format(E))

    try:
        if group_weight != 'Default':
            RiskFactorGroups_update[group_select1]['Weight'] = group_weight
        elif group_proportion == 'Default':
            pass
    except Exception as E:
        st.write('Error with group weight: {}'.format(E))

    cra_pivot = cust_cra_final.pivot(index='customer_id', columns=['risk_factor_type'], values='risk_factor_outcome')

    for c in cra_pivot.columns:
        cra_pivot['score_{}'.format(c)] = cra_pivot[c].map(rules_scores[c])

    # calculate scores of sample based on weight and proportion input
    return_score(cra_pivot,
                 'score_PEPAndSanctionsStatusRiskFactor',
                 'score_AdverseMediaRiskFactor',
                 'score_BusinessVerticalMccRiskFactor',
                 'score_HistoricMerchantRecordsRiskFactor',
                 'score_LengthOfTimeInBusinessRiskFactor',
                 'score_HomeTradingRiskFactor',
                 'score_EntityTypeRiskFactor',
                 'score_SignatoryUboCountryOfResidenceRiskFactor',
                 'score_OverseasOwnershipStructureRiskFactor',
                 'score_ProposedMotoUsageRiskFactor',
                 'score_ProposedEcommerceUsageRiskFactor',
                 'score_AnnualTurnoverRiskFactor',
                 'score_HighestTransactionValueRiskFactor',
                 'score_OnboardingChannelSourcesRiskFactor',
                 'score_SiteVisitRiskFactor',
                 RiskFactorGroups_update['Customer Risk Factors']['Weight'],
                 RiskFactorGroups_update['Country or Geographic Risk Factors']['Weight'],
                 RiskFactorGroups_update['Product, Service and Transaction Risk Factors']['Weight'],
                 RiskFactorGroups_update['Channel or Distribution Risk Factors']['Weight'],
                 RiskFactorGroups_update['Customer Risk Factors']['Proportion'],
                 RiskFactorGroups_update['Country or Geographic Risk Factors']['Proportion'],
                 RiskFactorGroups_update['Product, Service and Transaction Risk Factors']['Proportion'],
                 RiskFactorGroups_update['Channel or Distribution Risk Factors']['Proportion'],
                 )


    # convert calculated scores to rank
    cra_pivot['overall_risk_score_rating'] = convert_to_rank_category(cra_pivot['overall_score'])
    cra_pivot = cra_pivot.reset_index()

    # get just ids, scores and ranks from original sample
    og_cra = cust_cra_final[['customer_id', 'overall_score', 'overall_risk_score_rating']].drop_duplicates()


    # display results
    def rank_percentages(df):
        score_only = df[['customer_id', 'overall_risk_score_rating']].drop_duplicates()
        rank_counts = score_only.overall_risk_score_rating.value_counts()
        rank_countsdf = pd.DataFrame(rank_counts).reset_index()
        total = rank_countsdf['count'].sum()
        rank_countsdf['perc'] = round(rank_countsdf['count'] / total * 100, 1)
        return rank_countsdf


    FactorGroupsDf = pd.DataFrame(columns=['Rule Group','Weight','Proportion'])
    lc = 0
    for i,z in RiskFactorGroups.items():
        FactorGroupsDf.loc[lc] = [i,z['Weight'],z['Proportion']]
        lc += 1

    FactorGroupsEditDf = pd.DataFrame(columns=['Rule Group', 'Weight', 'Proportion'])
    lc1 = 0
    for i, z in RiskFactorGroups_update.items():
        FactorGroupsEditDf.loc[lc1] = [i, z['Weight'], z['Proportion']]
        lc1 += 1

    hypothetical_split, original_split = rank_percentages(cra_pivot), rank_percentages(og_cra)
    c1,c2,c3 = st.columns(3)

    c2.metric(label='Customers in Sample',
              value=cust_cra_final.customer_id.nunique()
              )
    col1, col2 = st.columns(2)

    col1.write("""
        ### Original Scoring Overview 
        """)
    col1.dataframe(FactorGroupsDf,
                   hide_index=True)

    col2.write("""
            ### Updated Scoring Overview
            """)
    col2.dataframe(FactorGroupsEditDf,
                   hide_index=True)

    cl1,cl2,cl3,cl4,cl5,cl6 = st.columns(6)

    cl1.metric(label="Original Sample Mean",
                value=round(np.mean(og_cra['overall_score']),3)
                )
    cl2.metric(label="Original Sample Minimum",
               value=round(float(np.min(og_cra['overall_score'])),3)
               )
    cl3.metric(label="Original Sample Minimum",
               value=round(float(np.max(og_cra['overall_score'])),1)
               )

    deltacl4 = round(float(np.mean(cra_pivot['overall_score']))-float(np.mean(og_cra['overall_score'])),3)
    cl4.metric(label="Updated Sample Mean",
               value=round(float(np.mean(cra_pivot['overall_score'])), 3),
               delta=deltacl4,
               delta_color="inverse"
               )

    deltacl5 = round(float(np.min(cra_pivot['overall_score']))-float(np.min(og_cra['overall_score'])),3)
    cl5.metric(label="Updated Sample Minimum",
               value=round(float(np.min(cra_pivot['overall_score'])), 3),
               delta=deltacl5,
               delta_color="inverse"
               )
    deltacl6 = round(float(np.max(cra_pivot['overall_score']))-float(np.max(og_cra['overall_score'])),1)
    cl6.metric(label="Updated Sample Maximum",
               value=round(float(np.max(cra_pivot['overall_score'])), 1),
               delta=deltacl6,
               delta_color="inverse"
               )


    col1, col2 = st.columns(2)
    col1.dataframe(original_split,
                   column_config={
                       "overall_risk_score_rating": "Risk",
                       "count": "Count",
                       "perc": "%"
                   },
                   hide_index=True,
                   )

    fig1 = px.bar(original_split,
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

    col1.plotly_chart(fig1, use_container_width=True)

    col2.dataframe(hypothetical_split,
                   column_config={
                       "overall_risk_score_rating": "Risk",
                       "count": "Count",
                       "perc": "%"
                   },
                   hide_index=True,
                   )

    fig2 = px.bar(hypothetical_split,
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
    col2.plotly_chart(fig2, use_container_width=True)
