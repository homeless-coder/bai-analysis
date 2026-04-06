# BAI Analysis – Anxiety in Engineering Students

## 📌 Project Overview
This project analyzes anxiety levels in engineering students using the Beck Anxiety Inventory (BAI).

The objective is to identify patterns, relationships, and profiles associated with anxiety levels through data analysis techniques.

## 🎯 Objectives
- Analyze the distribution of anxiety levels
- Identify key symptoms associated with higher anxiety
- Explore relationships between demographic variables and anxiety
- Build profiles of students based on symptom patterns

## 🧠 Methodology
The project follows a structured analytical pipeline:

1. Data ingestion
2. Data cleaning and preprocessing
3. Feature engineering
4. Exploratory data analysis (EDA)
5. Modeling and clustering
6. Insights and reporting

## 🗂️ Project Structure

bai-analysis/
│
├── data/
│ ├── raw/ # Raw data (not tracked in Git)
│ ├── processed/ # Cleaned datasets
│
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ ├── 02_eda.ipynb
│ ├── 03_modeling.ipynb
│
├── src/
│ ├── config.py
│ ├── data_loader.py
│ ├── preprocessing.py
│ ├── feature_engineering.py
│
├── outputs/
│ ├── figures/
│ ├── tables/
│
├── .env # Environment variables (not tracked)
├── .gitignore
├── requirements.txt
└── README.md


## 🛠️ Technologies
- Python
- Pandas
- Scikit-learn
- Jupyter Notebook

## 🔐 Data Handling
Raw data is not included in the repository.  
Paths are managed through environment variables.

## 🚀 How to Run

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate

2. Install dependencies:
pip install -r requirements.txt

3. Create .env file:
BAI_DATA_PATH=data/raw/bai_raw.xlsx

4. Run notebooks inside /notebooks

📊 Status
🟡 In progress – Data cleaning phase