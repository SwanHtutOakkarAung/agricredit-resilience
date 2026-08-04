# Data Understanding / Data Preparation

## Purpose of This Stage
After completing the Business Understanding stage, the next step is to understand what data is available and how it can be prepared for modeling. This follows the predictive data analytics workflow where the business problem is first translated into an analytics problem, and then the data is assessed to check whether the proposed solution is feasible.

The goal of this stage is to identify useful data sources, define possible target variables, select meaningful features, identify data limitations, and design the Analytics Base Table that will later be used for machine learning.

For this capstone project, the selected business problem is rural household financial vulnerability and responsible micro-finance/livelihood decision support. The system is not designed to automatically approve or reject loans. Instead, it is designed to support decision-makers by estimating household vulnerability, explaining the reasons behind the prediction, and recommending responsible support options.

## Data Understanding Overview
The uploaded documents show that the project can be supported by several types of data:

1. Household welfare and demographic data
2. Microfinance and debt-related data
3. Agriculture and farm production data
4. Food security and coping strategy data
5. Market price and market access data
6. Cash assistance and Minimum Expenditure Basket data
7. Humanitarian response and assistance coverage data
8. Climate, conflict, disaster, and shock exposure data

These sources do not all exist at the same level of detail. Some are household-level, some are township-level, some are state/region-level, and some are national or program-level. Therefore, the final dataset will likely combine household-level records with contextual location-level indicators.

## Main Data Sources Identified

### Household Welfare and Living Conditions Data
The Myanmar Living Conditions Survey and related household welfare sources are useful for understanding household-level characteristics such as household size, income, employment, rural/urban status, housing conditions, asset ownership, access to services, and welfare indicators.

For this project, this type of data can support the base household profile of each record in the dataset. Each row in the final Analytics Base Table should represent one household, preferably a rural farming household.

Possible variables from this source group include:
* household size
* number of children
* number of elderly members
* dependency ratio
* household head gender
* household head age
* household head education
* rural or urban location
* main income source
* employment status
* housing quality
* water access
* sanitation access
* electricity access
* mobile or internet access
* asset ownership

These variables help describe the household’s social and economic capacity.

### Microfinance and Financial Inclusion Data
The micro-finance impact assessment materials support the financial inclusion side of the project. They show that borrowing is common among households, but access to low-interest formal financial services is limited. This supports the need to include debt, loan source, repayment capacity, and access to finance indicators.

Possible variables include:
* has current loan
* loan source
* formal loan access
* informal borrowing
* low-interest loan access
* total current debt
* monthly repayment amount
* loan purpose
* loan amount
* previous repayment difficulty
* access to credit
* savings availability
* weeks of cash savings

These variables are important because a household may appear to have income but still be financially stressed if it has high debt or high repayment obligations.

### Agriculture and Farm Production Data
The farm production economics and rice productivity documents are important for designing farmer-specific features. They provide guidance on land, labor, farm assets, crop choices, input costs, yields, profitability, irrigation, mechanization, and agricultural loans.

Possible variables include:
* farm size
* main crop
* rice farmer indicator
* crop diversification
* irrigation access
* seed type
* fertilizer use
* fertilizer cost
* agrochemical cost
* mechanization access
* machinery ownership
* draught animal ownership
* yield per acre
* production cost per acre
* crop revenue
* farm profit margin
* market distance
* farm-gate price
* agricultural loan source
* agricultural loan amount

These variables are useful because repayment ability is connected to agricultural productivity, input costs, crop prices, and farm income stability.

### Food Security and Coping Strategy Data
Food security documents and cash monitoring guidance provide useful indicators for vulnerability. The most important indicator from the PDM guidance is the Reduced Coping Strategies Index, or rCSI. It measures how often households use coping strategies when they lack food or money to buy food.

The rCSI uses five strategies:
1. Relying on less preferred or less expensive food
2. Borrowing food or relying on help from friends or relatives
3. Reducing the number of meals eaten per day
4. Reducing meal portion size
5. Reducing adult consumption so children can eat

Each strategy has a severity weight. The final rCSI score is calculated by multiplying frequency by severity weight and summing the result.

