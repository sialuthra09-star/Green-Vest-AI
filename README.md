# Green-Vest-AI


https://drive.google.com/file/d/1Pi4Y0Ty4gt3QBwHb6OMm5XBLfT9CIc__/view?usp=drivesdk






🌱 GreenVest AI

AI-Powered Solar Energy Investment & Risk Analyzer

1M1B Artificial Intelligence Internship In collaboration with IBM SkillsBuild & AICTE

⸻

📌 Project Overview

GreenVest AI is an AI-powered decision-support tool designed to help investors evaluate the financial feasibility and investment risk of solar energy projects.

Investing in renewable energy requires more than estimating how much electricity a solar project can generate. Project profitability can be affected by:

Initial capital investment
Electricity prices
Solar generation
Panel degradation
Operating and maintenance costs
Financing assumptions
Market uncertainty
Changes in future cash flows
Regulatory and technical assumptions
GreenVest AI combines financial modelling, electricity-market analysis, renewable-energy data, risk analysis, Monte Carlo simulation, Retrieval-Augmented Generation (RAG), and AI-based explanation to provide a structured investment assessment.

The system converts project inputs into financial metrics such as NPV, IRR, payback period, revenue and cash flows, and then evaluates the project’s risk under different scenarios.

⸻

🎯 Problem Statement

How might we use AI and quantitative financial modelling to help investors make more informed and risk-aware decisions about solar energy investments?

Renewable energy projects require significant upfront investment and generate returns over many years. However, future electricity prices, energy generation, operating costs and other assumptions are uncertain.

Traditional project evaluation may rely on fixed assumptions and may not clearly communicate how uncertainty can affect the investment.

GreenVest AI addresses this gap by combining quantitative modelling with AI-assisted interpretation.

⸻

🌍 SDG Alignment

Primary SDG: SDG 7 — Affordable and Clean Energy

GreenVest AI directly supports Sustainable Development Goal 7, which focuses on ensuring access to affordable, reliable, sustainable and modern energy.

The project supports SDG 7 by:

Encouraging informed renewable-energy investment
Supporting solar-project feasibility analysis
Improving understanding of renewable-energy financial risks
Helping investors evaluate long-term project sustainability
Supporting evidence-based clean-energy decision making
Secondary relevance

The project also has relevance to:

SDG 8 — Decent Work and Economic Growth
SDG 9 — Industry, Innovation and Infrastructure
SDG 13 — Climate Action
However, SDG 7 remains the primary focus.

⸻

👥 Target Users

GreenVest AI is designed as a decision-support prototype for:

Renewable-energy investors
Solar project developers
Financial analysts
Students learning financial mathematics
Sustainability analysts
Energy-sector researchers
Individuals evaluating solar-project feasibility
The tool is not intended to replace professional financial, engineering or regulatory due diligence.

⸻

💡 Solution

The user provides basic information about a proposed solar project.

User Inputs

Input Example Project Capacity 10 MW Capital Cost ₹45 crore Electricity Tariff ₹3.50/kWh Project Life 25 years Expected CUF 21% Annual O&M Cost ₹7 lakh/MW/year Required Return 10%

The user then clicks:

GIVE ME THE ANALYSIS

GreenVest automatically processes the project through multiple analytical layers.

⸻

🔄 How GreenVest AI Works

             USER INPUTS
                 │
                 ▼
      ┌─────────────────────┐
      │ Solar Project Data  │
      └──────────┬──────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Renewable Energy Models │
    └───────────┬─────────────┘
                │
   ┌────────────┼────────────┐
   ▼            ▼            ▼
 IEX           MNRE         NREL
Electricity Generation Degradation Market Data Analysis │ │ │ └────────────┼────────────┘ ▼ CERC Assumptions │ ▼ Financial Model │ ┌─────────┴─────────┐ ▼ ▼ Scenario Analysis Monte Carlo │ │ └─────────┬─────────┘ ▼ Risk Analysis │ ▼ RAG Evidence │ ▼ AI Assessment │ ▼ ┌──────────────────────────┐ │ INVEST │ │ INVEST WITH CAUTION │ │ NOT RECOMMENDED │ └──────────────────────────┘

