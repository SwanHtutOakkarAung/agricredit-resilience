# Business Understanding

## Project Title
**AgriCredit Resilience:** Explainable Financial Vulnerability and Loan Risk Predictor for Rural Farmers in Myanmar.

## Project Background
Myanmar is facing a severe combination of economic, social, political, climate, and humanitarian challenges. Rural households and smallholder farmers are especially vulnerable because their income depends heavily on agriculture, seasonal labor, local markets, weather conditions, and access to affordable financial services.

Many poor and low-income households in Myanmar still have limited access to formal financial services such as savings, loans, insurance, and safe money transfer systems. Because of this, households often rely on informal borrowing, family support, moneylenders, or short-term coping strategies when they face income shocks. For farmers, these financial risks become more serious when crop production is affected by conflict, climate events, market disruption, price inflation, natural disasters, or loss of agricultural inputs.

Traditional micro-finance can help rural households access capital, but lending decisions can become risky when lenders do not have enough information about borrowers’ repayment capacity. At the same time, rejecting vulnerable farmers without understanding their situation can worsen poverty and financial exclusion.

This capstone project proposes an explainable machine learning system that supports safer and more socially responsible rural finance decisions. Instead of simply predicting whether a farmer should be approved or rejected for a loan, the system predicts both household financial vulnerability and possible loan repayment risk. The goal is to help loan officers, NGOs, or livelihood-support organizations identify vulnerable farmers, understand the reasons behind risk, and recommend suitable support such as safer loan terms, cash assistance referral, livelihood support, or further assessment.

## Business Problem
The main business problem is:

> **Rural farmers and agricultural households in Myanmar face high financial vulnerability, but micro-finance providers and support organizations may lack a clear, data-informed, and explainable way to assess repayment risk and household support needs.**

This creates two related problems.

First, financial institutions or micro-finance providers may approve loans for households that are already under severe financial pressure. If the household’s income is unstable, crop production is disrupted, or essential expenses are higher than income, the loan may increase debt stress and lead to repayment failure.

Second, lenders may reject farmers who appear risky but could repay successfully if they receive suitable support, adjusted loan terms, or complementary assistance. This can reduce financial inclusion and limit farmers’ ability to recover from shocks.

Therefore, the project focuses on building a decision-support tool, not an automatic loan rejection system.

## Business Objectives
The business objectives of this project are:

1. To help decision-makers estimate the financial vulnerability level of rural farming households.
2. To predict the likelihood of loan repayment difficulty or default risk using household, agriculture, market, and shock-related indicators.
3. To provide explainable reasons behind each prediction so that users can understand why a household is considered high, medium, or low risk.
4. To support fairer and more responsible micro-finance decisions by recommending possible actions instead of only approving or rejecting loans.
5. To align the project with SDG-related goals, especially poverty reduction, food security, decent work, economic resilience, and climate adaptation.

## Target Users
The possible target users are:

* Microfinance loan officers
* NGO livelihood program officers
* Rural development organizations
* Humanitarian cash assistance teams
* Agricultural support programs
* Policy or research teams working on rural financial inclusion

For this capstone project, the assumed primary user is a **micro-finance or livelihood-support officer** who needs to assess rural households before giving a loan or recommending assistance.

## Candidate Analytic Solutions

### Candidate Solution 1: Loan Default Risk Prediction
This solution predicts whether a farmer is likely to default on a micro-loan.

The model would use features such as household income, existing debt, loan amount, previous repayment history, crop type, farm size, market access, crop shock, and climate or conflict exposure.

The output would be:
* Low repayment risk
* Medium repayment risk
* High repayment risk

Possible models:
* Decision Tree
* Logistic Regression
* Random Forest as an optional extension

**How the business would use it:**
A loan officer could use the model before approving a loan. If the model predicts high risk, the officer could review the case more carefully, reduce loan size, extend repayment duration, request additional support information, or refer the household to assistance before lending.

