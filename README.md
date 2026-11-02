# 🌾 AgriCredit Resilience
> **Explainable Financial Vulnerability and Loan Risk Predictor for Rural Farmers in Myanmar**

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Vercel-10b981?style=for-the-badge&logo=vercel)](https://agricredit-resilience.vercel.app)
[![API Docs](https://img.shields.io/badge/API-Swagger%20on%20Render-46e3b7?style=for-the-badge&logo=fastapi)](https://agricredit-resilience.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18%20%2B%20Vite-61dafb?style=for-the-badge&logo=react)](https://react.dev/)

AgriCredit Resilience is an explainable machine learning decision-support system designed to evaluate household financial vulnerability and loan repayment risks for rural smallholder farmers in Myanmar. 

Rather than serving as an automated loan approval or rejection system, it acts as a **socially responsible decision-support tool** for microfinance loan officers, livelihood NGOs, and humanitarian cash assistance teams. It helps identify vulnerable households, unpack the driving factors behind financial stress, and suggest appropriate interventions (such as adjusted repayment terms, livelihood support, or cash assistance referrals).

---

## 🌐 Live Deployments

| Component | Platform | URL | Purpose |
| :--- | :--- | :--- | :--- |
| **Modern Frontend** | **Vercel** | [https://agricredit-resilience.vercel.app](https://agricredit-resilience.vercel.app) | Production SPA client (React + Vite + Tailwind CSS) |
| **Inference Backend** | **Render** | [https://agricredit-resilience.onrender.com](https://agricredit-resilience.onrender.com) | FastAPI REST microservice hosting ML inference |
| **Interactive API Docs** | **Render** | [https://agricredit-resilience.onrender.com/docs](https://agricredit-resilience.onrender.com/docs) | Interactive Swagger UI (OpenAPI specification) |
| **API Health Status** | **Render** | [https://agricredit-resilience.onrender.com/health](https://agricredit-resilience.onrender.com/health) | Real-time healthcheck & loaded model registry |

> [!NOTE]
> **Render Cold-Start Notice:** Render's free tier spins down after 15 minutes of inactivity. On the initial visit, the backend may take 30–50 seconds to wake up. The frontend features an auto-reconnect poller displaying `Waking up API...` until the backend is fully initialized.

---

## 🏛️ System Architecture & Decoupled Monorepo

The project is architected as a **decoupled full-stack machine learning system**, featuring a high-performance **FastAPI inference microservice** and a modern **React + Vite + Tailwind CSS** frontend:

```text
[ Modern Frontend ]                HTTP / JSON                [ FastAPI Backend ]               Disk / RAM
 (React + Vite + TS)    <=============================>    (Python REST Microservice)   <===>   (joblib models)
- Port: 3000 (Dev)       POST /api/v1/predict               - Port: 8000 (Dev) / $PORT           - Logistic Regression
- Persona selector       GET  /api/v1/personas              - Pydantic v2 validation             - Decision Tree
- Real-time risk dial    POST /api/v1/simulate              - Feature transformation
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

## 🔌 Port Mapping & Networking Configuration

| Service | Environment | Default Port | Host Address | Configuration / Command |
| :--- | :--- | :---: | :--- | :--- |
| **React Frontend** | Local Dev | `3000` | `http://localhost:3000` | Configured in `frontend/vite.config.ts` (`server.port: 3000`) |
| **FastAPI Backend** | Local Dev | `8000` | `http://127.0.0.1:8000` | `uvicorn src.api.main:app --reload --port 8000` |
| **Streamlit Dashboard** | Local Dev (Optional) | `8501` | `http://localhost:8501` | `streamlit run app/Home.py --server.port 8501` |
| **FastAPI Backend** | Production (Render) | Dynamic | Port assigned via `$PORT` | Configured in `render.yaml` (`uvicorn --port $PORT`) |
| **React Frontend** | Production (Vercel) | `443` (HTTPS) | Global CDN Edge | Reads `VITE_API_URL` environment variable |

### How Local Reverse Proxying Works
In local development, the React frontend runs on port `3000` while FastAPI runs on port `8000`. To eliminate Cross-Origin Resource Sharing (CORS) friction and avoid hardcoded localhost URLs in client code, `frontend/vite.config.ts` includes built-in reverse proxy rules:
```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
    '/health': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  },
}
```
Any request to `http://localhost:3000/api/*` is forwarded seamlessly to `http://127.0.0.1:8000/api/*`. In production, the client automatically points directly to Render via `VITE_API_URL=https://agricredit-resilience.onrender.com`.

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

## 🚀 Getting Started (Local Development)

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

### 3. Launch the FastAPI Backend (Port 8000)
```bash
# Start backend server with hot-reload
uvicorn src.api.main:app --reload --port 8000
```
* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 4. Launch the Modern Frontend UI (Port 3000)
Open a second terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open your browser at [**http://localhost:3000**](http://localhost:3000).

### 5. (Optional) Launch the Legacy Streamlit Dashboard (Port 8501)
If you wish to explore the original multi-page Streamlit analytical dashboard:
```bash
streamlit run app/Home.py --server.port 8501
```
Open your browser at [**http://localhost:8501**](http://localhost:8501).

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
