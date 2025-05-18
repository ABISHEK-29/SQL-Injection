# SQL Injection Detection using Deep Learning

This repository demonstrates detection of SQL injection attacks using deep learning and hybrid machine learning methods. It includes Jupyter notebooks for data exploration and model building, as well as a Flask web application that simulates registration and login processes with real-time SQL injection detection.

## Features

- **Deep Learning Pipeline**: Uses an autoencoder for unsupervised feature extraction, elastic CNN for advanced pattern recognition, and a classifier (Dense or XGBoost) for classifying SQL queries as benign or malicious.
- **Real-world Datasets**: Utilizes multiple SQL injection datasets for model training and evaluation.
- **Web Demo**: Flask-based app that allows users to register, login, and attempt SQL injection payloads to test detection.
- **Activity Logging**: Tracks login, registration, and SQL injection alerts.
- **Reproducible Research**: All steps from data loading to model evaluation are documented in Jupyter notebooks.

## Repository Structure

```
SQL-Injection/
│
├── app.py                 # Flask web application for demo and detection
├── sqli-notebook.ipynb    # Main notebook: data analysis, model training
├── test.ipynb             # Notebook for dataset handling and quick tests
├── dataset/               # Folder for SQL injection CSV datasets (not included)
├── templates/             # HTML templates for Flask app
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── (model files)          # Saved models: .h5 (Keras), .pkl (XGBoost), etc.
```
> **Note:** This structure is based on a limited file listing and may be incomplete. [See the full file list on GitHub.](https://github.com/ABISHEK-29/SQL-Injection)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ABISHEK-29/SQL-Injection.git
cd SQL-Injection
```

### 2. Dataset Preparation

- Download SQL injection datasets from [Kaggle](https://www.kaggle.com/datasets/syedsaqlainhussain/sql-injection-dataset)
- Place all CSV files (`sqli.csv`, `sqliv2.csv`, `SQLiV3.csv`, etc.) in the `dataset/` directory.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
Core requirements: `pandas`, `numpy`, `scikit-learn`, `tensorflow`, `keras`, `xgboost`, `flask`

### 4. Run the Jupyter Notebook

Open `sqli-notebook.ipynb` to explore data and reproduce deep learning experiments.

### 5. Run the Web Application

```bash
python app.py
```
Visit [http://localhost:8080](http://localhost:8080) in your browser.

## Model Details

- **Autoencoder**: For feature extraction from SQL queries.
- **Elastic CNN**: For advanced feature learning.
- **Classifier**: Dense or XGBoost for final detection.
- **Model Persistence**: Models saved as `.h5` (Keras) and `.pkl` (XGBoost).

## Acknowledgments

- Datasets: [Kaggle SQL Injection Dataset](https://www.kaggle.com/datasets/syedsaqlainhussain/sql-injection-dataset)
- Built with Python, Flask, TensorFlow, Keras, and XGBoost.

## License

For educational and research use. See dataset and code files for license specifics.

---

**Author:** [ABISHEK-29](https://github.com/ABISHEK-29)

```
This README includes a repository structure inferred from a partial file listing. For a complete view, visit the [GitHub file browser](https://github.com/ABISHEK-29/SQL-Injection).