**Strength:**
This solution is directly related to micro-finance and credit scoring. It is easy to explain to internship reviewers because it connects machine learning with a real financial decision.

**Weakness:**
If used alone, it may sound too focused on protecting lenders rather than supporting vulnerable farmers. It may also require real loan repayment data, which may be difficult to obtain for a capstone project.

---

### Candidate Solution 2: Household Financial Vulnerability Prediction
This solution predicts whether a rural household is financially vulnerable based on its income, expenses, food security, coping strategies, and exposure to shocks.

The model would use features such as monthly income, household size, food expenditure, Minimum Expenditure Basket gap, debt level, skipped meals, selling assets, loss of income, crop damage, displacement, disaster exposure, and access to markets.

The output would be:
* Low vulnerability
* Medium vulnerability
* High vulnerability

Possible models:
* Decision Tree
* Logistic Regression
* Naive Bayes as an optional comparison

**How the business would use it:**
An NGO, micro-finance provider, or support organization could use the model to identify households that need extra support before taking on new debt. A high-vulnerability household may need cash assistance, agricultural input support, or livelihood recovery support rather than a normal loan.

**Strength:**
This solution is strongly aligned with SDG goals and humanitarian-development logic. It is also more ethical because it focuses on household well-being, not only lender risk.

**Weakness:**
The target variable may need to be created from proxy indicators, such as coping strategies, MEB gap, food insecurity, or self-reported inability to meet basic needs.

---

### Candidate Solution 3: Food Security Risk Prediction
This solution predicts whether a household is likely to experience food insecurity.

The model would use features such as food expenditure, crop production difficulty, market price changes, household income, displacement, household size, food consumption score, coping strategies, and disaster exposure.

The output would be:
* Food secure
* At risk
* Food insecure

Possible models:
* Decision Tree
* Logistic Regression
* k-Nearest Neighbors as an optional comparison

**How the business would use it:**
A humanitarian or food security organization could use the model to prioritize households for food assistance, cash assistance, or nutrition support.

**Strength:**
This solution has strong SDG 2 alignment and many uploaded documents support the food security problem.

**Weakness:**
It moves away from the micro-finance internship showcase angle. It may look more like a humanitarian targeting project than a FinTech or enterprise AI project.

---

### Candidate Solution 4: Agricultural Shock and Livelihood Risk Prediction
This solution predicts whether a farmer’s livelihood is at risk because of agriculture-related shocks.

The model would use features such as crop type, farm size, irrigation access, machinery ownership, access to extension services, weather shock, conflict exposure, market disruption, input price increases, and expected harvest reduction.

The output would be:
* Low livelihood risk
* Medium livelihood risk
* High livelihood risk

Possible models:
* Decision Tree
* Logistic Regression
* Random Forest as an optional extension

**How the business would use it:**
Agricultural support organizations could identify farmers who need input support, cash-for-work, extension services, or flexible loan repayment plans.

**Strength:**
This solution has strong agriculture and climate alignment.

**Weakness:**
It may not directly showcase micro-finance decision-making unless combined with repayment risk.

## Evaluation of Candidate Solutions
The candidate solutions are evaluated using two practical criteria:

1. **Data requirement feasibility:** Can the needed data be realistically collected, simulated, or approximated for a capstone project?
2. **Business capacity to use the model:** Can the assumed organization realistically understand and use the model output in decision-making?

### Candidate Solution 1: Loan Default Risk Prediction
* **Data feasibility:** Medium
  This solution requires repayment/default data, which may not be available publicly for Myanmar rural farmers. A synthetic or proxy target may be needed.
* **Business usability:** High
  Microfinance providers can easily understand loan risk categories and probability scores.
* **Overall feasibility:** Medium to High
  This is useful, but it should not be the only solution because default prediction alone may be too narrow.

