# 🛡️ Your Bank Just Called — But Was It Really Them? Detecting Phishing Attacks with Machine Learning

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen?style=for-the-badge)

**An end-to-end MLOps pipeline that detects phishing websites before they steal your data.**

[Getting Started](#-getting-started) · [Architecture](#-system-architecture) · [Results](#-model-performance) · [Deployment](#-deployment)

</div>

---

## 📌 The Problem

> **Every 11 seconds**, a new phishing attack is launched. In 2024 alone, phishing was responsible for **over $10 billion in losses** worldwide, and **36% of all data breaches** involved phishing.

Traditional rule-based filters catch known threats — but attackers are evolving faster than the rules. They use **URL shorteners, IP-based addresses, suspicious iframes, fake SSL certificates**, and **domain age manipulation** to bypass conventional detection.

**This project solves that.** By analyzing **30 real-time website features** — from URL structure and domain metadata to traffic patterns and page behavior — this system learns the fingerprint of a phishing site and flags it before a user ever clicks.

Whether it's a fake banking portal, a spoofed login page, or a malicious redirect, the model catches it with **97.4% F1-score on unseen data**.

---

## 🎯 What This Project Does

| Capability | Description |
|---|---|
| 🔍 **Phishing Detection** | Classifies websites as legitimate or phishing based on 30 extracted features |
| 📊 **Automated ML Pipeline** | End-to-end pipeline: Ingestion → Validation → Transformation → Training |
| 🧪 **Experiment Tracking** | All model runs tracked via MLflow + DagsHub |
| 🔄 **Data Drift Detection** | Automatically detects distribution shifts using the KS-2 sample test |
| ☁️ **Cloud-Native** | Model artifacts synced to AWS S3; deployed on AWS EC2 via Docker |
| 🌐 **REST API** | FastAPI-based prediction endpoint — upload a CSV and get results instantly |
| 🔁 **CI/CD** | GitHub Actions pipeline: lint → build → push to ECR → deploy to EC2 |

---

## 🏗️ System Architecture

```
                          ┌──────────────────────────────────────────┐
                          │            GitHub Actions CI/CD          │
                          │  (Lint → Build → Push ECR → Deploy EC2)  │
                          └──────────────┬───────────────────────────┘
                                         │
┌──────────────┐    ┌────────────┐    ┌──┴───────────┐    ┌──────────────┐
│   MongoDB    │───▶│   Data     │───▶│    Data      │───▶│    Data      │
│  (Raw Data)  │    │ Ingestion  │    │  Validation  │    │Transformation│
└──────────────┘    └────────────┘    └──────────────┘    └──────┬───────┘
                                                                │
                    ┌────────────┐    ┌──────────────┐    ┌─────┴────────┐
                    │  FastAPI   │◀───│  AWS S3 +    │◀───│    Model     │
                    │  Predict   │    │  ECR + EC2   │    │   Trainer    │
                    │  Endpoint  │    │  (Deploy)    │    │  (Best Model)│
                    └────────────┘    └──────────────┘    └──────────────┘
                          │                                      │
                          │           ┌──────────────┐           │
                          └──────────▶│   MLflow +   │◀──────────┘
                                      │   DagsHub    │
                                      │  (Tracking)  │
                                      └──────────────┘
```

---

## 📁 Project Structure

```
NetworkSecurity/
│
├── networksequrity/                # Core ML package
│   ├── components/                 # Pipeline components
│   │   ├── data_ingestion.py       #   → Fetch data from MongoDB, train-test split
│   │   ├── data_validation.py      #   → Schema checks, column validation, drift detection
│   │   ├── data_transformation.py  #   → KNN Imputer for missing values
│   │   └── model_trainer.py        #   → Train 5 classifiers, hyperparameter tuning, MLflow
│   ├── pipeline/
│   │   └── training_pipeline.py    # Orchestrates the full training workflow
│   ├── cloud/
│   │   └── s3_syncer.py            # Sync artifacts & models to AWS S3
│   ├── entity/                     # Config & artifact dataclasses
│   ├── constant/                   # Constants (paths, params, thresholds)
│   ├── exception/                  # Custom exception handling
│   ├── logging/                    # Structured logging
│   └── utils/                      # ML utilities, metrics, model wrapper
│
├── app.py                          # FastAPI application (train & predict endpoints)
├── main.py                         # Standalone training script
├── push_data.py                    # Push CSV data to MongoDB
├── DockerFile                      # Container definition (Python 3.12-slim)
├── requirements.txt                # Python dependencies
├── setup.py                        # Package configuration
├── data_schema/schema.yaml         # Column schema (30 features + target)
├── Network_data/phisingData.csv    # Raw phishing dataset
├── templates/table.html            # Jinja2 template for prediction results
│
├── .github/workflows/main.yml      # CI/CD: GitHub Actions → ECR → EC2
└── logs/                           # Training run logs with metrics
```

---

## 📊 Model Performance

The pipeline evaluates **5 classifiers** with hyperparameter tuning via `GridSearchCV` and selects the best performer:

| Model | Hyperparameters Tuned |
|---|---|
| Random Forest | `n_estimators`: [8, 16, 32, 128, 256] |
| Decision Tree | `criterion`: [gini, entropy, log_loss] |
| Gradient Boosting | `learning_rate`, `subsample`, `n_estimators` |
| Logistic Regression | Default |
| AdaBoost | `learning_rate`, `n_estimators` |

### 🏆 Best Model Results (from training logs)

<table>
<tr>
<th></th>
<th colspan="3" align="center">Training Set</th>
<th colspan="3" align="center">Test Set</th>
</tr>
<tr>
<th>Run</th>
<th>F1-Score</th>
<th>Precision</th>
<th>Recall</th>
<th>F1-Score</th>
<th>Precision</th>
<th>Recall</th>
</tr>
<tr>
<td><b>Run 1</b></td>
<td>0.9912</td>
<td>0.9888</td>
<td>0.9936</td>
<td>0.9766</td>
<td>0.9702</td>
<td>0.9832</td>
</tr>
<tr>
<td><b>Run 2</b></td>
<td>0.9920</td>
<td>0.9895</td>
<td>0.9945</td>
<td>0.9710</td>
<td>0.9557</td>
<td>0.9869</td>
</tr>
<tr>
<td><b>Run 3</b></td>
<td>0.9915</td>
<td>0.9896</td>
<td>0.9934</td>
<td>0.9738</td>
<td>0.9674</td>
<td>0.9803</td>
</tr>
</table>

> **Key Takeaway:** The best model consistently achieves **~99.1% F1-score on training data** and **~97.4% F1-score on the test set** — with recall above **98%**, meaning almost no phishing site goes undetected.

---

## 🔬 Feature Engineering

The model uses **30 handcrafted features** extracted from website characteristics:

| Category | Features |
|---|---|
| **URL Analysis** | `having_IP_Address`, `URL_Length`, `Shortining_Service`, `having_At_Symbol`, `double_slash_redirecting`, `Prefix_Suffix`, `having_Sub_Domain` |
| **Security Signals** | `SSLfinal_State`, `HTTPS_token`, `Domain_registeration_length` |
| **Page Behavior** | `Redirect`, `on_mouseover`, `RightClick`, `popUpWidnow`, `Iframe` |
| **External References** | `Request_URL`, `URL_of_Anchor`, `Links_in_tags`, `SFH`, `Submitting_to_email`, `Abnormal_URL`, `Favicon` |
| **Domain Intelligence** | `age_of_domain`, `DNSRecord`, `web_traffic`, `Page_Rank`, `Google_Index`, `Links_pointing_to_page`, `Statistical_report`, `port` |

Missing values are handled using **KNN Imputer** (k=3, uniform weights).

---

## 🚀 Deployment

### ✅ Current Status: **DEPLOYED & LIVE**

The application is fully deployed and accessible using the following infrastructure:

| Component | Technology | Status |
|---|---|---|
| **Containerization** | Docker (Python 3.12-slim) | ✅ Running |
| **Container Registry** | AWS ECR (Elastic Container Registry) | ✅ Active |
| **Compute** | AWS EC2 (Self-hosted runner) | ✅ Live |
| **Storage** | AWS S3 (Model artifacts & training data) | ✅ Synced |
| **CI/CD** | GitHub Actions (3-stage pipeline) | ✅ Automated |
| **Experiment Tracking** | MLflow via DagsHub | ✅ Tracking |
| **Database** | MongoDB Atlas | ✅ Connected |

### CI/CD Pipeline Flow

```
Push to main → GitHub Actions triggers:

  1️⃣  Continuous Integration
      └── Lint code → Run unit tests

  2️⃣  Continuous Delivery
      └── Configure AWS → Login to ECR → Build Docker image → Push to ECR

  3️⃣  Continuous Deployment (Self-hosted EC2 runner)
      └── Pull image from ECR → Stop old container → Run new container on port 8000
```

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.12+
- MongoDB Atlas account (or local MongoDB)
- AWS account (for S3 and ECR)
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/Prateekkhicher/PhishGuard.git
cd PhishGuard

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
MONGODB_URL_KEY=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
```

### Push Data to MongoDB

```bash
python push_data.py
```

### Run Training Pipeline

```bash
python main.py
```

### Launch the API Server

```bash
python app.py
```

The API will be live at `http://localhost:8000`.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to interactive API docs |
| `GET` | `/train` | Triggers the full training pipeline |
| `POST` | `/predict` | Upload a CSV file → Get phishing predictions |

---

## 🧪 Experiment Tracking

All training experiments are tracked on **[DagsHub MLflow](https://dagshub.com/Prateekkhicher/PhishGuard)**, including:

- Model hyperparameters
- F1-score, Precision, Recall (train + test)
- Serialized model artifacts
- Run comparisons across experiments

---

## 🐳 Docker

Build and run locally:

```bash
docker build -t network-security .
docker run -d -p 8000:8000 --name networksecurity network-security
```

---

## 📦 Tech Stack

| Layer | Technologies |
|---|---|
| **ML Framework** | scikit-learn (Random Forest, Gradient Boosting, AdaBoost, Decision Tree, Logistic Regression) |
| **Data Processing** | pandas, NumPy, KNN Imputer |
| **Experiment Tracking** | MLflow, DagsHub |
| **API** | FastAPI, Uvicorn |
| **Database** | MongoDB Atlas, PyMongo |
| **Cloud** | AWS S3, ECR, EC2 |
| **CI/CD** | GitHub Actions |
| **Containerization** | Docker |
| **Visualization** | Matplotlib, Seaborn |

---

## 👤 Author

**Prateek Khicher**
- 🔗 [GitHub](https://github.com/Prateekkhicher)

---

## 📜 License

This project is open-source and available for educational and research purposes.

---

<div align="center">

**If you found this project useful, give it a ⭐ on GitHub!**

*Built with 💻 and ☕ by Prateek Khicher*

</div>