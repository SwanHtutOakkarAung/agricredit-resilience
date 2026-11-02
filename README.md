# 🌾 AgriCredit Resilience
> **Explainable Financial Vulnerability and Loan Risk Predictor for Rural Farmers in Myanmar**

AgriCredit Resilience is an explainable machine learning decision-support system designed to evaluate household financial vulnerability and loan repayment risks for rural smallholder farmers in Myanmar. 

Rather than serving as an automated loan approval or rejection system, it acts as a **socially responsible decision-support tool** for microfinance loan officers, livelihood NGOs, and humanitarian cash assistance teams. It helps identify vulnerable households, unpack the driving factors behind financial stress, and suggest appropriate interventions (such as adjusted repayment terms, livelihood support, or cash assistance referrals).

---

## 🏛️ System Architecture & Decoupled Monorepo

The project is architected as a **decoupled full-stack machine learning system**, featuring a high-performance **FastAPI inference microservice** and a modern **React + Vite + Tailwind CSS** frontend:

```text
[ Modern Frontend ]                HTTP / JSON                [ FastAPI Backend ]               Disk / RAM
 (React + Vite + TS)    <=============================>    (Python REST Microservice)   <===>   (joblib models)
- Sleek interactive UI   POST /api/v1/predict               - Pydantic validation                - Logistic Regression
- Persona selector       GET  /api/v1/personas              - Feature transformation             - Decision Tree
- Real-time risk dial    POST /api/v1/simulate              - Inference execution
- What-If simulator      GET  /docs (Swagger UI)            - Lifespan model cache
```

| Layer | Directory | Tech Stack | Role |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | **`/frontend`** | React 18, Vite, TypeScript, Tailwind CSS, Lucide | Modern web client featuring one-click case studies, radial risk gauge, and "What-If" policy simulator. |
| **Inference API** | **`/src/api`** | FastAPI, Pydantic, Uvicorn | Production REST microservice serving scikit-learn models with automatic OpenAPI/Swagger docs (`/docs`). |
| **Model Registry** | **`/models`** | scikit-learn, joblib | Serialized ML models (Logistic Regression for probability scoring, Decision Tree for explainability). |
| **Data Tier** | **`/data`** | Pandas, CSV | Raw household tables (`raw/`), Analytical Base Table (`processed/`), and regional reference benchmarks (`reference/`). |
| **Experimentation** | **`/notebooks`** | Jupyter Notebooks | Step-by-step CRISP-DM research from synthetic generation to EDA, feature engineering, and model tuning. |
| **Pipelines** | **`/src`** | Python | Modular ETL and training pipelines (`generate_raw_data.py`, `prepare_abt.py`, `train_models.py`, `evaluate_models.py`). |
| **Legacy UI** | **`/app`** | Streamlit, Plotly | Multi-page Streamlit exploratory dashboard. |

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
* Node.js v18+ (tested on Node v22)
* Git

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/SwanHtutOakkarAung/agricredit-resilience.git
cd agricredit-resilience

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Launch the FastAPI Backend
```bash
# Start backend server with hot-reload
uvicorn src.api.main:app --reload --port 8000
```
* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 4. Launch the Modern Frontend UI
Open a second terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open your browser at [**http://localhost:3000**](http://localhost:3000).

---

## 🌟 Key Application Features

* **One-Click Farmer Case Studies (Personas):**
  * 🔴 **Flood-Displaced Smallholder (Ayeyarwady Delta):** Climate flood inundation $\rightarrow$ *Evaluates to High Risk (100%), recommends humanitarian cash assistance referral rather than debt.*
  * 🟢 **Resilient Commercial Producer (Shan South):** Stable highland producer $\rightarrow$ *Evaluates to Low Risk (0%), recommends standard microfinance expansion.*
  * 🟡 **Input-Stressed Borderline Farmer (Sagaing Dry Zone):** Input inflation shock $\rightarrow$ *Evaluates to Medium Risk, recommends flexible grace periods.*
* **Visual Decision-Support Radial Gauge:** Animated dial showing calibrated vulnerability percentage and ethical lending recommendations.
* **Explainability Drivers:** Breaks down shock drivers (`+ Risk`) versus liquidity/yield buffers (`- Mitigation`).
* **"What-If" Counterfactual Policy Simulator:** Sliders to model emergency cash grants (MPCA), fertilizer subsidies, debt relief, and flood rehabilitation in real time.

---

## 🎯 Alignment with UN Sustainable Development Goals (SDGs)

* **SDG 1: No Poverty:** Promotes inclusive finance by identifying households that need support rather than harsh exclusion.
* **SDG 2: Zero Hunger:** Protects farming households from predatory debt cycles when crop yields are hit by shocks.
* **SDG 8: Decent Work & Economic Growth:** Enhances financial resilience and stability for smallholder agricultural workers.
* **SDG 13: Climate Action:** Incorporates climate shock indicators and coping strategies into credit evaluation.

---

## 👤 Author

* **Swan Htut Oakkar Aung** - [GitHub Profile](https://github.com/SwanHtutOakkarAung)
