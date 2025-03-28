# 🦠 COVID-19 Data Analysis with Python & MySQL

This project performs a full pipeline of COVID-19 case analysis using Python, web scraping, and MySQL for data storage. It retrieves and processes pandemic data from HTML sources, stores structured records in a MySQL database, and generates meaningful visualizations to uncover patterns such as infection trends, recovery rates, and country-level comparisons.

Built using an Object-Oriented Programming (OOP) approach, the project is modular and split into classes for handling scraping, requests, file I/O, database operations, and data analysis.

---

## 🔧 Project Setup

### 1 Clone the Repository

```bash
git clone https://github.com/Yibhir0/covid_cases_data_analysis.git
cd covid_cases_data_analysis

### 2 Start MySQL with Docker

```bash
docker-compose up -d

### 3 Set Up the Python Environment

```bash
python -m venv env
source env/bin/activate        # On Windows: .\env\Scripts\activate
pip install -r requirements.txt

### 4 How to Run the Program

```bash
python DriverClass.py

