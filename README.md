# Stock-Momentum

Build a pipeline that ingests daily stock data, models it for analysis, and surfaces it for a dashboard.



\\# 📈 Quantitative Momentum Data Pipeline







A self-contained \\\*\\\*Analytics Engineering\\\*\\\* project that automates the ingestion, transformation, and visualization of stock market data to identify "Golden Cross" momentum signals.







Built with the \\\*\\\*Modern Data Stack\\\*\\\*: Python, DuckDB, dbt, and Streamlit.







!\\\[Dashboard Screenshot](path/to/your/screenshot.png) 



\\\*(Note: Upload your dashboard screenshot to the repo and link it here!)\\\*







\\## 🏗 Architecture







This project follows a robust \\\*\\\*ELT (Extract, Load, Transform)\\\*\\\* architecture, running entirely locally using high-performance tooling.







```mermaid



graph LR



\&nbsp;   A\\\[Yahoo Finance API] -->|Extract \\\& Load (Python)| B\\\[(DuckDB Data Lake)]



\&nbsp;   B -->|Transform \\\& Test (dbt)| C\\\[Staging Views]



\&nbsp;   C -->|Dimensional Modeling| D\\\[Marts (Star Schema)]



\&nbsp;   D -->|Visualize| E\\\[Streamlit Dashboard]