### Candidate Solution 2: Household Financial Vulnerability Prediction
* **Data feasibility:** High
  The required features can be designed from household income, expenditure, MEB gap, coping strategies, food security indicators, and shock exposure. These are more realistic to approximate from public humanitarian and development sources.
* **Business usability:** High
  NGOs, micro-finance providers, and livelihood teams can use vulnerability levels to decide whether a household needs a loan, grant, cash assistance, or additional support.
* **Overall feasibility:** Very High
  This is the most practical and socially responsible core solution.

### Candidate Solution 3: Food Security Risk Prediction
* **Data feasibility:** Medium to High
  Food security indicators are commonly used in humanitarian assessments, but detailed household-level data may not be available.
* **Business usability:** Medium
  Humanitarian organizations can use it, but micro-finance providers may not use it as their main decision tool.
* **Overall feasibility:** Medium
  Useful as a supporting feature or dashboard section, but not ideal as the main project.

### Candidate Solution 4: Agricultural Shock and Livelihood Risk Prediction
* **Data feasibility:** Medium
  Some agriculture and shock indicators can be approximated, but detailed farm-level production data may be difficult to access.
* **Business usability:** Medium to High
  Agricultural NGOs and livelihood teams could use it, but it may need to be connected to financial vulnerability or loan risk to fit the internship showcase.
* **Overall feasibility:** Medium to High
  Useful as a supporting component in the final solution.

## Selected Practical Solution
The selected solution is a combined model:

**Explainable Financial Vulnerability and Loan Risk Predictor for Rural Farmers in Myanmar**

The system will produce two main outputs:

1. **Household Financial Vulnerability Risk**
   * Predicts whether a farming household is under financial stress.
   * Uses features such as income, household size, MEB gap, food cost pressure, coping strategies, disaster shock, conflict exposure, and agriculture disruption.

2. **Loan Repayment Risk**
   * Predicts whether the household may struggle to repay a new micro-loan.
   * Uses features such as loan amount, existing debt, income stability, crop risk, previous repayment behavior, financial gap, and productive asset ownership.

This selected solution is more practical than a pure default prediction model because it does not require the project to depend only on real micro-finance default data. It is also more socially responsible because it considers whether lending may help or harm the household.

## How the Model Solves the Business Problem
The model helps decision-makers in four ways.

* **First**, it summarizes complex household and farming conditions into understandable risk categories. This helps users quickly identify households that need closer review.
* **Second**, it provides probability scores instead of only yes/no decisions. This allows organizations to choose their own risk threshold depending on their mission. For example, a commercial lender may use a stricter threshold, while an NGO-linked micro-finance program may allow more flexibility if support services are available.
* **Third**, it explains the main reasons behind the prediction. For example, the system may show that a household is high risk because its monthly income is below the MEB, it has existing debt, it recently sold productive assets, and its crop area was reduced after a shock.
* **Fourth**, it recommends responsible actions. Instead of simply saying “reject,” the system can suggest:
  * approve normal loan
  * approve smaller loan
  * offer flexible repayment
  * refer to cash assistance
  * refer to agricultural input support
  * require manual review
  * delay loan until income stabilizes

## Capstone Assumptions
Because this is a capstone project and not a real deployed business system, the following assumptions are made:

1. The project assumes the role of a micro-finance or livelihood-support organization working with rural farming households in Myanmar.
2. The project assumes that household-level data can be collected through surveys, partner records, or simulated based on public reports.
3. The project assumes that the model is used as decision support, not as an automatic final decision-maker.
4. The project assumes that the organization has basic capacity to use a web dashboard and interpret simple risk explanations.
5. The project assumes that some target variables may need to be created from proxy indicators, such as high financial gap, use of severe coping strategies, or repayment difficulty.
6. The project will clearly label synthetic or simulated data if real household-level data is not available.

## Model Success Goals
The model success goals are:

