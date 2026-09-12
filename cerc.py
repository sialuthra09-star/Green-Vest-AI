import pandas as pd


cerc_data = {
    "Parameter": [
        "Debt_Equity_Ratio_Debt",
        "Debt_Equity_Ratio_Equity",
        "Loan_Tenure_Years",
        "Loan_Interest_Margin_%",
        "Salvage_Value_%",
        "Depreciation_Rate_%",
        "Return_on_Equity_%",
        "Hours_per_Year",
        "OM_Escalation_%",
        "Working_Capital_OM_Months",
        "Receivables_Days",
        "Maintenance_Spares_%_of_OM",
        "Working_Capital_Interest_Margin_%",
        "Solar_PV_Minimum_CUF_%",
        "Solar_PV_Auxiliary_Consumption_%"
    ],

    "Value": [
        70,
        30,
        15,
        2.00,
        10.00,
        4.67,
        14.00,
        8766,
        5.25,
        1,
        45,
        15.00,
        3.25,
        21.00,
        0.75
    ]
}

cerc = pd.DataFrame(cerc_data)

# Display the raw CERC data
print("\nRaw CERC Parameters:")
print(cerc.to_string(index=False))



print("Rows and columns:", cerc.shape)


print("\nData types:")
print(cerc.dtypes)


print("\nMissing values:")
print(cerc.isnull().sum())


print("\nDuplicate rows:", cerc.duplicated().sum())


print("Duplicate parameters:",
      cerc["Parameter"].duplicated().sum())


print("\nNegative values:")
print(cerc["Value"].lt(0).sum())


print("\nCERC Data:")
print(cerc.to_string(index=False))



# 1. Convert Debt-Equity ratio into proportions
cerc["Debt_Ratio"] = None
cerc["Equity_Ratio"] = None

cerc.loc[
    cerc["Parameter"] == "Debt_Equity_Ratio_Debt",
    "Debt_Ratio"
] = cerc.loc[
    cerc["Parameter"] == "Debt_Equity_Ratio_Debt",
    "Value"
] / 100

cerc.loc[
    cerc["Parameter"] == "Debt_Equity_Ratio_Equity",
    "Equity_Ratio"
] = cerc.loc[
    cerc["Parameter"] == "Debt_Equity_Ratio_Equity",
    "Value"
] / 100


# 2. Calculate maximum depreciation allowed
# CERC allows depreciation up to 90% of capital cost
cerc["Depreciable_Capital_%"] = None

cerc.loc[
    cerc["Parameter"] == "Depreciation_Rate_%",
    "Depreciable_Capital_%"
] = 90


# 3. Calculate effective solar generation after
# maximum auxiliary consumption
cerc["Net_Generation_%"] = None

cerc.loc[
    cerc["Parameter"] == "Solar_PV_Auxiliary_Consumption_%",
    "Net_Generation_%"
] = 100 - cerc.loc[
    cerc["Parameter"] == "Solar_PV_Auxiliary_Consumption_%",
    "Value"
]


# 4. Display the processed CERC data
print("\nProcessed CERC Data:")
print(cerc.to_string(index=False))
