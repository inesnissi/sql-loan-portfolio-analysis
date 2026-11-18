# SQL Loan Portfolio Analysis

## Project Overview

This project focuses on analysing a simulated UK consumer lending portfolio using SQL and MySQL.

The objective is to investigate lending patterns, customer characteristics, loan performance and credit risk indicators through practical business questions.

The project simulates a consumer lending environment and explores how SQL can be used to extract, manipulate and analyse financial data to support business and risk management decisions.

## Business Context

Consumer lending institutions need to monitor their loan portfolios to understand repayment behaviour, identify potential credit risks and evaluate the performance of their financial products.

This project explores several questions relevant to credit risk and portfolio analysis:

- Which customer regions and employment categories are represented in the portfolio?
- What are the characteristics of the largest loans?
- What factors might be associated with loan defaults?
- How does credit score relate to loan performance?
- How do different lending products perform?

## Dataset

The project uses a simulated UK consumer lending dataset consisting of four relational tables:

| Table | Description |
|---|---|
| Customers | Customer information, including region, date of birth, annual income and employment status. |
| Products | Lending products, including product type and base interest rate. |
| Loans | Loan information, including loan amount, interest rate, credit score, term and repayment status. |
| Repayments | Repayment records, including due dates, payment dates and amounts. |

The dataset is generated using Python and is designed to simulate realistic consumer lending patterns.

**Note:** All data is synthetic and does not represent real customers or financial transactions.

## Tools & Technologies

- **MySQL:** Database management and SQL queries.
- **MySQL Workbench:** Writing and executing SQL queries.
- **Python:** Generating synthetic financial data.
- **Git & GitHub:** Version control and project documentation.

## SQL Skills

The project is structured as a 10-day learning and practical application exercise.

The SQL concepts covered include:

| Topic | Description |
|---|---|
| SELECT & WHERE | Retrieving and filtering records. |
| ORDER BY & LIMIT | Sorting and restricting query results. |
| DISTINCT | Identifying unique values. |
| Aggregations | Using COUNT, SUM, AVG, MIN and MAX. |
| GROUP BY & HAVING | Analysing grouped data. |
| JOINs | Combining information from multiple tables. |
| CASE WHEN | Creating conditional categories. |
| Subqueries | Solving multi-step analytical questions. |
| CTEs | Structuring complex queries. |
| Window Functions | Ranking records and analysing trends. |

## Project Structure

```text
sql-loan-portfolio-analysis/
│
├── README.md
│
├── schema/
│   └── create_tables.sql
│
├── data/
│   ├── generate_data.py
│   └── load_data.sql
│
└── queries/
    ├── day01_basics.sql
    ├── day02_aggregates.sql
    ├── day03_joins.sql
    ├── day04_case_dates.sql
    ├── day05_subqueries.sql
    ├── day06_ctes.sql
    ├── day07_ranking.sql
    ├── day08_trends.sql
    └── day09_risk_report.sql
```

*The query files will be added progressively as the project develops.*

## Project Progress

- [x] Day 0 – Database setup and data generation.
- [x] Day 1 – SQL basics: SELECT, WHERE, ORDER BY, LIMIT and DISTINCT.
- [ ] Day 2 – Aggregations and GROUP BY.
- [ ] Day 3 – JOINs.
- [ ] Day 4 – CASE WHEN, NULLs and date functions.
- [ ] Day 5 – Subqueries.
- [ ] Day 6 – Common Table Expressions (CTEs).
- [ ] Day 7 – Window Functions: Ranking.
- [ ] Day 8 – Window Functions: Running Totals, LAG and LEAD.
- [ ] Day 9 – SQL Assessment-Style Problems.
- [ ] Day 10 – Mock Assessment and Final Risk Report.

## Expected Outcomes

By completing this project, I aim to:

- Develop practical SQL skills using a relational financial dataset.
- Identify potential indicators of credit risk.
- Analyse loan performance across different customer and product segments.
- Develop more complex queries to investigate repayment trends.
- Build a foundation for further financial data analysis and reporting.

## Future Improvements

Potential extensions to this project include:

- Connecting SQL query outputs to Power BI or Tableau.
- Developing a credit risk dashboard.
- Exploring relationships between customer characteristics and default rates.
- Investigating repayment trends and portfolio performance over time.

---

**Author:** Inès Diakiese  
**Project:** SQL Loan Portfolio Analysis  
**Database:** MySQL