Possible variables include:
* rCSI score
* reduced meals
* reduced portion size
* borrowed food
* relied on cheaper food
* adults reduced consumption for children
* food consumption score
* household hunger score
* ability to meet basic food needs
* skipped meals
* food expenditure share
* essential food needs covered

These variables may be used either as input features or as proxy target variables.

### Market Price and Market Access Data
The WFP market price updates, Market Stoplight Tool, Joint Market Monitoring references, and CASS market findings support the market pressure part of the project. These documents show that food prices, fuel prices, transport restrictions, conflict, and market access problems can affect household vulnerability.

Possible variables include:
* basic food basket price
* basic food basket price change
* rice price change
* palm oil price change
* chickpea price change
* salt price change
* fuel price change
* market access
* market travel cost
* market travel time
* goods availability
* goods affordability
* rice availability
* cooking oil availability
* medicine availability
* fuel affordability
* market functionality level
* road closure flag
* transport restriction flag
* market disruption flag

These variables are important because cash assistance or micro-finance may not be effective if markets are not accessible or goods are unavailable.

### Minimum Expenditure Basket and Cash Assistance Data
The MEB and cash assistance documents are central to feature engineering. The Minimum Expenditure Basket gives an estimate of the monthly cost required to meet essential needs. This allows us to create stronger financial pressure indicators than income alone.

Possible variables include:
* household monthly income
* state or region MEB value
* household size
* MEB per person
* household MEB requirement
* income-to-MEB ratio
* MEB gap
* MPCA value
* Cash for Food Assistance value
* transfer gap
* essential needs coverage

Important derived features include:
* `household_meb_requirement = state_meb_per_person * household_size`
* `meb_gap = household_meb_requirement - monthly_income`
* `income_to_meb_ratio = monthly_income / household_meb_requirement`
* `basic_needs_unmet = 1 if monthly_income < household_meb_requirement else 0`

These features are highly useful because they estimate whether the household can meet basic needs.

### Humanitarian Response and Assistance Coverage Data
Food Security Cluster dashboards and response monitoring data can provide contextual indicators about whether a location is being reached by food assistance, agriculture support, livelihood support, cash assistance, or other interventions.

Possible variables include:
* people in need
* people targeted
* people reached
* response gap
* coverage rate
* township reached flag
* targeted but unreached flag
* assistance type
* food assistance coverage
* agriculture input support coverage
* cash assistance coverage
* number of partners active
* delivery modality

These variables can be attached at township or state/region level.

### Shock, Conflict, Climate, and Disaster Data
Several documents show that rural households and farmers are affected by conflict, transport restrictions, floods, droughts, earthquakes, market disruption, and climate-related shocks.

Possible variables include:
* drought exposure
* flood exposure
* cyclone exposure
* earthquake affected area
* conflict affected area
* road access disruption
* displacement status
* crop damage
* livestock loss
* irrigation damage
* market damage
* income source loss
* shock count

These variables help explain why a household may be vulnerable even if it had normal income before.

## Data Level and Integration Plan
The project data sources exist at different levels:

| Data Source Type | Level | How It Can Be Used |
| :--- | :--- | :--- |
| Household survey data | Household | Main row-level data |
| Microfinance/debt data | Household | Financial stress and repayment features |
| PDM/cash monitoring data | Household | Basic needs, debt, rCSI, market access |
| Agriculture survey data | Household/farm | Farm production and crop risk features |
| Market price data | Township/state/month | Location-level market pressure |
| MEB/CFA/MPCA data | State/region | Essential cost benchmark |
| FSC response data | Township/state | Assistance coverage and response gap |
| Climate/conflict/disaster data | Township/state | Shock exposure features |

The final dataset will most likely use household-level rows and attach contextual data by location and time.

Example:
* Household lives in Sagaing
* Attach Sagaing MEB value
* Attach Sagaing rice price change
* Attach Sagaing food basket change
* Attach Sagaing response coverage
* Attach Sagaing shock/disaster flag

This creates one complete row for modeling.

