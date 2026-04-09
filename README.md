# Credit Risk Decision Studio

🔗 Live App: [https://your-streamlit-link.streamlit.app](https://credit-risk-decision-studio-utc5sum2r55xsfimkypspu.streamlit.app/)
# Credit Risk Decision Studio

🔗 Live App: [https://your-streamlit-link.streamlit.app](https://credit-risk-decision-studio-utc5sum2r55xsfimkypspu.streamlit.app/)

---

## Overview

This project is an interactive credit risk decision tool that simulates how lenders evaluate borrower risk and make approval decisions.

It allows users to input borrower characteristics and receive:
- Probability of Default (PD)
- Expected Loss (EL)
- Automated approval/decline decisions

It also supports portfolio-level analysis using batch uploads, making it useful for understanding aggregate lending risk.

---

## Features

### Individual Loan Analysis
- FICO score, income, DTI, loan amount inputs
- Real-time risk scoring
- Policy-based approval decision

### Portfolio Analysis
- Upload CSV of borrowers
- Average Probability of Default
- Total Expected Loss
- Approval rate
- Risk distribution visualization

---

## Key Concepts Implemented

- Probability of Default (PD)
- Loss Given Default (LGD)
- Expected Loss = PD × LGD × Exposure
- Risk segmentation and decision thresholds

---

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy

---

## How to Run Locally

```bash
git clone https://github.com/jt-203/credit-risk-decision-studio.git
cd credit-risk-decision-studio
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

fico,income,dti,loan,emp_years,delinq,util,inquiries,term
720,85000,18,15000,5,0,35,1,36
680,60000,25,20000,3,1,55,2,60

Motivation

I built this project to better understand how financial institutions evaluate credit risk and translate that logic into an interactive tool.

The goal was not just to analyze data, but to simulate real decision-making processes used in lending environments.
Future Improvements
Integrate a trained machine learning model (logistic regression)
Add downloadable decision reports
Improve UI/UX for production-level feel
Connect to real-world datasets (e.g., LendingClub)

Author

Jeremiah Tshinyama
Applied Mathematics @ UConn
