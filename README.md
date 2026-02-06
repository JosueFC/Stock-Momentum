# 📈 Quantitative Momentum Data Pipeline


A self-contained **Analytics Engineering** project that automates the ingestion, transformation, and visualization of stock market data to identify "Golden Cross" momentum signals.

Built with the **Modern Data Stack**: Python, DuckDB, dbt, and Streamlit.


<img width="1830" height="965" alt="image" src="https://github.com/user-attachments/assets/25396c98-aa4c-49ab-a145-cd82e460faad" />


## 🏗 Architecture

This project follows a robust **ELT (Extract, Load, Transform)** architecture, running entirely locally using high-performance tooling.


A[Yahoo Finance API] -->|Extract & Load (Python)| B[(DuckDB Data Lake)]
    B -->|Transform & Test (dbt)| C[Staging Views]
    C -->|Dimensional Modeling| D[Marts (Star Schema)]
    D -->|Visualize| E[Streamlit Dashboard]