## Proposed Prediction Target
After reviewing the documents, the most feasible main target is:

### Main Target: Household Financial Vulnerability
This is better than pure loan default prediction because real micro-finance repayment/default data may be difficult to obtain. Household financial vulnerability can be created from available or simulated indicators such as MEB gap, debt burden, basic needs coverage, rCSI, and market access.

Possible target variable:
`financial_vulnerability`

Possible classes:
* Low vulnerability
* Medium vulnerability
* High vulnerability

For machine learning, this can be simplified into binary classification:
* `0 = not highly vulnerable`
* `1 = highly vulnerable`

### Possible Rule for Creating the Target
A household can be labeled as high vulnerability if it meets two or more of the following conditions:

1. Income is below household MEB requirement
2. Debt repayment burden is above a chosen threshold
3. rCSI score is high
4. Household reports inability to meet basic needs
5. Household cannot access nearby market
6. Household reports essential food items as unaffordable
7. Household experienced recent livelihood shock

Example target rule:
```text
high_vulnerability = 1 if
  meb_gap > 0 and (
    rCSI_score >= threshold or
    debt_to_income_ratio >= threshold or
    market_access == no
  )
```

This is a proxy target, so the project must clearly explain that it is a capstone modeling target created from vulnerability indicators, not a real observed loan default label.

## Secondary Output: Responsible Loan/Support Recommendation
The second output should not be a separate ML target at first. Instead, it can be a rule-based recommendation generated from the model result and market indicators.

Example recommendation logic:

| Vulnerability Risk | Market Functionality | Suggested Action |
| :--- | :--- | :--- |
| Low | Green | Normal loan may be considered |
| Medium | Green | Smaller loan or flexible repayment |
| High | Green | Refer to cash/livelihood support before loan |
| High | Yellow | Manual review and market monitoring |
| High | Red | Avoid new debt; prioritize emergency support |
| Medium | Red | In-kind or direct support preferred |

This makes the system more ethical and realistic because it avoids using the model as an automatic loan rejection tool.

## Candidate Features for the Analytics Base Table

### Household Profile Features
* `household_id`
* `state_region`
* `township`
* `rural_urban`
* `household_size`
* `children_count`
* `elderly_count`
* `dependency_ratio`
* `female_headed_household`
* `disability_present`
* `displacement_status`

### Financial Features
* `monthly_income`
* `income_source_count`
* `has_debt`
* `total_debt`
* `monthly_debt_repayment`
* `debt_to_income_ratio`
* `savings_duration_weeks`
* `has_formal_loan`
* `has_informal_loan`
* `loan_amount`
* `loan_purpose`
* `previous_repayment_difficulty`

### Agriculture Features
* `is_farming_household`
* `farm_size_acres`
* `main_crop`
* `crop_diversification_count`
* `rice_farmer`
* `irrigation_access`
* `fertilizer_use`
* `fertilizer_cost`
* `seed_type`
* `mechanization_access`
* `yield_per_acre`
* `production_cost_per_acre`
* `farm_profit_margin`
* `crop_damage_recent`
* `livestock_owned`
* `productive_assets_owned`

### Food Security and Coping Features
* `rCSI_score`
* `relied_on_less_preferred_food_days`
* `borrowed_food_days`
* `reduced_meals_days`
* `reduced_portion_days`
* `adults_reduced_for_children_days`
* `skipped_meals`
* `food_consumption_status`
* `household_hunger_status`

### Market Features
* `market_access`
* `market_travel_time`
* `market_travel_cost`
* `rice_available`
* `cooking_oil_available`
* `medicine_available`
* `fuel_available`
* `rice_affordable`
* `cooking_oil_affordable`
* `medicine_affordable`
* `fuel_affordable`
* `basic_food_basket_price`
* `basic_food_basket_change_1m`
* `basic_food_basket_change_1y`
* `fuel_price_change_1y`
* `market_functionality_status`

### MEB and Basic Needs Features
* `state_meb_value`
* `household_meb_requirement`
* `meb_gap`
* `income_to_meb_ratio`
* `basic_needs_met`
* `essential_food_needs_covered`
* `health_needs_covered`
* `wash_needs_covered`
* `shelter_needs_covered`

