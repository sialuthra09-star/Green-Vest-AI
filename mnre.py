import pandas as pd

mnre_data = {
    "Financial_Year": [
        "2014-15", "2015-16", "2016-17", "2017-18", "2018-19",
        "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
    ],

    "Solar_Installed_Capacity_GW": [
        3.99, 7.12, 12.78, 22.35, 29.10,
        35.60, 41.24, 54.00, 66.78, 81.81, 105.65
    ],

    "Solar_Generation_BU": [
        4.60, 7.45, 13.50, 25.80, 39.27,
        50.13, 60.40, 73.48, 102.01, 115.98, 144.15
    ]
}

mnre = pd.DataFrame(mnre_data)

print(mnre)     


print("Rows and columns:", mnre.shape)


print("\nData types:")
print(mnre.dtypes)

print("\nMissing values:")
print(mnre.isnull().sum())

print("\nDuplicate rows:", mnre.duplicated().sum())

print("Duplicate financial years:",
      mnre["Financial_Year"].duplicated().sum())

print("\nNegative values:")
print(
    mnre[
        ["Solar_Installed_Capacity_GW", "Solar_Generation_BU"]
    ].lt(0).sum()
)



# Capacity Growth (%)
mnre["Capacity_Growth_%"] = (
    mnre["Solar_Installed_Capacity_GW"].pct_change() * 100
)

# Generation Growth (%)
mnre["Generation_Growth_%"] = (
    mnre["Solar_Generation_BU"].pct_change() * 100
)

# Generation per MW (MWh/MW)
mnre["Generation_per_MW_MWh"] = (
    mnre["Solar_Generation_BU"]
    / mnre["Solar_Installed_Capacity_GW"]
) * 1000

# Implied CUF (%)
mnre["Implied_CUF_%"] = (
    mnre["Solar_Generation_BU"]
    / (mnre["Solar_Installed_Capacity_GW"] * 8.76)
) * 100

# Round values
mnre = mnre.round(2)

# SHOW OUTPUT
print("\nProcessed MNRE Data:")
print(mnre.to_string(index=False))



mnre.to_csv("mnre_processed.csv", index=False)

print("MNRE processed data saved successfully!")
