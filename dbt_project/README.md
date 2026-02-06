\# 📈 Quantitative Momentum Data Pipeline



A self-contained \*\*Analytics Engineering\*\* project that automates the ingestion, transformation, and visualization of stock market data to identify "Golden Cross" momentum signals.



Built with the \*\*Modern Data Stack\*\*: Python, DuckDB, dbt, and Streamlit.



!\[Dashboard Screenshot](path/to/your/screenshot.png) 

\*(Note: Upload your dashboard screenshot to the repo and link it here!)\*



\## 🏗 Architecture



This project follows a robust \*\*ELT (Extract, Load, Transform)\*\* architecture, running entirely locally using high-performance tooling.



```mermaid

graph LR

&nbsp;   A\[Yahoo Finance API] -->|Extract \& Load (Python)| B\[(DuckDB Data Lake)]

&nbsp;   B -->|Transform \& Test (dbt)| C\[Staging Views]

&nbsp;   C -->|Dimensional Modeling| D\[Marts (Star Schema)]

&nbsp;   D -->|Visualize| E\[Streamlit Dashboard]

### Resources:

* Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
* Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
* Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
* Find [dbt events](https://events.getdbt.com) near you
* Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