### Assistance Coverage Features
* `food_assistance_received`
* `cash_assistance_received`
* `agriculture_input_support_received`
* `livelihood_support_received`
* `township_food_assistance_coverage`
* `township_response_gap`
* `targeted_but_unreached_area`
* `number_of_partners_active`

### Shock and Context Features
* `conflict_affected_area`
* `drought_exposure`
* `flood_exposure`
* `earthquake_affected_area`
* `road_closure_flag`
* `transport_restriction_flag`
* `market_damage_flag`
* `recent_income_loss`
* `shock_count`

## Proposed Analytics Base Table
Each row should represent one rural or agriculture-linked household.

| Column Group | Example Columns | Purpose |
| :--- | :--- | :--- |
| Household identity | household_id, state_region, township | Identification and merge keys |
| Household profile | household_size, dependency_ratio, disability_present | Social vulnerability |
| Financial status | income, debt, repayment, savings | Financial stress |
| Agriculture | farm_size, crop, irrigation, input cost, yield | Farm livelihood risk |
| Food security | rCSI_score, skipped_meals, food consumption | Food vulnerability |
| Market | market_access, price changes, affordability | Market pressure |
| MEB/basic needs | meb_gap, income_to_meb_ratio, basic_needs_met | Essential needs pressure |
| Assistance coverage | support received, response gap | Contextual support |
| Shock exposure | conflict, flood, drought, earthquake | External risk |
| Target | financial_vulnerability | ML label |

## Data Preparation Plan

### Data Cleaning
The first cleaning step is to standardize column names, remove duplicate records, check data types, and ensure that location names are consistent.

Examples:
* Convert all state/region names to one format
* Standardize township names
* Convert numeric columns to numbers
* Convert Yes/No values to binary
* Remove or flag impossible values such as negative household size
* Check whether income, debt, and expenditure values are monthly or yearly

### Handling Missing Values
Missing values should be handled differently depending on the column type.

For numerical columns:
* Use median imputation for income, debt, and cost variables if missingness is moderate
* Use zero only when zero truly means absence, such as no debt
* Create missing indicator columns when missingness itself may be meaningful

For categorical columns:
* Use “Unknown” for missing categories
* Avoid deleting many rows unless the target variable is missing

Examples:
* If `total_debt` is missing but `has_debt = no`, set `total_debt = 0`
* If `market_access` is missing, set `market_access = unknown`
* If `income` is missing, impute median income by state/region if possible

### Encoding Categorical Variables
Decision Trees can handle encoded categories, but Logistic Regression requires numerical encoding.

Suggested encoding:
* Binary encoding for Yes/No features
* One-hot encoding for nominal categories such as crop type or state/region
* Ordinal encoding for ordered categories such as low, medium, high

Examples:
* `market_access`: yes = 1, no = 0
* `main_crop`: rice, pulses, maize, oilseed, mixed → one-hot encoding
* `vulnerability_level`: low = 0, medium = 1, high = 2

### Feature Scaling
Decision Trees do not require feature scaling. Logistic Regression usually benefits from scaling numerical features.

Features to scale:
* monthly income
* total debt
* loan amount
* farm size
* market travel cost
* production cost
* MEB gap
* rCSI score

Suggested method:
* Use StandardScaler or MinMaxScaler for Logistic Regression
* Keep unscaled version for Decision Tree if needed for interpretability

### Derived Feature Engineering
Derived features are important because raw variables may not directly show vulnerability.

Important derived features:

#### MEB Gap
`meb_gap = household_meb_requirement - monthly_income`

Meaning:
* Positive value = household income is below essential needs
* Negative value = household income is above essential needs

#### Income-to-MEB Ratio
`income_to_meb_ratio = monthly_income / household_meb_requirement`

Meaning:
* Below 1 = income is insufficient
* Above 1 = income may cover essential needs

#### Debt-to-Income Ratio
`debt_to_income_ratio = monthly_debt_repayment / monthly_income`

Meaning:
* Higher value = heavier repayment burden

