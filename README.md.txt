# Qabalan – Odoo POS Sales Visualization

## Overview
This project is a Python-based data analysis and visualization script
developed for internal use at **Qabalan**.

The script processes cleaned transaction data exported from
the **Odoo POS system** and generates business-focused visual insights.

> No real data is included due to company privacy.

## Business Purpose
- Analyze sales volume across the day
- Compare Visa vs Cash usage
- Identify peak hours using 30-minute intervals
- Support operational decision-making

## Features
- Payment method normalization
- Visa & Cash filtering
- 30-minute time aggregation
- Multiple charts for sales insights

## Tech Stack
- Python
- Pandas
- Matplotlib
- Odoo POS

## How to Run
1. Add your cleaned CSV file (not included)
2. Update the filename if needed:
   ```python
   df = pd.read_csv("train22.csv")