⸻

🧮 Core Quantitative Model

GreenVest uses quantitative financial modelling to estimate the performance of the solar project.

Solar Generation
The project generation is estimated using:

Gross Generation = Capacity × Hours per Year × CUF

The model then accounts for auxiliary consumption and annual degradation.

The basic degradation model is:

Generationₜ = Generation₁ × (1 − degradation rate)^(t−1)

The GreenVest base model uses a 0.5% annual degradation assumption.

⸻

⚡ 2. Electricity Market Analysis — IEX

GreenVest incorporates electricity-market information from the Indian Energy Exchange (IEX).

The model analyses Market Clearing Price (MCP) data.

The IEX analysis includes:

Mean electricity price
Median electricity price
Standard deviation
Minimum price
Maximum price
₹10,000/MWh price-cap frequency
Price regimes
Regime transition probabilities
Monte Carlo market-price simulation
Price Regimes

The model divides electricity prices into:

Low Normal High Capped

This allows the model to understand not only the average electricity price but also how prices behave across different market conditions.

⸻

🔁 3. Markov Regime Analysis

GreenVest uses a Markov-style regime model to study how electricity prices move between different states.

For example:

Low → Low Low → Normal Normal → Low Normal → Normal Normal → High High → Normal High → High High → Capped Capped → High Capped → Capped

The transition matrix is used to represent the probability of moving from one market regime to another.

This helps GreenVest model price-state persistence and market uncertainty.

⸻

🎲 4. Monte Carlo Simulation

Because future electricity prices and project performance are uncertain, GreenVest uses Monte Carlo simulation.

Instead of calculating only one possible future, the model generates many possible outcomes.

The simulation introduces uncertainty into factors such as:

Electricity-market conditions
Generation
Operating costs
The resulting distribution is used to estimate:

Expected NPV
Median NPV
Probability of negative NPV
Investment uncertainty
A project may appear profitable under one set of assumptions but become unattractive when assumptions change.

Monte Carlo analysis helps answer What could happen if conditions are different from our base assumptions

⸻

💰 5. Financial Analysis

GreenVest generates a year-by-year financial model.

The model estimates:

Revenue

Revenue = Net Electricity Generation × Electricity Tariff

Operating Costs

Operating and maintenance costs are projected over the project life using an escalation assumption.

Cash Flow

The model estimates annual operating cash flows after relevant operating costs.

The resulting cash flows are used for project valuation.

⸻

📊 Key Financial Outputs

GreenVest calculates:

Net Present Value (NPV)
Internal Rate of Return (IRR)
Payback Period
Total Revenue
Total Costs
Annual Cash Flow
Cumulative Cash Flow
These metrics help determine whether the project appears financially attractive under the model assumptions.

⸻

📉 6. Scenario Analysis

GreenVest does not rely only on one forecast.

Three scenarios are evaluated:

🟢 Base Case

The project is evaluated using the user’s original assumptions.

🟡 Downside Case

The model assumes:

Tariff ↓ 10% CUF ↓ 5% Costs ↑ 10%

🔴 Stress Case

The model assumes:

Tariff ↓ 20% CUF ↓ 10% Costs ↑ 20%

This allows the user to understand how sensitive the investment is to adverse conditions.

⸻

📈 7. Sensitivity Analysis

GreenVest evaluates how changes in important project variables can affect financial performance.

Important variables include:

Electricity tariff
CUF
Capital cost
Operating cost
Market conditions
The purpose is to identify which assumptions have the greatest influence on project economics.

⸻

☀️ 8. MNRE Generation Analysis

The Ministry of New and Renewable Energy (MNRE) data is used to provide renewable-energy context.

GreenVest uses MNRE information to examine:

Solar installed capacity
Solar generation
Generation per MW
Historical generation trends
Implied capacity utilisation
This provides a broader view of India’s solar-energy environment and helps contextualise the project’s expected generation.