#### Loan-to-Income Ratio
`loan_to_income_ratio = loan_amount / monthly_income`

Meaning:
* Higher value = larger loan pressure relative to income

#### Food Price Pressure
`food_price_pressure = basic_food_basket_change_1y`

Meaning:
* Higher value = stronger food affordability pressure

#### Shock Count
`shock_count = drought + flood + conflict + earthquake + market_disruption + income_loss`

Meaning:
* Higher value = more overlapping shocks

#### rCSI Score
`rCSI = less_preferred_food_days*1 + borrowed_food_days*2 + reduced_meals_days*1 + reduced_portion_days*1 + adults_reduced_for_children_days*3`

Meaning:
* Higher score = more severe food insecurity coping

### Target Variable Construction
If the final dataset does not contain a direct vulnerability label, a proxy target can be created.

Example binary target:
`financial_vulnerability = 1 if household is high risk, else 0`

Suggested rule:
A household is high vulnerability if at least two of the following are true:
* `income_to_meb_ratio < 1`
* `debt_to_income_ratio > 0.30`
* `rCSI_score >= 19`
* `basic_needs_met = no`
* `market_access = no`
* `shock_count >= 2`

This threshold can be adjusted after exploratory data analysis.

### Train/Test Split
The dataset should be split into training and testing sets.

Suggested split:
* 80% training
* 20% testing

Use stratified sampling if the target variable is imbalanced.

Reason:
If high-vulnerability households are rare or very common, random splitting may produce an unfair test set. Stratification keeps the same class ratio in both train and test data.

### Class Imbalance Check
Financial vulnerability data may be imbalanced. For example, if most households are vulnerable, a model may achieve high accuracy by predicting “high vulnerability” for everyone.

Check:
* percentage of low-risk households
* percentage of high-risk households
* confusion matrix
* precision
* recall
* F1-score
* ROC-AUC

Possible handling methods:
* class weights
* threshold tuning
* resampling
* evaluation beyond accuracy

### Data Leakage Prevention
Data leakage happens when the model uses information that would not be available at prediction time.

Avoid using columns such as:
* final assistance decision
* post-model recommendation
* future outcome after receiving assistance
* variables directly created from the target if not properly separated

Example:
If the target is created from `rCSI_score`, then using `rCSI_score` as an input feature may cause leakage. In that case, either use rCSI as the target basis or as a feature, but be clear about the modeling design.

## Modeling Connection to the Textbook

### Decision Tree
Decision Tree is suitable because it provides explainable rules. For this project, it can show why a household is classified as high vulnerability.

Example rule:
High vulnerability if:
* income-to-MEB ratio is below 1
* debt-to-income ratio is high
* market access is unavailable
* rCSI score is high

This is useful for loan officers, NGO staff, and livelihood-support workers because the prediction can be explained in human language.

### Logistic Regression
Logistic Regression is useful because it gives a probability score.

Example:
* 0.78 probability of high financial vulnerability

This allows the dashboard to show risk levels:
* 0.00–0.39 = low risk
* 0.40–0.69 = medium risk
* 0.70–1.00 = high risk

The threshold can be adjusted depending on the organization’s purpose.

### Evaluation
The project should not rely only on accuracy.

Important evaluation metrics:
* confusion matrix
* precision
* recall
* F1-score
* ROC curve
* AUC
* threshold comparison

In this project, the cost of mistakes matters.

**False positive:**
* The model says household is high risk, but it is not.
* Possible harm: unfairly denying a loan or support opportunity.

**False negative:**
* The model says household is low risk, but it is actually highly vulnerable.
* Possible harm: giving an unsuitable loan or failing to refer support.

For a humanitarian and responsible finance project, recall for high-vulnerability households may be especially important because missing vulnerable households can cause serious harm.

## Dashboard Data Outputs
The final dashboard should show:

### Household Risk Prediction Page
Inputs:
* income
* debt
* household size
* crop type
* market access
* MEB location
* shock exposure
* coping behavior

Outputs:
* financial vulnerability probability
* low/medium/high risk category
* main risk reasons
* suggested action

