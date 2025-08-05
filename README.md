## Brent Oil Price Change Point Analysis

### Overview

This project analyzes Brent oil price fluctuations from 1987 to 2022 using Bayesian change point modeling with PyMC3. It detects structural breaks in the price series and associates them with major geopolitical and economic events. An interactive dashboard (Flask backend, React frontend) visualizes results, and a LaTeX report summarizes findings.
Folder Structure

## Setup Instructions

Install Dependencies:pip install pandas numpy pymc3 matplotlib flask

Ensure a modern browser for the React frontend.
Prepare Data:
Place brent_oil_prices.csv and events.csv in data/.

Run Analysis:
Execute eda.py for exploratory analysis.
Execute change_point_model.py for change point detection.

Run Dashboard:
Start Flask backend: python web_app/backend/app.py.
Open web_app/frontend/index.html in a browser.

Compile Report:
Run latexmk -pdf docs/report.tex to generate report.pdf.

Dependencies

Python: pandas, numpy, pymc3, matplotlib, flask
LaTeX: texlive-full, texlive-fonts-extra
Browser: For React dashboard (uses CDN-hosted React, Recharts, Tailwind CSS)
