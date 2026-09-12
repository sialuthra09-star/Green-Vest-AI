import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime



st.set_page_config(
    page_title="GreenVest AI",
    page_icon="🌱",
    layout="wide"
)



IEX_URL = (
    "https://www.iexindia.com/market-data/"
    "day-ahead-market/market-snapshot"
    "?dp=LAST_31_DAYS&fromDate=1"
    "&interval=ONE_FOURTH_HOUR&toDate=1"
)

MNRE_URL = (
    "https://mnre.gov.in/en/physical-progress/"
)

CERC_URL = (
    "https://cercind.gov.in/current_reg.html"
)

NREL_URL = (
    "https://nrel.gov/docs/fy12osti/51664.pdf"
)

NREL_ATB_URL = (
    "https://atb.nrel.gov/electricity/2021/residential_pv"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
    )
}


IEX_MEAN = 5231.326159274195
IEX_MEDIAN = 3730.765
IEX_STD = 3529.962255193287
IEX_MIN = 99.91
IEX_MAX = 10000.0

IEX_CAP_PRICE = 10000.0
IEX_CAP_COUNT = 937
IEX_TOTAL_OBS = 2976
IEX_CAP_PERCENT = 31.485215053763444

IEX_SIM_MEAN = 6467.575268541666
IEX_SIM_MEDIAN = 6416.28
IEX_SIM_CAP_PERCENT = 46.48854166666666

IEX_MEAN_DIFFERENCE = 1236.2491092674718
IEX_MEDIAN_DIFFERENCE = 2685.515
IEX_CAP_DIFFERENCE = 15.00332661290322

IEX_LOW_THRESHOLD = 2011.6118
IEX_HIGH_THRESHOLD = 3499.879

IEX_REGIME_PERCENTAGES = {
    "Low": 22.614247,
    "Normal": 23.286290,
    "High": 22.614247,
    "Capped": 31.485215
}

IEX_REGIME_MEANS = {
    "Low": 1435.552437,
    "Normal": 2786.241934,
    "High": 4905.548588,
    "Capped": 10000.0
}

IEX_TRANSITION_MATRIX = pd.DataFrame(
    [
        [0.9539, 0.0461, 0.0000, 0.0000],
        [0.0447, 0.8773, 0.0779, 0.0000],
        [0.0000, 0.0802, 0.8559, 0.0639],
        [0.0000, 0.0000, 0.0459, 0.9541]
    ],
    index=["Low", "Normal", "High", "Capped"],
    columns=["Low", "Normal", "High", "Capped"]
)


NREL_MEDIAN_DEGRADATION = 0.75
NREL_BASE_DEGRADATION = 0.50
NREL_MODERN_N_LOWER = 0.30
NREL_MODERN_N_UPPER = 0.40
NREL_TYPICAL_LOWER = 0.40
NREL_TYPICAL_UPPER = 0.60


MNRE_DATA = pd.DataFrame({
    "Financial Year": [
        "2014-15", "2015-16", "2016-17", "2017-18",
        "2018-19", "2019-20", "2020-21", "2021-22",
        "2022-23", "2023-24", "2024-25"
    ],
    "Installed Capacity GW": [
        3.99, 7.12, 12.78, 22.35, 29.10,
        35.60, 41.24, 54.00, 66.78, 81.81, 105.65
    ],
    "Solar Generation BU": [
        4.60, 7.45, 13.50, 25.80, 39.27,
        50.13, 60.40, 73.48, 102.01, 115.98, 144.15
    ],
    "Generation per MW MWh": [
        1152.88, 1046.35, 1056.34, 1154.36,
        1349.48, 1408.15, 1464.60, 1360.74,
        1527.55, 1417.68, 1364.41
    ],
    "Implied CUF %": [
        13.16, 11.94, 12.06, 13.18, 15.41,
        16.07, 16.72, 15.53, 17.44, 16.18, 15.58
    ]
})


CERC = {
    "debt_ratio": 0.70,
    "equity_ratio": 0.30,
    "loan_tenure": 15,
    "loan_interest_margin": 2.00,
    "salvage_value": 10.00,
    "depreciation_rate": 4.67,
    "return_on_equity": 14.00,
    "hours_per_year": 8766,
    "om_escalation": 5.25,
    "working_capital_om_months": 1,
    "receivables_days": 45,
    "maintenance_spares": 15.00,
    "working_capital_interest": 3.25,
    "minimum_cuf": 21.00,
    "auxiliary_consumption": 0.75
}