### Model Explanation Page
Show:
* decision tree rules
* feature importance
* top factors for individual prediction

### Market Feasibility Page
Show:
* market access
* food availability
* food affordability
* market functionality status
* cash/in-kind recommendation

### Evaluation Page
Show:
* confusion matrix
* precision
* recall
* F1-score
* ROC curve
* AUC
* threshold comparison

### SDG Impact Page
Show alignment with:
* SDG 1: No Poverty
* SDG 2: Zero Hunger
* SDG 8: Decent Work and Economic Growth
* SDG 13: Climate Action

## Data Quality Issues and Limitations

### Different Data Levels
Some data is household-level, while other data is township-level or state-level. This means location-level indicators may not perfectly describe each household.

### Time Mismatch
Some sources are from 2016–2017, others from 2021, 2024, 2025, or 2026. This creates a time mismatch. The project should clearly explain that older sources are used for structural indicators, while newer sources are used for current shock and market context.

### Proxy Target Limitation
If real micro-finance default data is unavailable, the project will use financial vulnerability as a proxy target. This is acceptable for a capstone prototype, but it must be clearly stated.

### Data Availability
Some dashboards may contain useful information but may not provide downloadable raw data. If raw data cannot be accessed, those dashboards should be used for context and documentation, not direct model training.

### Ethical Considerations
The model should not automatically reject households from loans or assistance. It should support human decision-making. Sensitive variables such as ethnicity, religion, or disability should be handled carefully and should not be used to discriminate.

## Final Recommended Modeling Dataset
The best final dataset for this project should be a household-level dataset with the following structure:

| Column | Example |
| :--- | :--- |
| household_id | HH001 |
| state_region | Sagaing |
| township | Monywa |
| household_size | 5 |
| monthly_income | 350000 |
| total_debt | 800000 |
| monthly_debt_repayment | 90000 |
| farm_size_acres | 3 |
| main_crop | rice |
| rCSI_score | 22 |
| market_access | no |
| rice_affordable | no |
| fuel_affordable | no |
| state_meb_value | 55000 per person |
| household_meb_requirement | 275000 |
| meb_gap | -75000 |
| township_response_gap | high |
| shock_count | 3 |
| financial_vulnerability | 1 |

This dataset can be used to train:
1. Decision Tree Classifier
2. Logistic Regression Classifier
3. Optional Random Forest for comparison

## Final Data Understanding and Preparation Statement
The uploaded documents show that the AgriCredit Resilience project is data-feasible as a capstone prototype if the main target is framed as household financial vulnerability rather than direct loan default. The available documents provide strong support for designing features related to household income, debt, MEB gap, food security coping strategies, agriculture production, market access, food price pressure, shock exposure, and humanitarian response coverage.

The final Analytics Base Table should use one household per row and combine household-level indicators with location-level contextual data. The most important derived features are MEB gap, income-to-MEB ratio, debt-to-income ratio, rCSI score, food price pressure, market access status, and shock count.

The prepared dataset will support explainable classification models, especially Decision Trees and Logistic Regression. The Decision Tree will provide transparent rules, while Logistic Regression will provide probability-based vulnerability scores. Evaluation should focus on confusion matrix, precision, recall, F1-score, ROC curve, and AUC rather than accuracy alone.

This approach creates a realistic, ethical, and SDG-aligned machine learning project that connects rural finance, food security, agriculture, cash assistance, and household resilience in Myanmar.

## Supporting Evidences/References
* Guidelines Microfinance Impact Assessment Designs LIFT Aug13
* Report Human Resource Development Indicators 2018
* Assesst Farm Production Economics WB_Feb2016
* Assessment Rice Productivity in Myanmar IFPRI May2022
* Research Monitoring the Agri food System in Myanmar Rising Costs
* mmr humanitarian response plan 2023 final 0
* note fsc workshop june 2022 final
* FSC Myanmar Gap Analysis and Response Snapshot January_to_March
* Area_Monitoring Market Findings CASS Q4 2024
* Cash Assistance Post Distribution Monitoring Guidance ENG Nov2025
