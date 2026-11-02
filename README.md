# 🌾 AgriCredit Resilience
> **Explainable Financial Vulnerability and Loan Risk Predictor for Rural Farmers in Myanmar**

AgriCredit Resilience is an explainable machine learning decision-support system designed to evaluate household financial vulnerability and loan repayment risks for rural smallholder farmers in Myanmar. 

Rather than serving as an automated loan approval or rejection system, it acts as a **socially responsible decision-support tool** for microfinance loan officers, livelihood NGOs, and humanitarian cash assistance teams. It helps identify vulnerable households, unpack the driving factors behind financial stress, and suggest appropriate interventions (such as adjusted repayment terms, livelihood support, or cash assistance referrals).

---

## 🏛️ Project Architecture & Mental Model

The repository is structured around a clear separation of concerns, following standard **CRISP-DM** (Cross-Industry Standard Process for Data Mining) and modern Machine Learning engineering principles:

```text
[1. Experimentation]        [2. Production Pipeline]         [3. Artifacts]           [4. User Interface]
     /notebooks       ===>            /src            ===>    /data & /models   ===>         /app
(Explore & Prototype)        (ETL & Training Scripts)        (ABT & .joblib)          (Streamlit Dashboard)
                                      ||
                                      \/
                                   /reports
                            (Findings & Metrics)
```

| Directory | Layer / Mental Model Role | Description |
| :--- | :--- | :--- |
| **`/app`** | **Front End** | Multi-page Streamlit web application providing an intuitive UI for risk assessment, model explanations, market price feasibility, and SDG impact metrics. |
| **`/data`** | **Data Tier (Backend Storage)** | Houses raw tables (`raw/`), the feature-engineered Analytical Base Table (`processed/farmer_vulnerability_abt.csv`), and reference documentation (`reference/`). |
| **`/models`** | **Model Store (ML Backend)** | Stores trained, serialized machine learning model artifacts (`.joblib`), serving as the project's inference engine. |
| **`/notebooks`** | **Experimentation Lab** | CRISP-DM research notebooks (01 through 06) used for exploratory data analysis, hypothesis testing, feature experimentation, and prototyping. |
| **`/reports`** | **Findings & Deliverables** | Business and data understanding documentation, evaluation summaries, and quantitative benchmark reports for stakeholders. |
| **`/src`** | **Data & ML Pipelines** | Modular, reproducible Python scripts transforming experimental notebook code into production-grade pipelines (data generation, ABT preparation, training, evaluation, and UI helper functions). |

---

## 📁 Repository Structure

```text
agricredit-resilience/
├── app/                           # Multi-page Streamlit Dashboard (Frontend)
│   ├── Home.py                    # Landing page & executive summary
│   └── pages/
│       ├── 1_Risk_Prediction.py   # Interactive farmer vulnerability assessment
│       ├── 2_Model_Explanation.py # Feature contributions & interpretable drivers
│       ├── 3_Market_Feasibility.py# Local food prices & Minimum Expenditure Basket (MEB)
│       ├── 4_Model_Evaluation.py  # Confusion matrix, ROC-AUC, and precision-recall curves
│       └── 5_SDG_Impact.py        # Alignment with UN Sustainable Development Goals
├── data/                          # Data Storage Layer
│   ├── raw/                       # Raw simulated data (households, agriculture, coping, etc.)
│   ├── processed/                 # Analytical Base Table (farmer_vulnerability_abt.csv)
│   └── reference/                 # Business & data dictionaries
├── models/                        # Serialized ML Models
│   ├── logistic_regression_model.joblib  # Primary probability-based model
│   └── decision_tree_model.joblib        # Transparent rule-based support model
├── notebooks/                     # CRISP-DM Sequential Experimentation
│   ├── 01_generate_raw_tables.ipynb
│   ├── 02_data_understanding.ipynb
│   ├── 03_data_preparation_abt.ipynb
│   ├── 04_modeling_decision_tree.ipynb
│   ├── 05_modeling_logistic_regression.ipynb
│   └── 06_evaluation.ipynb
├── reports/                       # Project Findings & Stakeholder Reports
│   ├── business_understanding.md
│   ├── data_understanding_preparation.md
│   └── model_comparison_summary.csv
├── src/                           # Production Pipelines
│   ├── config.py                  # Global configurations, seed, and file paths
│   ├── generate_raw_data.py       # Raw synthetic data generator
│   ├── prepare_abt.py             # Feature engineering & ABT builder
│   ├── train_models.py            # Model training & serialization pipeline
│   ├── evaluate_models.py         # Evaluation and metrics benchmarking
│   └── app_utils.py               # Helper routines for the Streamlit UI
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation & architecture overview
```

---

## 🤖 Models & Benchmark Results

The system evaluates two complementary models:
1. **Logistic Regression (Primary Model):** Probability-based classification optimized for calibrated risk scoring.
2. **Decision Tree (Support Model):** Transparent, rule-based model for explainability and clear decision paths.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Role |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | **85.67%** | **90.56%** | **86.24%** | **88.35%** | **0.9484** | Main probability-based prediction model |
| **Decision Tree** | 80.67% | 85.03% | 84.13% | 84.57% | 0.9007 | Explainable rule-based support model |

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+ (tested on Python 3.12)
* Git

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/SwanHtutOakkarAung/agricredit-resilience.git
cd agricredit-resilience

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard
```bash
streamlit run app/Home.py
```
Open your browser at `http://localhost:8501`.

### 4. Running the Pipelines
To regenerate raw data, rebuild the Analytical Base Table (ABT), retrain models, or produce evaluations:
```bash
# Step 1: Generate raw tables
python src/generate_raw_data.py

# Step 2: Build the Analytical Base Table (ABT)
python src/prepare_abt.py

# Step 3: Train and export models
python src/train_models.py

# Step 4: Evaluate and update benchmark report
python src/evaluate_models.py
```

---

## 🎯 Alignment with UN Sustainable Development Goals (SDGs)

* **SDG 1: No Poverty:** Promotes inclusive finance by identifying households that need support rather than harsh exclusion.
* **SDG 2: Zero Hunger:** Protects farming households from predatory debt cycles when crop yields are hit by shocks.
* **SDG 8: Decent Work & Economic Growth:** Enhances financial resilience and stability for smallholder agricultural workers.
* **SDG 13: Climate Action:** Incorporates climate shock indicators and coping strategies into credit evaluation.

---

## 👤 Author

* **Swan Htut Oakkar Aung** - [GitHub Profile](https://github.com/SwanHtutOakkarAung)
