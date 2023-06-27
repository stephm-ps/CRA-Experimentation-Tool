# group proportions
CustRiskFactorProportionDefault = 0.32
CountryGeoFactorProportionDefault = 0.25
ProductServicesFactorProportionDefault = 0.22
ChannelDistFactorProportionDefault = 0.21

# group weights
CustRiskFactorWeightDefault = 3
CountryGeoFactorWeightDefault = 2
ProductServicesFactorWeightDefault = 3
ChannelDistFactorWeightDefault = 2

# store groups
groups = {
    'Customer Risk Factors':[CustRiskFactorProportionDefault,CustRiskFactorWeightDefault],
    'Country or Geographic Risk Factors':[CountryGeoFactorProportionDefault,CountryGeoFactorWeightDefault],
    'Product, Service and Transaction RIsk Factors':[ProductServicesFactorProportionDefault,ProductServicesFactorWeightDefault],
    'Channel or Distribution Risk Factors':[ChannelDistFactorProportionDefault,ChannelDistFactorWeightDefault]
}