⸻

🏛️ 9. CERC Financial & Regulatory Context

GreenVest incorporates selected CERC-based assumptions into the financial model.

Examples include:

Debt-to-equity structure
Loan tenure
Interest assumptions
O&M escalation
Depreciation
Return on equity
Working-capital assumptions
Auxiliary consumption
Minimum CUF benchmark
Salvage value
These assumptions help make the financial model more realistic than using arbitrary values.

Important: CERC information is treated as regulatory/reference evidence. Regulatory parameters can change over time, so users should verify the latest applicable CERC regulations before making an actual investment decision.

⸻

☀️ 10. NREL Degradation Analysis

Solar panels gradually lose generation capability over time.

GreenVest therefore incorporates annual degradation into the generation model.

The NREL-based analysis provides context around different degradation assumptions, including:

Base modelling assumption
Typical degradation range
Modern technology range
Median degradation evidence
GreenVest currently uses:

Base degradation = 0.50% per year

This means that generation gradually decreases over the project’s lifetime.

⸻

🤖 11. AI Assessment

After completing the quantitative analysis, GreenVest produces an AI-assisted investment assessment.

The assessment considers:

NPV
IRR
Payback
Negative-NPV probability
Scenario performance
Electricity-market conditions
Generation assumptions
Degradation
Financial risks
The final recommendation falls into one of three categories:

🟢 INVEST

The project shows favourable financial characteristics under the model assumptions.

🟡 INVEST WITH CAUTION

The project may be viable, but meaningful risks or sensitivity to assumptions are present.

🔴 NOT RECOMMENDED

The project’s financial performance is weak under the analysed assumptions or shows substantial downside risk.

The recommendation is not based on a single metric.

⸻

📚 12. Retrieval-Augmented Generation (RAG)

GreenVest uses a Retrieval-Augmented Generation (RAG) approach to connect the analytical model with supporting evidence.

RAG workflow

Official Documents ↓ Text Extraction ↓ Document Chunking ↓ Embeddings / Retrieval ↓ Relevant Evidence ↓ AI Assessment

The RAG layer can retrieve supporting information from sources such as:

IEX
MNRE
CERC
NREL
Why RAG?

The financial model calculates the numerical results.

RAG provides the context and evidence behind important assumptions.

For example:

Financial Model: NPV = ₹X crore RAG: Relevant CERC / MNRE / NREL evidence supporting the assumptions used in the analysis.

Therefore:

RAG provides evidence; the financial model performs the calculations.

This separation helps reduce the risk of an AI system inventing financial numbers.

⸻

🧠 Role of AI

AI is not used simply to produce a generic chatbot response.

GreenVest uses AI-oriented workflows for:

Information Retrieval
Finding relevant renewable-energy and regulatory evidence.

Pattern Interpretation
Interpreting electricity-price and project-risk patterns.

Decision Support
Combining financial results and risk indicators into an understandable assessment.

Explanation
Converting technical financial results into language that a non-specialist user can understand.

⸻

🛠️ Technology Stack

Programming

Python
Application

Streamlit
Data Analysis

Pandas
NumPy
Visualisation

Matplotlib
Quantitative Modelling

Financial cash-flow modelling
NPV
IRR
Payback analysis
Scenario analysis
Monte Carlo simulation
Markov regime analysis
Sensitivity analysis
AI / Information Retrieval

Retrieval-Augmented Generation (RAG)
Document retrieval
AI-assisted explanation
⸻

🖥️ User Workflow

The user does not need to understand the underlying mathematics to use the prototype.

Step 1 — Enter project details

The investor enters:

Capacity Capital Cost Electricity Tariff Project Life CUF Annual O&M Cost Required Return

Step 2 — Click

GIVE ME THE ANALYSIS

Step 3 — GreenVest processes the project

The system performs:

Generation Calculation ↓ Revenue Calculation ↓ Cash Flow Modelling ↓ NPV / IRR / Payback ↓ IEX Market Analysis ↓ Scenario Analysis ↓ Monte Carlo Simulation ↓ Risk Analysis ↓ RAG Evidence ↓ AI Assessment