1. The financial vulnerability model should correctly identify most high-vulnerability households.
2. The loan repayment risk model should perform better than a simple baseline model.
3. The model should not rely only on accuracy, because the dataset may be imbalanced.
4. The evaluation should include confusion matrix, precision, recall, F1-score, ROC curve, and AUC.
5. The model should provide explainable outputs using decision tree rules, feature importance, or clear reason codes.
6. The model should allow threshold adjustment so users can understand the trade-off between false positives and false negatives.

## Business Impact Goals
The expected business and social impact goals are:

1. Help micro-finance or livelihood officers make more informed lending decisions.
2. Reduce the risk of giving unsuitable loans to households already under severe financial stress.
3. Reduce unfair rejection by explaining whether risk comes from temporary shock, structural poverty, or repayment history.
4. Support financial inclusion by recommending alternative support instead of simple rejection.
5. Help organizations prioritize vulnerable farming households for cash, agricultural, or livelihood assistance.
6. Contribute to SDG 1, SDG 2, SDG 8, and SDG 13 by supporting poverty reduction, food security, decent work, economic resilience, and climate-aware rural finance.

## Dashboard/Product Success Goals
The product success goals are:

1. Build a simple web dashboard where a user can input household and farm information.
2. Display financial vulnerability risk and loan repayment risk clearly.
3. Show the main factors that influenced the prediction.
4. Include a model evaluation page with confusion matrix, ROC curve, and key metrics.
5. Include a data explanation page describing the dataset, features, target variables, and limitations.
6. Include an SDG impact page explaining how the project connects to Myanmar’s rural development and humanitarian context.
7. Make the project easy to demonstrate in an internship interview within 3–5 minutes.

## Final Business Understanding Statement
This project aims to develop an explainable machine learning decision-support system for rural finance and livelihood support in Myanmar. The system predicts household financial vulnerability and possible loan repayment risk for farming households affected by poverty, agriculture shocks, market disruption, conflict, climate events, and disaster-related income loss.

The project is designed not to replace human decision-makers, but to help them make fairer, clearer, and more responsible decisions. By combining microfinance risk assessment with household vulnerability analysis, the project supports both business decision-making and SDG-oriented social impact.

## Supporting Evidences/References
The business problem and project direction are supported by evidence from the uploaded Myanmar development, humanitarian, agriculture, microfinance, climate, food security, and cash assistance documents.

### Financial Exclusion and Microfinance Need
Myanmar’s rural and low-income households often face limited access to formal financial services. The micro-finance literature explains that poor households commonly lack access to savings accounts, formal credit, insurance, and reliable financial tools. Microfinance is presented as one mechanism to help low-income households access capital, manage risks, and build more secure livelihoods. This supports the project’s focus on rural financial inclusion and responsible micro-loan decision support. [R1], [R2]

### Poverty and Household Vulnerability
Myanmar’s current poly-crisis has increased poverty and weakened household resilience. The evidence shows that many households are either below the poverty line or barely above it, meaning that even small income, food price, climate, or agricultural shocks can push households into deeper vulnerability. This supports the need for a model that considers household financial stress, not only loan repayment history. [R3]

### Agriculture as a Core Livelihood Sector
Agriculture, fisheries, and livestock are central to Myanmar’s economy, employment, food security, and rural livelihoods. Agriculture employs a large share of the labor force and is dominated by small-scale landholders. Because many rural households depend on agriculture for income, any disruption to farming directly affects household repayment capacity, food security, and livelihood resilience. [R4], [R5]

### Conflict and Agricultural Productivity Risk
Conflict has directly affected agricultural productivity in Myanmar. Evidence from rice producers shows that increases in violent events reduced rice total factor productivity and affected poorer farmers more severely, especially those with less agricultural capital and reduced access to extension services. This supports including conflict exposure, agricultural capital, extension access, and farm disruption indicators in the model. [R6]

