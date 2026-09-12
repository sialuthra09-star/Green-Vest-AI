import pandas as pd



nrel_data = {
    "Parameter": [
        "Median_Degradation_Rate_%",
        "Base_Degradation_Rate_%",
        "Modern_N_Type_Degradation_Lower_%",
        "Modern_N_Type_Degradation_Upper_%",
        "Typical_Modeling_Lower_%",
        "Typical_Modeling_Upper_%"
    ],

    "Value": [
        0.75,
        0.50,
        0.30,
        0.40,
        0.40,
        0.60
    ]
}

nrel = pd.DataFrame(nrel_data)

print("\nNREL Degradation Data:")
print(nrel.to_string(index=False))





print("Rows and columns:", nrel.shape)


print("\nData types:")
print(nrel.dtypes)


print("\nMissing values:")
print(nrel.isnull().sum())


print("\nDuplicate rows:", nrel.duplicated().sum())


print("Duplicate parameters:",
      nrel["Parameter"].duplicated().sum())


print("\nNegative values:")
print(nrel["Value"].lt(0).sum())


print("\nNREL Data:")
print(nrel.to_string(index=False))



# GreenVest base-case degradation assumption
degradation_rate = 0.005

print("GreenVest Base Degradation Rate:",
      degradation_rate * 100, "% per year")