Step 4 — User receives the result

The application presents:

Overall assessment
Financial results
Generation analysis
IEX market analysis
Cash flows
Scenario analysis
Monte Carlo risk
Sensitivity analysis
NREL degradation analysis
CERC assumptions
AI investment assessment
Supporting evidence
⸻

📋 Example Output

A typical GreenVest analysis provides information such as:

Overall Assessment ↓ INVEST WITH CAUTION NPV IRR Payback Period Total Revenue Total Costs ↓ Generation Analysis ↓ IEX Market Analysis ↓ Scenario Analysis ↓ Monte Carlo Risk ↓ AI Explanation

The exact result depends on the project inputs and market assumptions.

⸻

🌱 Sustainability Impact

GreenVest aims to contribute to sustainable-energy adoption by improving the quality of information available during early-stage renewable-energy investment analysis.

Expected impact

The project can help:

Improve renewable-energy investment awareness
Encourage evidence-based solar-project evaluation
Highlight financial risks before investment
Make quantitative analysis easier to understand
Support clean-energy project development
Connect financial decision-making with sustainability objectives
The project does not directly build solar infrastructure. Instead, it addresses an important part of the renewable-energy ecosystem:

better-informed investment decisions can support the development and financing of renewable-energy projects.

⸻

⚖️ Responsible AI Considerations

Responsible AI is an important part of GreenVest.

Transparency
GreenVest displays the financial metrics and assumptions contributing to its assessment.

Users can see:

Inputs
Financial outputs
Scenario assumptions
Risk indicators
Supporting evidence
The system does not intentionally hide the basis of its recommendation.

⸻

Human Oversight
GreenVest is a decision-support system, not an autonomous investment adviser.

The final investment decision should remain with a qualified human decision-maker.

⸻

Avoiding Misleading Recommendations
The system does not guarantee that a project will be profitable.

Instead, recommendations are based on the modelled assumptions and available evidence.

For example:

“INVEST” does not mean the investment is guaranteed to succeed.

It means the project appears financially favourable under the assumptions tested.

⸻

Data Reliability
Market and renewable-energy data can change.

Therefore, GreenVest should use authoritative sources wherever possible, including:

IEX
MNRE
CERC
NREL
Data retrieval and source dates should be displayed where possible.

⸻

Privacy
GreenVest does not require sensitive personal information from the investor.

The project primarily uses:

Project characteristics
Financial assumptions
Energy-market data
Public renewable-energy information
⸻

Bias and Assumptions
Financial models can be affected by assumptions.

For example:

Electricity prices may behave differently in the future.
Actual solar generation may differ from expected CUF.
Capital costs may change.
O&M costs may increase.
Regulatory conditions may change.
Therefore, GreenVest uses scenario and Monte Carlo analysis rather than relying exclusively on a single forecast.

⸻

⚠️ Limitations

GreenVest is a prototype and should not be treated as a replacement for professional investment or engineering due diligence.

Important limitations include:

Electricity price uncertainty

Historical IEX behaviour does not guarantee future electricity prices.

Solar generation uncertainty

Actual generation can be affected by:

Weather
Irradiance
Location
Panel technology
System losses
Maintenance
Grid availability
Financial assumptions

Capital cost, O&M, financing and tariff assumptions may differ between projects.

Regulatory changes

CERC regulations and renewable-energy policies can change.

Model uncertainty

Monte Carlo simulation represents modelled uncertainty; it does not predict the future with certainty.

AI limitations

AI-generated explanations should be treated as decision-support information and verified against the underlying model and source documents.

⸻

🔬 Why Quantitative Modelling Matters

GreenVest combines sustainability with mathematical and financial analysis.

The project demonstrates applications of:

Probability
Statistics
Financial mathematics
Time-series thinking
Markov processes
Monte Carlo simulation
Discounted cash flow
NPV
IRR
Risk analysis
This makes GreenVest more than an awareness tool.