### Climate and Disaster Risk
Myanmar’s agriculture sector is highly exposed to climate change, including droughts, floods, intense rainfall, cyclones, temperature increases, and changing rainfall patterns. These climate risks can reduce crop yields, damage assets, and weaken farmers’ income stability. This supports the inclusion of weather shocks, climate-sensitive location, irrigation access, and disaster exposure as important features in the project. [R7], [R8]

### Food Security and Market Price Pressure
Food insecurity in Myanmar is connected to conflict, income loss, rising food prices, disrupted markets, and reduced agricultural production. Food security analysis also shows that many crop producers faced difficulties in crop production, reduced planted area, and expected lower harvests. This supports using food security indicators, market price pressure, and crop production difficulty as signals of household vulnerability. [R9], [R10]

### Minimum Expenditure Basket and Financial Gap
The Minimum Expenditure Basket defines the monthly monetary threshold required for a household to meet essential needs. The MEB document explains that the basket is useful for transfer values, assessments, program design, profiling, targeting, and monitoring. The gap between household income and the MEB can be used to estimate whether a household can meet its basic needs. This strongly supports creating a derived feature such as `financial_gap = household_income - MEB` or `MEB_gap = MEB - household_income`. [R11], [R12]

### Multi-Purpose Cash Assistance and Coping Capacity
The MPC guidance states that cash assistance targets households with multi-sectoral needs and collapsed coping capacity. It highlights indicators such as inability to meet basic needs, high-risk coping strategies, lack of recent assistance, displacement, and the presence of vulnerable household members. This supports using coping strategies as model features, such as selling productive assets, skipping meals, borrowing unsustainably, delaying healthcare, or losing income sources. [R13]

### Earthquake and Shock-Based Livelihood Disruption
The 2025 earthquake addendum shows that disasters can sharply increase humanitarian and livelihood needs. It reports damage to fields, irrigation, grain stores, livestock, markets, infrastructure, and income sources in affected areas. This supports the project’s broader “resilience” framing, where loan risk is not only caused by personal behavior but also by external shocks affecting livelihood capacity. [R14]

### Why These References Support the Final Project Direction
Together, these documents support the decision to build an explainable financial vulnerability and loan risk predictor rather than a simple loan approval model. The evidence shows that rural households in Myanmar face overlapping risks: poverty, limited financial access, agricultural dependence, conflict, climate shocks, food insecurity, market price pressure, and disaster-related livelihood loss.

Therefore, the selected project should not only ask:

> “Will this farmer default?”

It should ask:

> “Is this household financially vulnerable, what factors are driving the risk, and what type of support or loan decision would be most responsible?”

This makes the project more aligned with SDG goals, humanitarian-development thinking, and responsible AI use.

* **[R1]** : Report Microfinance for Poverty Alleviation UNDP May2014
* **[R2]** : Report Afford Two Eat One Financial Inclusion in Rural Myanmar
* **[R3]** : Report Myanmars Enduring Poly-crisis Four Years into a Tumultuous
* **[R4]** : Core Doc Myanmar Climate Change Strategy 2018-2030 ENG
* **[R5]** : Analysis Conflict Agricultural Productivity Evidence from Myanmar
* **[R6]** : Analysis Conflict Agricultural Productivity Evidence from Myanmar
* **[R7]** : Core Doc Myanmar Climate Change Strategy 2018-2030 ENG
* **[R8]** : Core Doc Myanmar Climate Change Strategy 2018-2030 ENG
* **[R9]** : Report Myanmar Economic Fallout Food Insecurity WFP Apr2021
* **[R10]** : fsc food security analysis march 2022
* **[R11]** : Myanmar MEB Techn cal Note CMWG Feb_2026
* **[R12]** : Myanmar MEB Techn cal Note CMWG Feb_2026
* **[R13]** : Myanmar MPCA Guidance and Strategy Feb_2026
* **[R14]** : Myanmar 2025 HNRP Earthquake Flash Addendum - FINAL 11 April