def download_page(url, timeout=30):
    """
    Downloads a webpage.
    Returns text if successful.
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout
    )

    response.raise_for_status()

    return response.text



def fetch_live_iex():

    try:

        html = download_page(IEX_URL)

        tables = pd.read_html(html)

        if len(tables) == 0:
            raise ValueError("No IEX table found.")

        # Find the table containing MCP
        iex_table = None

        for table in tables:

            columns = [
                str(c).lower()
                for c in table.columns
            ]

            if any("mcp" in c for c in columns):
                iex_table = table
                break

        if iex_table is None:
            raise ValueError("IEX MCP column not found.")

        # Flatten multi-index columns if necessary
        if isinstance(iex_table.columns, pd.MultiIndex):
            iex_table.columns = [
                " ".join(
                    [str(x) for x in col if str(x) != "nan"]
                ).strip()
                for col in iex_table.columns
            ]

        # Locate MCP column
        mcp_column = None

        for column in iex_table.columns:

            if "mcp" in str(column).lower():

                mcp_column = column
                break

        if mcp_column is None:
            raise ValueError("MCP column not found.")

        mcp = (
            iex_table[mcp_column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+(?:\.\d+)?)")[0]
        )

        mcp = pd.to_numeric(
            mcp,
            errors="coerce"
        ).dropna()

        # Remove impossible/non-market values
        mcp = mcp[
            (mcp >= 0) &
            (mcp <= 10000)
        ]

        if len(mcp) < 50:
            raise ValueError(
                "Too few valid IEX observations."
            )

        mean = float(mcp.mean())
        median = float(mcp.median())
        std = float(mcp.std())
        minimum = float(mcp.min())
        maximum = float(mcp.max())

        cap_count = int(
            np.sum(
                np.isclose(
                    mcp.values,
                    10000,
                    atol=0.01
                )
            )
        )

        cap_percent = (
            cap_count / len(mcp) * 100
        )

        # Data-driven regimes
        low_threshold = float(
            mcp.quantile(0.33)
        )

        high_threshold = float(
            mcp.quantile(0.66)
        )

        regimes = []

        for price in mcp:

            if price >= 10000:

                regimes.append("Capped")

            elif price <= low_threshold:

                regimes.append("Low")

            elif price <= high_threshold:

                regimes.append("Normal")

            else:

                regimes.append("High")

        regime_series = pd.Series(
            regimes
        )

        regime_percentages = (
            regime_series.value_counts(
                normalize=True
            ) * 100
        )

        regime_means = {}

        for regime in [
            "Low",
            "Normal",
            "High",
            "Capped"
        ]:

            values = mcp[
                regime_series.values == regime
            ]

            if len(values) > 0:

                regime_means[regime] = float(
                    values.mean()
                )

            else:

                regime_means[regime] = 0.0

        return {
            "success": True,
            "source": IEX_URL,
            "retrieved_at": datetime.now().strftime(
                "%d %B %Y, %H:%M"
            ),
            "mean": mean,
            "median": median,
            "std": std,
            "min": minimum,
            "max": maximum,
            "cap_count": cap_count,
            "total_obs": len(mcp),
            "cap_percent": cap_percent,
            "low_threshold": low_threshold,
            "high_threshold": high_threshold,
            "regime_percentages": {
                x: float(
                    regime_percentages.get(
                        x,
                        0
                    )
                )
                for x in [
                    "Low",
                    "Normal",
                    "High",
                    "Capped"
                ]
            },
            "regime_means": regime_means
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }



def fetch_live_mnre():

    try:

        html = download_page(MNRE_URL)

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        text = soup.get_text(
            " ",
            strip=True
        )

        # Find current cumulative solar capacity.
        # Example:
        # Solar Power (Cumulative) : 168.04GW
        pattern = (
            r"Solar Power\s*\(Cumulative\)"
            r".{0,100}?"
            r"(\d+(?:\.\d+)?)\s*GW"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            current_capacity = float(
                match.group(1)
            )

        else:

            # Search the cumulative installed
            # solar capacity number.
            capacity_pattern = (
                r"Solar Power.*?"
                r"Cumulative.*?"
                r"(\d+(?:\.\d+)?)\s*GW"
            )

            match = re.search(
                capacity_pattern,
                text,
                flags=re.IGNORECASE
            )

            if not match:
                raise ValueError(
                    "Current MNRE solar capacity not found."
                )

            current_capacity = float(
                match.group(1)
            )

        
        latest_existing = MNRE_DATA.iloc[-1].copy()

        latest_existing[
            "Financial Year"
        ] = "Current MNRE"

        latest_existing[
            "Installed Capacity GW"
        ] = current_capacity

        updated_data = pd.concat(
            [
                MNRE_DATA,
                pd.DataFrame(
                    [latest_existing]
                )
            ],
            ignore_index=True
        )

        return {
            "success": True,
            "source": MNRE_URL,
            "retrieved_at": datetime.now().strftime(
                "%d %B %Y, %H:%M"
            ),
            "current_capacity_gw": current_capacity,
            "data": updated_data
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "data": MNRE_DATA
        }




    try:

        html = download_page(
            NREL_ATB_URL
        )

        text = BeautifulSoup(
            html,
            "html.parser"
        ).get_text(
            " ",
            strip=True
        )

        # Search for a 0.5%/yr statement
        if re.search(
            r"0\.5%\s*/?\s*yr",
            text,
            flags=re.IGNORECASE
        ):

            base_degradation = 0.50

        else:

            base_degradation = (
                NREL_BASE_DEGRADATION
            )

        # Search for the common 0.7% figure
        if re.search(
            r"0\.7%\s*/?\s*yr",
            text,
            flags=re.IGNORECASE
        ):

            current_baseline = 0.70

        else:

            current_baseline = 0.70

        return {
            "success": True,
            "source": NREL_ATB_URL,
            "retrieved_at": datetime.now().strftime(
                "%d %B %Y, %H:%M"
            ),
            "base_degradation": base_degradation,
            "baseline_degradation": current_baseline,
            "median_degradation": 0.50
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "base_degradation":
                NREL_BASE_DEGRADATION,
            "baseline_degradation": 0.70,
            "median_degradation": 0.50
        }




def fetch_live_cerc():

    try:

        html = download_page(
            CERC_URL
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        text = soup.get_text(
            " ",
            strip=True
        )

        if "2026" not in text:
            raise ValueError(
                "CERC current-regulations page did not "
                "contain expected current entries."
            )

        
        renewable_matches = re.findall(
            r"renewable energy",
            text,
            flags=re.IGNORECASE
        )

        renewable_count = len(
            renewable_matches
        )

        return {
            "success": True,
            "source": CERC_URL,
            "retrieved_at": datetime.now().strftime(
                "%d %B %Y, %H:%M"
            ),
            "renewable_regulation_mentions":
                renewable_count,
            "text": text[:12000]
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "text": ""
        }




@st.cache_data(ttl=3600)
def load_live_sources():

    iex = fetch_live_iex()
    mnre = fetch_live_mnre()
    nrel = fetch_live_nrel()
    cerc = fetch_live_cerc()

    return {
        "iex": iex,
        "mnre": mnre,
        "nrel": nrel,
        "cerc": cerc
    }



def retrieve_evidence(
    query,
    sources,
    top_k=5
):
    """
    Lightweight local RAG-style retrieval.

    It does not calculate financial results.
    It retrieves relevant source evidence.
    """

    documents = []

    if sources["cerc"]["success"]:

        documents.append({
            "source": "CERC",
            "url": CERC_URL,
            "text": sources["cerc"]["text"]
        })

    if sources["mnre"]["success"]:

        mnre_text = (
            "MNRE current solar capacity: "
            f"{sources['mnre']['current_capacity_gw']} GW. "
            "MNRE historical solar data is also used "
            "as a generation benchmark."
        )

        documents.append({
            "source": "MNRE",
            "url": MNRE_URL,
            "text": mnre_text
        })

    if sources["nrel"]["success"]:

        nrel_text = (
            "NREL solar degradation evidence. "
            "GreenVest base degradation: "
            f"{sources['nrel']['base_degradation']}% per year. "
            "NREL source: photovoltaic degradation research."
        )

        documents.append({
            "source": "NREL",
            "url": NREL_URL,
            "text": nrel_text
        })

    if sources["iex"]["success"]:

        iex_text = (
            "IEX Day-Ahead Market 15-minute data. "
            f"Mean MCP: ₹{sources['iex']['mean']:,.2f}/MWh. "
            f"Median MCP: ₹{sources['iex']['median']:,.2f}/MWh. "
            f"Cap frequency: "
            f"{sources['iex']['cap_percent']:.2f}%."
        )

        documents.append({
            "source": "IEX",
            "url": IEX_URL,
            "text": iex_text
        })

    # Simple keyword scoring.
    query_words = set(
        re.findall(
            r"[a-zA-Z]+",
            query.lower()
        )
    )

    scored = []

    for doc in documents:

        doc_words = set(
            re.findall(
                r"[a-zA-Z]+",
                doc["text"].lower()
            )
        )

        score = len(
            query_words.intersection(
                doc_words
            )
        )

        scored.append(
            (
                score,
                doc
            )
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        doc
        for _, doc in scored[:top_k]
    ]




def calculate_generation(
    capacity_mw,
    cuf,
    project_life,
    degradation_rate,
    hours_per_year,
    auxiliary_rate
):

    gross_year_1_mwh = (
        capacity_mw
        * hours_per_year
        * (cuf / 100)
    )

    rows = []

    for year in range(
        1,
        project_life + 1
    ):

        degradation_factor = (
            (1 - degradation_rate / 100)
            ** (year - 1)
        )

        gross_generation = (
            gross_year_1_mwh
            * degradation_factor
        )

        auxiliary_consumption = (
            gross_generation
            * auxiliary_rate / 100
        )

        net_generation = (
            gross_generation
            - auxiliary_consumption
        )

        rows.append({
            "Year": year,
            "Gross Generation (MWh)":
                gross_generation,
            "Auxiliary Consumption (MWh)":
                auxiliary_consumption,
            "Net Generation (MWh)":
                net_generation,
            "Degradation Factor":
                degradation_factor
        })

    return pd.DataFrame(rows)


def calculate_irr(cashflows):

    def npv_function(rate):

        if rate <= -1:
            return np.inf

        return sum(
            cf / ((1 + rate) ** i)
            for i, cf in enumerate(
                cashflows
            )
        )

    rate = 0.10

    for _ in range(100):

        value = npv_function(rate)

        derivative = sum(
            -i * cf /
            ((1 + rate) ** (i + 1))
            for i, cf in enumerate(
                cashflows
            )
            if i > 0
        )

        if abs(derivative) < 1e-12:
            break

        new_rate = (
            rate - value / derivative
        )

        if abs(
            new_rate - rate
        ) < 1e-7:

            return new_rate * 100

        rate = new_rate

    return None


def calculate_financials(
    capacity_mw,
    capital_cost_crore,
    tariff,
    project_life,
    cuf,
    om_per_mw_lakh,
    discount_rate,
    degradation_rate
):

    generation_df = calculate_generation(
        capacity_mw,
        cuf,
        project_life,
        degradation_rate,
        CERC["hours_per_year"],
        CERC["auxiliary_consumption"]
    )

    initial_om_lakh = (
        capacity_mw
        * om_per_mw_lakh
    )

    rows = []

    initial_investment = (
        capital_cost_crore
    )

    for _, row in generation_df.iterrows():

        year = int(
            row["Year"]
        )

        net_generation_mwh = row[
            "Net Generation (MWh)"
        ]

        generation_kwh = (
            net_generation_mwh * 1000
        )

        revenue_rupees = (
            generation_kwh * tariff
        )

        revenue_crore = (
            revenue_rupees / 10_000_000
        )

        om_lakh = (
            initial_om_lakh
            * (
                (1 + CERC["om_escalation"] / 100)
                ** (year - 1)
            )
        )

        om_crore = (
            om_lakh / 100
        )

        debt_initial = (
            capital_cost_crore
            * CERC["debt_ratio"]
        )

        if year <= CERC["loan_tenure"]:

            annual_principal = (
                debt_initial
                / CERC["loan_tenure"]
            )

            beginning_debt = (
                debt_initial
                - annual_principal
                * (year - 1)
            )

            interest_rate = (
                CERC["loan_interest_margin"]
                / 100
            )

            interest = (
                beginning_debt
                * interest_rate
            )

            principal = (
                annual_principal
            )

        else:

            interest = 0
            principal = 0

        debt_service = (
            interest + principal
        )

        operating_cash_flow = (
            revenue_crore
            - om_crore
        )

        equity_cash_flow = (
            operating_cash_flow
            - debt_service
        )

        salvage = 0

        if year == project_life:

            salvage = (
                capital_cost_crore
                * CERC["salvage_value"]
                / 100
            )

        equity_cash_flow += salvage

        rows.append({
            "Year": year,
            "Gross Generation (MWh)":
                row["Gross Generation (MWh)"],
            "Net Generation (MWh)":
                net_generation_mwh,
            "Revenue (₹ crore)":
                revenue_crore,
            "O&M (₹ crore)":
                om_crore,
            "Interest (₹ crore)":
                interest,
            "Principal (₹ crore)":
                principal,
            "Operating Cash Flow (₹ crore)":
                operating_cash_flow,
            "Salvage Value (₹ crore)":
                salvage,
            "Equity Cash Flow (₹ crore)":
                equity_cash_flow
        })

    df = pd.DataFrame(rows)

    project_cashflows = [
        -initial_investment
    ]

    for value in df[
        "Operating Cash Flow (₹ crore)"
    ]:

        project_cashflows.append(
            value
        )

    if project_life > 0:

        project_cashflows[-1] += (
            capital_cost_crore
            * CERC["salvage_value"]
            / 100
        )

    discount = (
        discount_rate / 100
    )

    npv = 0

    for t, cashflow in enumerate(
        project_cashflows
    ):

        npv += (
            cashflow
            / ((1 + discount) ** t)
        )

    irr = calculate_irr(
        project_cashflows
    )

    cumulative = (
        -initial_investment
    )

    payback = None

    for _, row in df.iterrows():

        cumulative += row[
            "Operating Cash Flow (₹ crore)"
        ]

        if (
            cumulative >= 0
            and payback is None
        ):

            payback = int(
                row["Year"]
            )

    df[
        "Cumulative Operating Cash Flow (₹ crore)"
    ] = (
        -initial_investment
        + df[
            "Operating Cash Flow (₹ crore)"
        ].cumsum()
    )

    return (
        df,
        npv,
        irr,
        payback
    )



def scenario_analysis(
    capacity,
    capital_cost,
    tariff,
    project_life,
    cuf,
    om,
    discount_rate,
    degradation_rate
):

    scenarios = {

        "Base Case": {
            "tariff_factor": 1.00,
            "cuf_factor": 1.00,
            "cost_factor": 1.00
        },

        "Downside": {
            "tariff_factor": 0.90,
            "cuf_factor": 0.95,
            "cost_factor": 1.10
        },

        "Stress": {
            "tariff_factor": 0.80,
            "cuf_factor": 0.90,
            "cost_factor": 1.20
        }
    }

    results = []

    for name, assumptions in (
        scenarios.items()
    ):

        scenario_tariff = (
            tariff
            * assumptions["tariff_factor"]
        )

        scenario_cuf = (
            cuf
            * assumptions["cuf_factor"]
        )

        scenario_om = (
            om
            * assumptions["cost_factor"]
        )

        _, npv, irr, payback = (
            calculate_financials(
                capacity,
                capital_cost,
                scenario_tariff,
                project_life,
                scenario_cuf,
                scenario_om,
                discount_rate,
                degradation_rate
            )
        )

        results.append({
            "Scenario": name,
            "Tariff (₹/kWh)":
                scenario_tariff,
            "CUF (%)":
                scenario_cuf,
            "O&M (₹ lakh/MW)":
                scenario_om,
            "NPV (₹ crore)":
                npv,
            "IRR (%)":
                irr,
            "Payback (years)":
                payback
        })

    return pd.DataFrame(
        results
    )




def monte_carlo_npv(
    capacity,
    capital_cost,
    tariff,
    project_life,
    cuf,
    om,
    discount_rate,
    degradation_rate,
    iex_std,
    iex_mean,
    simulations=1000
):

    rng = np.random.default_rng(
        42
    )

    npvs = []

    price_cv = (
        iex_std / max(
            iex_mean,
            1
        )
    )

    for _ in range(
        simulations
    ):

        market_factor = (
            rng.normal(
                1.0,
                min(
                    price_cv * 0.20,
                    0.50
                )
            )
        )

        market_factor = max(
            0.50,
            min(
                market_factor,
                1.50
            )
        )

        generation_factor = (
            rng.normal(
                1.0,
                0.05
            )
        )

        generation_factor = max(
            0.80,
            min(
                generation_factor,
                1.20
            )
        )

        om_factor = (
            rng.normal(
                1.0,
                0.05
            )
        )

        om_factor = max(
            0.90,
            min(
                om_factor,
                1.15
            )
        )

        scenario_tariff = (
            tariff
            * market_factor
        )

        scenario_cuf = (
            cuf
            * generation_factor
        )

        scenario_om = (
            om
            * om_factor
        )

        _, npv, _, _ = (
            calculate_financials(
                capacity,
                capital_cost,
                scenario_tariff,
                project_life,
                scenario_cuf,
                scenario_om,
                discount_rate,
                degradation_rate
            )
        )

        npvs.append(
            npv
        )

    return np.array(
        npvs
    )



def investment_assessment(
    npv,
    irr,
    payback,
    negative_npv_probability,
    downside_npv,
    stress_npv,
    project_cuf,
    mnre_cuf,
    iex_cap_percent
):

    reasons = []

    if npv > 0:

        reasons.append(
            "The base-case project NPV is positive."
        )

    else:

        reasons.append(
            "The base-case project NPV is negative."
        )

    if (
        irr is not None
        and irr > 10
    ):

        reasons.append(
            "The project IRR is above the "
            "10% reference level."
        )

    else:

        reasons.append(
            "The project IRR does not provide "
            "a strong return margin."
        )

    if (
        negative_npv_probability < 20
    ):

        risk_level = "relatively low"

    elif (
        negative_npv_probability < 40
    ):

        risk_level = "moderate"

    else:

        risk_level = "high"

    reasons.append(
        f"Monte Carlo analysis indicates a "
        f"{risk_level} probability of negative NPV."
    )

    if downside_npv < 0:

        reasons.append(
            "The downside scenario produces "
            "a negative NPV."
        )

    if stress_npv < 0:

        reasons.append(
            "The stress scenario produces "
            "a negative NPV."
        )

    if project_cuf > mnre_cuf:

        reasons.append(
            "The project's CUF is above the "
            "latest available MNRE benchmark."
        )

    else:

        reasons.append(
            "The project's CUF is at or below "
            "the available MNRE benchmark."
        )

    if iex_cap_percent > 25:

        reasons.append(
            "IEX data show a substantial frequency "
            "of prices at the market cap."
        )

    reasons.append(
        "IEX market-price behaviour is treated as "
        "uncertainty rather than as a guaranteed "
        "future selling price."
    )

    if (
        npv > 0
        and irr is not None
        and irr > 10
        and negative_npv_probability < 20
        and downside_npv > 0
    ):

        recommendation = "INVEST"

    elif (
        npv > 0
        and irr is not None
        and irr > 8
    ):

        recommendation = (
            "INVEST WITH CAUTION"
        )

    else:

        recommendation = (
            "NOT RECOMMENDED"
        )

    return (
        recommendation,
        reasons
    )




st.title(
    "🌱 GREENVEST AI"
)

st.subheader(
    "Solar Project Investment Analysis"
)

st.write(
    "Enter the basic project information and let "
    "GreenVest combine live official data, financial "
    "analysis, generation modelling, market-price "
    "uncertainty and risk analysis."
)

st.divider()


col1, col2 = st.columns(2)

with col1:

    capacity = st.number_input(
        "Project Capacity (MW)",
        min_value=0.1,
        value=10.0,
        step=0.5
    )

    capital_cost = st.number_input(
        "Total Capital Cost (₹ crore)",
        min_value=0.1,
        value=45.0,
        step=1.0
    )

    tariff = st.number_input(
        "Electricity Selling Price / Tariff (₹/kWh)",
        min_value=0.01,
        value=3.50,
        step=0.10
    )

    project_life = st.number_input(
        "Project Life (years)",
        min_value=1,
        value=25,
        step=1
    )

with col2:

    cuf = st.number_input(
        "Expected CUF (%)",
        min_value=0.1,
        max_value=100.0,
        value=21.0,
        step=0.5
    )

    om = st.number_input(
        "Annual O&M Cost (₹ lakh/MW/year)",
        min_value=0.0,
        value=7.0,
        step=0.5
    )

    discount_rate = st.number_input(
        "Required Return / Discount Rate (%)",
        min_value=0.1,
        value=10.0,
        step=0.5
    )

st.divider()

analyze = st.button(
    "🚀 GIVE ME THE ANALYSIS",
    use_container_width=True
)


if analyze:

    
    if capacity <= 0:
        st.error(
            "Project capacity must be greater than zero."
        )
        st.stop()

    if capital_cost <= 0:
        st.error(
            "Capital cost must be greater than zero."
        )
        st.stop()

    if tariff <= 0:
        st.error(
            "Tariff must be greater than zero."
        )
        st.stop()

    if project_life <= 0:
        st.error(
            "Project life must be greater than zero."
        )
        st.stop()

    if cuf <= 0 or cuf > 100:
        st.error(
            "CUF must be between 0% and 100%."
        )
        st.stop()

    
    with st.spinner(
        "🌐 Fetching latest official CERC, MNRE, "
        "NREL and IEX information..."
    ):

        sources = load_live_sources()

   
    if sources["iex"]["success"]:

        iex_live = sources["iex"]

        live_iex = True

        current_iex_mean = (
            iex_live["mean"]
        )

        current_iex_median = (
            iex_live["median"]
        )

        current_iex_std = (
            iex_live["std"]
        )

        current_iex_min = (
            iex_live["min"]
        )

        current_iex_max = (
            iex_live["max"]
        )

        current_iex_cap_percent = (
            iex_live["cap_percent"]
        )

        current_iex_cap_count = (
            iex_live["cap_count"]
        )

        current_iex_total_obs = (
            iex_live["total_obs"]
        )

        current_iex_low_threshold = (
            iex_live["low_threshold"]
        )

        current_iex_high_threshold = (
            iex_live["high_threshold"]
        )

        current_iex_regime_percentages = (
            iex_live["regime_percentages"]
        )

        current_iex_regime_means = (
            iex_live["regime_means"]
        )

    else:

        live_iex = None

        live_iex = False

        current_iex_mean = IEX_MEAN
        current_iex_median = IEX_MEDIAN
        current_iex_std = IEX_STD
        current_iex_min = IEX_MIN
        current_iex_max = IEX_MAX
        current_iex_cap_percent = IEX_CAP_PERCENT
        current_iex_cap_count = IEX_CAP_COUNT
        current_iex_total_obs = IEX_TOTAL_OBS
        current_iex_low_threshold = IEX_LOW_THRESHOLD
        current_iex_high_threshold = IEX_HIGH_THRESHOLD
        current_iex_regime_percentages = (
            IEX_REGIME_PERCENTAGES
        )
        current_iex_regime_means = (
            IEX_REGIME_MEANS
        )

   

    mnre_data = sources[
        "mnre"
    ].get(
        "data",
        MNRE_DATA
    )

    if sources["mnre"]["success"]:

        latest_mnre_capacity = (
            sources["mnre"][
                "current_capacity_gw"
            ]
        )

        live_mnre = True

    else:

        latest_mnre_capacity = (
            MNRE_DATA[
                "Installed Capacity GW"
            ].iloc[-1]
        )

        live_mnre = False

    # Historical benchmark remains available.
    latest_mnre_cuf = (
        MNRE_DATA[
            "Implied CUF %"
        ].iloc[-1]
    )


    if sources["nrel"]["success"]:

        degradation_rate = (
            sources["nrel"][
                "base_degradation"
            ]
        )

        live_nrel = True

    else:

        degradation_rate = (
            NREL_BASE_DEGRADATION
        )

        live_nrel = False

    

    live_cerc = (
        sources["cerc"]["success"]
    )

    
    with st.spinner(
        "📊 Running GreenVest financial and risk analysis..."
    ):

        financial_df, npv, irr, payback = (
            calculate_financials(
                capacity,
                capital_cost,
                tariff,
                int(project_life),
                cuf,
                om,
                discount_rate,
                degradation_rate
            )
        )

        scenarios = scenario_analysis(
            capacity,
            capital_cost,
            tariff,
            int(project_life),
            cuf,
            om,
            discount_rate,
            degradation_rate
        )

        npv_simulations = (
            monte_carlo_npv(
                capacity,
                capital_cost,
                tariff,
                int(project_life),
                cuf,
                om,
                discount_rate,
                degradation_rate,
                current_iex_std,
                current_iex_mean,
                simulations=1000
            )
        )

        mean_npv = np.mean(
            npv_simulations
        )

        median_npv = np.median(
            npv_simulations
        )

        negative_npv_probability = (
            np.mean(
                npv_simulations < 0
            )
            * 100
        )

        p5_npv = np.percentile(
            npv_simulations,
            5
        )

        p95_npv = np.percentile(
            npv_simulations,
            95
        )

  

    downside_npv = scenarios.loc[
        scenarios["Scenario"] == "Downside",
        "NPV (₹ crore)"
    ].iloc[0]

    stress_npv = scenarios.loc[
        scenarios["Scenario"] == "Stress",
        "NPV (₹ crore)"
    ].iloc[0]

    
    rag_query = (
        "solar project investment "
        "financial risk generation "
        "electricity price degradation "
        "regulation"
    )

    evidence = retrieve_evidence(
        rag_query,
        sources
    )

    
    recommendation, reasons = (
        investment_assessment(
            npv,
            irr,
            payback,
            negative_npv_probability,
            downside_npv,
            stress_npv,
            cuf,
            latest_mnre_cuf,
            current_iex_cap_percent
        )
    )

   

    st.success(
        "Analysis completed successfully."
    )

    

    st.header(
        "🌐 Live Data Status"
    )

    status_cols = st.columns(4)

    status_items = [
        (
            "IEX",
            live_iex
        ),
        (
            "MNRE",
            live_mnre
        ),
        (
            "NREL",
            live_nrel
        ),
        (
            "CERC",
            live_cerc
        )
    ]

    for col, (
        name,
        status
    ) in zip(
        status_cols,
        status_items
    ):

        with col:

            if status:

                st.success(
                    f"✓ {name}: LIVE"
                )

            else:

                st.warning(
                    f"⚠ {name}: FALLBACK"
                )

    st.caption(
        "GreenVest uses official-source data when "
        "available and falls back to the last "
        "validated model values if a source is "
        "temporarily unavailable."
    )

    

    st.header(
        "1. Overall Investment Assessment"
    )

    if recommendation == "INVEST":

        st.success(
            f"### {recommendation}"
        )

    elif recommendation == (
        "INVEST WITH CAUTION"
    ):

        st.warning(
            f"### {recommendation}"
        )

    else:

        st.error(
            f"### {recommendation}"
        )

    for reason in reasons:

        st.write(
            "•",
            reason
        )

   
    st.header(
        "2. Project Summary"
    )

    summary_cols = st.columns(7)

    summary_values = [
        (
            "Capacity",
            f"{capacity:.2f} MW"
        ),
        (
            "Capital Cost",
            f"₹{capital_cost:.2f} Cr"
        ),
        (
            "Tariff",
            f"₹{tariff:.2f}/kWh"
        ),
        (
            "Project Life",
            f"{project_life} years"
        ),
        (
            "CUF",
            f"{cuf:.2f}%"
        ),
        (
            "O&M",
            f"₹{om:.2f} Lakh/MW"
        ),
        (
            "Discount Rate",
            f"{discount_rate:.2f}%"
        )
    ]

    for col, (
        label,
        value
    ) in zip(
        summary_cols,
        summary_values
    ):

        with col:

            st.metric(
                label,
                value
            )

    st.header(
        "3. Key Financial Results"
    )

    total_revenue = (
        financial_df[
            "Revenue (₹ crore)"
        ].sum()
    )

    total_om = (
        financial_df[
            "O&M (₹ crore)"
        ].sum()
    )

    cols = st.columns(5)

    with cols[0]:

        st.metric(
            "NPV",
            f"₹{npv:,.2f} Cr"
        )

    with cols[1]:

        if irr is not None:

            st.metric(
                "IRR",
                f"{irr:.2f}%"
            )

        else:

            st.metric(
                "IRR",
                "N/A"
            )

    with cols[2]:

        if payback is not None:

            st.metric(
                "Payback",
                f"{payback} years"
            )

        else:

            st.metric(
                "Payback",
                "Not achieved"
            )

    with cols[3]:

        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.2f} Cr"
        )

    with cols[4]:

        st.metric(
            "Total O&M",
            f"₹{total_om:,.2f} Cr"
        )

   
    st.header(
        "4. Generation Analysis"
    )

    year1_generation = (
        financial_df.iloc[0][
            "Net Generation (MWh)"
        ]
    )

    final_generation = (
        financial_df.iloc[-1][
            "Net Generation (MWh)"
        ]
    )

    generation_cols = st.columns(4)

    with generation_cols[0]:

        st.metric(
            "Year 1 Net Generation",
            f"{year1_generation:,.0f} MWh"
        )

    with generation_cols[1]:

        st.metric(
            "Final Year Generation",
            f"{final_generation:,.0f} MWh"
        )

    with generation_cols[2]:

        st.metric(
            "NREL Degradation",
            f"{degradation_rate:.2f}% / year"
        )

    with generation_cols[3]:

        st.metric(
            "MNRE CUF Benchmark",
            f"{latest_mnre_cuf:.2f}%"
        )

    if cuf > latest_mnre_cuf:

        st.warning(
            f"The project's CUF of "
            f"{cuf:.2f}% is above the latest "
            f"historical MNRE benchmark of "
            f"{latest_mnre_cuf:.2f}%."
        )

    else:

        st.info(
            f"The project's CUF of "
            f"{cuf:.2f}% is at or below the "
            f"historical MNRE benchmark of "
            f"{latest_mnre_cuf:.2f}%."
        )

    fig, ax = plt.subplots()

    ax.plot(
        financial_df["Year"],
        financial_df[
            "Net Generation (MWh)"
        ]
    )

    ax.set_title(
        "Annual Net Solar Generation"
    )

    ax.set_xlabel(
        "Project Year"
    )

    ax.set_ylabel(
        "Net Generation (MWh)"
    )

    st.pyplot(fig)

    st.dataframe(
        financial_df[
            [
                "Year",
                "Gross Generation (MWh)",
                "Net Generation (MWh)"
            ]
        ],
        use_container_width=True
    )

    

    st.header(
        "5. IEX Electricity Market Analysis"
    )

    st.write(
        "GreenVest retrieves the latest available "
        "IEX Day-Ahead Market observations when "
        "the official source is accessible."
    )

    iex_cols = st.columns(6)

    with iex_cols[0]:

        st.metric(
            "Mean MCP",
            f"₹{current_iex_mean:,.0f}/MWh"
        )

    with iex_cols[1]:

        st.metric(
            "Median MCP",
            f"₹{current_iex_median:,.0f}/MWh"
        )

    with iex_cols[2]:

        st.metric(
            "Std. Deviation",
            f"₹{current_iex_std:,.0f}"
        )

    with iex_cols[3]:

        st.metric(
            "Minimum",
            f"₹{current_iex_min:,.0f}"
        )

    with iex_cols[4]:

        st.metric(
            "Maximum",
            f"₹{current_iex_max:,.0f}"
        )

    with iex_cols[5]:

        st.metric(
            "At ₹10,000 Cap",
            f"{current_iex_cap_percent:.2f}%"
        )

    st.caption(
        f"Observations analysed: "
        f"{current_iex_total_obs:,}"
    )

    st.subheader(
        "IEX Price Regimes"
    )

    regime_df = pd.DataFrame({
        "Regime":
            list(
                current_iex_regime_percentages.keys()
            ),
        "Percentage":
            list(
                current_iex_regime_percentages.values()
            ),
        "Average MCP (₹/MWh)":
            [
                current_iex_regime_means[x]
                for x in
                current_iex_regime_percentages.keys()
            ]
    })

    st.dataframe(
        regime_df,
        use_container_width=True,
        hide_index=True
    )

    fig, ax = plt.subplots()

    ax.bar(
        regime_df["Regime"],
        regime_df["Percentage"]
    )

    ax.set_title(
        "IEX Price Regime Distribution"
    )

    ax.set_ylabel(
        "Percentage of Observations"
    )

    st.pyplot(fig)

    

    st.header(
        "6. Tariff vs IEX Market Benchmark"
    )

    tariff_mcp = (
        tariff * 1000
    )

    comparison_df = pd.DataFrame({
        "Price": [
            "Project Tariff",
            "IEX Mean MCP",
            "IEX Median MCP"
        ],
        "₹/MWh": [
            tariff_mcp,
            current_iex_mean,
            current_iex_median
        ]
    })

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "The IEX figures are market benchmarks "
        "and uncertainty indicators. They do not "
        "automatically replace the project's entered "
        "tariff."
    )

    

    st.header(
        "7. Financial Cash Flow"
    )

    st.dataframe(
        financial_df.style.format({
            "Gross Generation (MWh)":
                "{:,.0f}",
            "Net Generation (MWh)":
                "{:,.0f}",
            "Revenue (₹ crore)":
                "₹{:,.2f}",
            "O&M (₹ crore)":
                "₹{:,.2f}",
            "Interest (₹ crore)":
                "₹{:,.2f}",
            "Principal (₹ crore)":
                "₹{:,.2f}",
            "Operating Cash Flow (₹ crore)":
                "₹{:,.2f}",
            "Salvage Value (₹ crore)":
                "₹{:,.2f}",
            "Equity Cash Flow (₹ crore)":
                "₹{:,.2f}",
            "Cumulative Operating Cash Flow (₹ crore)":
                "₹{:,.2f}"
        }),
        use_container_width=True
    )

    fig, ax = plt.subplots()

    ax.plot(
        financial_df["Year"],
        financial_df[
            "Cumulative Operating Cash Flow (₹ crore)"
        ]
    )

    ax.axhline(
        0,
        linewidth=1
    )

    ax.set_title(
        "Cumulative Project Cash Flow"
    )

    ax.set_xlabel(
        "Project Year"
    )

    ax.set_ylabel(
        "₹ crore"
    )

    st.pyplot(fig)

   
    st.header(
        "8. Scenario Analysis"
    )

    st.dataframe(
        scenarios.style.format({
            "Tariff (₹/kWh)":
                "₹{:.2f}",
            "CUF (%)":
                "{:.2f}%",
            "O&M (₹ lakh/MW)":
                "₹{:.2f}",
            "NPV (₹ crore)":
                "₹{:,.2f}",
            "IRR (%)":
                "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    fig, ax = plt.subplots()

    ax.bar(
        scenarios["Scenario"],
        scenarios["NPV (₹ crore)"]
    )

    ax.axhline(
        0,
        linewidth=1
    )

    ax.set_title(
        "Scenario NPV Comparison"
    )

    ax.set_ylabel(
        "NPV (₹ crore)"
    )

    st.pyplot(fig)

    
    st.header(
        "9. Monte Carlo Investment Risk"
    )

    mc_cols = st.columns(5)

    with mc_cols[0]:

        st.metric(
            "Mean NPV",
            f"₹{mean_npv:,.2f} Cr"
        )

    with mc_cols[1]:

        st.metric(
            "Median NPV",
            f"₹{median_npv:,.2f} Cr"
        )

    with mc_cols[2]:

        st.metric(
            "Negative NPV Probability",
            f"{negative_npv_probability:.2f}%"
        )

    with mc_cols[3]:

        st.metric(
            "5th Percentile NPV",
            f"₹{p5_npv:,.2f} Cr"
        )

    with mc_cols[4]:

        st.metric(
            "95th Percentile NPV",
            f"₹{p95_npv:,.2f} Cr"
        )

    fig, ax = plt.subplots()

    ax.hist(
        npv_simulations,
        bins=40
    )

    ax.axvline(
        0,
        linewidth=2
    )

    ax.set_title(
        "Monte Carlo NPV Distribution"
    )

    ax.set_xlabel(
        "NPV (₹ crore)"
    )

    ax.set_ylabel(
        "Frequency"
    )

    st.pyplot(fig)

  

    st.header(
        "10. Sensitivity Analysis"
    )

    sensitivity_results = []

    for factor in [
        0.80,
        0.90,
        1.00,
        1.10,
        1.20
    ]:

        _, sensitivity_npv, _, _ = (
            calculate_financials(
                capacity,
                capital_cost,
                tariff * factor,
                int(project_life),
                cuf,
                om,
                discount_rate,
                degradation_rate
            )
        )

        sensitivity_results.append({
            "Variable": "Tariff",
            "Change":
                f"{(factor - 1) * 100:+.0f}%",
            "NPV (₹ crore)":
                sensitivity_npv
        })

    for factor in [
        0.90,
        0.95,
        1.00,
        1.05,
        1.10
    ]:

        _, sensitivity_npv, _, _ = (
            calculate_financials(
                capacity,
                capital_cost,
                tariff,
                int(project_life),
                cuf * factor,
                om,
                discount_rate,
                degradation_rate
            )
        )

        sensitivity_results.append({
            "Variable": "CUF",
            "Change":
                f"{(factor - 1) * 100:+.0f}%",
            "NPV (₹ crore)":
                sensitivity_npv
        })

    for factor in [
        0.80,
        0.90,
        1.00,
        1.10,
        1.20
    ]:

        _, sensitivity_npv, _, _ = (
            calculate_financials(
                capacity,
                capital_cost * factor,
                tariff,
                int(project_life),
                cuf,
                om,
                discount_rate,
                degradation_rate
            )
        )

        sensitivity_results.append({
            "Variable": "Capital Cost",
            "Change":
                f"{(factor - 1) * 100:+.0f}%",
            "NPV (₹ crore)":
                sensitivity_npv
        })

    sensitivity_df = pd.DataFrame(
        sensitivity_results
    )

    st.dataframe(
        sensitivity_df.style.format({
            "NPV (₹ crore)":
                "₹{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    

    st.header(
        "11. NREL Degradation Analysis"
    )

    degradation_df = pd.DataFrame({
        "Scenario": [
            "Modern N-type Lower",
            "Modern N-type Upper",
            "Typical Modelling Lower",
            "GreenVest Base",
            "Typical Modelling Upper",
            "NREL Median"
        ],
        "Degradation (%/year)": [
            NREL_MODERN_N_LOWER,
            NREL_MODERN_N_UPPER,
            NREL_TYPICAL_LOWER,
            degradation_rate,
            NREL_TYPICAL_UPPER,
            0.50
        ]
    })

    st.dataframe(
        degradation_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        f"GreenVest currently uses a "
        f"{degradation_rate:.2f}%/year degradation "
        f"assumption based on the NREL source."
    )

   
    st.header(
        "12. CERC Financial / Regulatory Evidence"
    )

    cerc_display = pd.DataFrame({
        "Parameter": [
            "Debt Ratio",
            "Equity Ratio",
            "Loan Tenure",
            "Loan Interest Margin",
            "Salvage Value",
            "Depreciation Rate",
            "Return on Equity",
            "Hours per Year",
            "O&M Escalation",
            "Working Capital O&M",
            "Receivables",
            "Maintenance Spares",
            "Working Capital Interest Margin",
            "Minimum CUF",
            "Auxiliary Consumption"
        ],
        "Value": [
            "70%",
            "30%",
            "15 years",
            "2%",
            "10%",
            "4.67%",
            "14%",
            "8766 hours",
            "5.25%",
            "1 month",
            "45 days",
            "15% of O&M",
            "3.25%",
            "21%",
            "0.75%"
        ]
    })

    st.dataframe(
        cerc_display,
        use_container_width=True,
        hide_index=True
    )

    if live_cerc:

        st.success(
            "✓ CERC current-regulations page "
            "successfully retrieved."
        )

        st.caption(
            "Live CERC evidence is used as the "
            "regulatory source layer. Existing "
            "GreenVest numerical financial assumptions "
            "remain the model assumptions unless they "
            "are explicitly mapped to a verified CERC "
            "parameter."
        )

    else:

        st.warning(
            "CERC live page was unavailable during "
            "this run. Existing validated GreenVest "
            "assumptions are being displayed."
        )

   

    st.header(
        "13. Risk Summary"
    )

    market_risk = (
        "HIGH"
        if current_iex_cap_percent >= 25
        else "MODERATE"
    )

    generation_risk = (
        "MODERATE"
        if cuf >= latest_mnre_cuf
        else "LOW-MODERATE"
    )

    financial_risk = (
        "HIGH"
        if negative_npv_probability >= 40
        else (
            "MODERATE"
            if negative_npv_probability >= 20
            else "LOW-MODERATE"
        )
    )

    risk_data = {

        "Market Risk":
            f"{market_risk} — IEX data show "
            f"{current_iex_cap_percent:.2f}% of observations "
            "at the ₹10,000/MWh cap.",

        "Generation Risk":
            f"{generation_risk} — project CUF is "
            f"{cuf:.2f}% versus the available "
            f"MNRE historical benchmark of "
            f"{latest_mnre_cuf:.2f}% and degradation "
            f"is modelled at {degradation_rate:.2f}%/year.",

        "Cost Risk":
            "MODERATE — O&M is escalated using "
            "the current GreenVest CERC assumption "
            "of 5.25% per year.",

        "Financing Risk":
            "MODELLED — debt/equity and loan-tenure "
            "assumptions are incorporated.",

        "Financial Risk":
            f"{financial_risk} — Monte Carlo estimates "
            f"a {negative_npv_probability:.2f}% probability "
            "of negative NPV."
    }

    for risk, explanation in (
        risk_data.items()
    ):

        st.write(
            f"**{risk}:** {explanation}"
        )

    

    st.header(
        "14. Supporting Evidence — RAG"
    )

    st.write(
        "GreenVest retrieves relevant information "
        "from the official source layer to support "
        "the investment explanation. The RAG layer "
        "does not calculate NPV, IRR or other "
        "financial metrics."
    )

    for item in evidence:

        with st.expander(
            f"📄 {item['source']} Evidence"
        ):

            st.write(
                item["text"][:4000]
            )

            st.caption(
                item["url"]
            )

    

    st.header(
        "15. GreenVest AI Final Assessment"
    )

    if recommendation == "INVEST":

        st.success(
            f"## {recommendation}"
        )

    elif recommendation == (
        "INVEST WITH CAUTION"
    ):

        st.warning(
            f"## {recommendation}"
        )

    else:

        st.error(
            f"## {recommendation}"
        )

    st.write(
        "GreenVest's assessment combines the calculated "
        "financial results, scenario analysis, Monte Carlo "
        "risk analysis, live market evidence and "
        "official-source contextual evidence."
    )

    st.subheader(
        "Why GreenVest reached this assessment"
    )

    for reason in reasons:

        st.write(
            "•",
            reason
        )

    
    st.header(
        "16. Official Data Sources"
    )

    source_table = pd.DataFrame({
        "Source": [
            "IEX",
            "MNRE",
            "CERC",
            "NREL"
        ],
        "Status": [
            "LIVE" if live_iex
            else "FALLBACK",
            "LIVE" if live_mnre
            else "FALLBACK",
            "LIVE" if live_cerc
            else "FALLBACK",
            "LIVE" if live_nrel
            else "FALLBACK"
        ],
        "Purpose": [
            "Electricity market price behaviour",
            "Solar capacity and generation benchmark",
            "Regulatory and tariff evidence",
            "PV degradation evidence"
        ]
    })

    st.dataframe(
        source_table,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "🌱 GreenVest AI analysis complete."
    )