It is a quantitative decision-support prototype for renewable-energy investment.

⸻

🚀 Future Improvements

Future versions of GreenVest could include:

More detailed solar forecasting
Incorporate location-specific:

Solar irradiance
Weather
Temperature
Cloud cover
Advanced electricity-price modelling
Future versions could explore:

Stochastic differential equations
Mean-reversion models
Jump-diffusion models
GARCH models
More advanced Markov models
Geographic analysis
Allow users to select the location of a solar project and automatically incorporate regional generation and regulatory information.

Improved RAG
Expand the knowledge base with:

CERC regulations
MNRE reports
IEX market reports
NREL technical literature
Government renewable-energy policies
Interactive AI Assistant
A future version could allow users to ask:

“Why is this project risky?”

“What happens if electricity prices fall by 15%?”

“Which assumption affects my NPV the most?”

“Why did GreenVest recommend investing with caution?”

Portfolio Analysis
The system could eventually compare multiple renewable-energy projects and construct an investment portfolio.

⸻

🧪 Testing & Validation

The model can be tested using different project configurations.

Examples include:

Test Case 1 — High-performing project

Higher CUF + moderate capital cost + favourable tariff.

Test Case 2 — High-cost project

Higher capital cost + normal generation + moderate tariff.

Test Case 3 — Market stress

Lower electricity price + lower generation + higher operating costs.

Test Case 4 — Long-term degradation

Evaluate how annual degradation affects generation and project valuation over the full project life.

The purpose of testing is to determine whether the model behaves logically when assumptions change.

⸻

📊 Project Making Journey

The project follows the 1M1B AI for Sustainability project-development framework:

Problem Identification ↓ SDG Alignment ↓ AI Role & Ideation ↓ Design Thinking ↓ Prototype & Testing ↓ Impact & Evaluation ↓ Responsible AI & Ethics

Problem Identification

Renewable-energy projects involve high upfront costs and uncertain long-term returns.

SDG Alignment

The project is primarily aligned with SDG 7 — Affordable and Clean Energy.

AI Role & Ideation

AI and information-retrieval techniques are used to support analysis, evidence retrieval and explanation.

Design Thinking

The solution is designed around the needs of an investor who wants a clear understanding of a solar project’s financial feasibility and risk.

Prototype & Testing

A Streamlit prototype was developed using Python-based financial and risk models.

Impact & Evaluation

The project evaluates whether better quantitative information can improve renewable-energy investment decision-making.

Responsible AI & Ethics

The system emphasizes transparency, human oversight, evidence, privacy and uncertainty.

⸻

🎯 Project Objective

The overall objective of GreenVest AI is:

To develop an AI-assisted quantitative decision-support system that helps users evaluate the financial feasibility and risk of solar-energy investments while promoting informed and responsible renewable-energy decision-making.

⸻

👩‍💻 Project Information

Project: GreenVest AI Project Type: AI + Sustainability / Financial Decision Support Primary SDG: SDG 7 — Affordable and Clean Energy Domain: Renewable Energy + Financial Mathematics + AI Platform: Streamlit Language: Python Programme: 1M1B AI for Sustainability Virtual Internship In Collaboration With: IBM SkillsBuild & AICTE

⸻

📌 Key Takeaway

GreenVest AI demonstrates how AI, financial mathematics, renewable-energy data and responsible decision-support systems can be combined to address a real sustainability problem.

Rather than simply predicting whether an investment will succeed, GreenVest attempts to answer a more useful question:

“Given the project’s assumptions, market conditions and uncertainty, how financially attractive and risk-sensitive is this solar investment?”

The goal is not to replace human judgement.

The goal is to make that judgement better informed.

⸻

📚 Data & Evidence Sources

GreenVest is designed to use authoritative sources including:

Indian Energy Exchange (IEX) — electricity-market data
Ministry of New and Renewable Energy (MNRE) — renewable-energy statistics
Central Electricity Regulatory Commission (CERC) — regulatory and tariff information
National Renewable Energy Laboratory (NREL) — solar technology and degradation research
