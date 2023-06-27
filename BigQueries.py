# CRA BackBook Testing Query
def cra_backbook():
    cust_query = '''
    SELECT
    cust.customer_id,
    DATE(cust.live_date) as live_date,
    cust.primary_mcc_industry_category,
    cust.registered_company_legal_type,
    score.overall_score,
    score.overall_risk_score_rating,
    risk_factor_type,
    risk_factor_outcome


    FROM
    `data-mdm-prod.mdm_customers_output.all_customers` as cust
    RIGHT OUTER JOIN `analytics-hub-prod.staging.stg_customer_risk_score_calculated_production` as score
    ON cust.onboarding_id = score.onboarding_id
    WHERE customer_id is not null
    AND overall_score is not null
    ORDER BY customer_id
    '''
    return cust_query
