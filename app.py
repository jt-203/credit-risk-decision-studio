import math
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Credit Risk Decision Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# UI styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #ffffff;
        color: #111827;
    }

    [data-testid="stHeader"] {
        background: #ffffff;
    }

    [data-testid="stSidebar"] {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    div.stAlert {
        border-radius: 12px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #111827;
        letter-spacing: -0.02em;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
        min-height: 110px;
    }

    .info-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .info-card-text {
        font-size: 0.95rem;
        line-height: 1.45;
        color: #374151;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Core scoring functions
# -----------------------------
def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def estimate_pd(
    fico: float,
    income: float,
    dti: float,
    loan: float,
    emp_years: float,
    delinq: float,
    util: float,
    inquiries: float,
    term: float,
) -> float:
    term_factor = 0.18 if term == 60 else 0.0

    score = (
        -1.35
        + (680 - fico) / 82
        + 0.05 * dti
        + 1.25 * (loan / max(income, 1))
        - 0.07 * emp_years
        + 0.52 * delinq
        + 0.028 * util
        + 0.16 * inquiries
        + term_factor
    )
    return max(0.01, min(sigmoid(score), 0.95))


def estimate_lgd(fico: float, util: float, dti: float) -> float:
    lgd = 0.36 + (680 - fico) / 1000 + util / 220 + dti / 500
    return max(0.20, min(lgd, 0.90))


def decision(pd_value: float, el_value: float, policy: str) -> str:
    limits = {
        "Conservative": {"pd": 0.07, "el": 0.05},
        "Balanced": {"pd": 0.12, "el": 0.08},
        "Growth": {"pd": 0.18, "el": 0.12},
    }
    rule = limits[policy]

    if pd_value <= rule["pd"] and el_value <= rule["el"]:
        return "Approve"
    if pd_value <= rule["pd"] * 1.25:
        return "Review"
    return "Decline"


def risk_grade(pd_value: float) -> str:
    if pd_value < 0.04:
        return "A"
    if pd_value < 0.07:
        return "B"
    if pd_value < 0.11:
        return "C"
    if pd_value < 0.16:
        return "D"
    if pd_value < 0.22:
        return "E"
    return "F"


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Credit Risk Decision Studio")
st.sidebar.caption("A streamlined borrower risk scoring and lending decision app.")

policy = st.sidebar.selectbox(
    "Underwriting Policy",
    ["Conservative", "Balanced", "Growth"],
    index=1,
    help="Controls how strict the final decision thresholds are.",
)

show_methodology = st.sidebar.toggle("Show methodology notes", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**How to use this app**\n"
    "1. Enter borrower details\n"
    "2. Review risk metrics\n"
    "3. Interpret the recommended decision\n"
    "4. Upload a portfolio for batch review"
)

# -----------------------------
# Header
# -----------------------------
st.title("Credit Risk Decision Studio")
st.markdown(
    "A professional borrower risk assessment tool that estimates "
    "**probability of default**, **loss given default**, and **expected loss** "
    "to support more consistent lending decisions."
)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Purpose</div>
            <div class="info-card-text">
                Evaluate borrower-level credit risk using transparent scorecard logic.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Designed for</div>
            <div class="info-card-text">
                Analytics demos, underwriting concepts, and portfolio decision support.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Output</div>
            <div class="info-card-text">
                Risk metrics, grade assignment, and a recommendation aligned to policy.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if show_methodology:
    st.markdown("### Methodology")
    st.write(
        "This demo uses a transparent scorecard-style approach rather than a black-box model. "
        "That makes the logic easier to explain in interviews, demos, and stakeholder conversations."
    )

st.markdown("---")

# -----------------------------
# Main borrower analysis section
# -----------------------------
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown("## Borrower Application Inputs")
    st.caption("Enter borrower and loan characteristics below. The app scores the application in real time.")

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        fico = st.slider(
            "FICO Score",
            min_value=550,
            max_value=850,
            value=700,
            step=5,
            help="Higher scores generally indicate lower default risk.",
        )
        income = st.number_input(
            "Annual Income ($)",
            min_value=20000,
            max_value=300000,
            value=80000,
            step=1000,
            help="Gross annual borrower income.",
        )
        loan = st.number_input(
            "Loan Amount ($)",
            min_value=1000,
            max_value=75000,
            value=15000,
            step=500,
            help="Requested loan balance.",
        )
        term = st.selectbox(
            "Loan Term (Months)",
            [36, 60],
            index=0,
            help="Longer terms can raise borrower risk exposure.",
        )

    with input_col2:
        dti = st.slider(
            "Debt-to-Income Ratio (%)",
            min_value=0.0,
            max_value=50.0,
            value=20.0,
            step=0.5,
            help="Higher DTI usually signals tighter repayment capacity.",
        )
        emp_years = st.slider(
            "Years Employed",
            min_value=0,
            max_value=25,
            value=5,
            step=1,
            help="Simple employment stability signal.",
        )
        delinq = st.slider(
            "Past Delinquencies",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            help="Prior delinquency activity is a strong risk signal.",
        )
        util = st.slider(
            "Credit Utilization (%)",
            min_value=0,
            max_value=100,
            value=30,
            step=1,
            help="Measures how much revolving credit is currently in use.",
        )

    inquiries = st.slider(
        "Recent Credit Inquiries",
        min_value=0,
        max_value=8,
        value=1,
        step=1,
        help="Higher inquiry counts may indicate more active recent credit seeking.",
    )

with right:
    st.markdown("## Decision Summary")
    st.caption("Outputs update automatically as you adjust the inputs.")

    pd_est = estimate_pd(fico, income, dti, loan, emp_years, delinq, util, inquiries, term)
    lgd_est = estimate_lgd(fico, util, dti)
    el_est = pd_est * lgd_est
    grade = risk_grade(pd_est)
    rec = decision(pd_est, el_est, policy)

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Probability of Default", f"{pd_est:.2%}")
    metric_col2.metric("Loss Given Default", f"{lgd_est:.2%}")

    metric_col3, metric_col4 = st.columns(2)
    metric_col3.metric("Expected Loss", f"{el_est:.2%}")
    metric_col4.metric("Risk Grade", grade)

    st.markdown("### Recommended Action")
    if rec == "Approve":
        st.success(f"**{rec}** — the application falls within the selected underwriting policy.")
    elif rec == "Review":
        st.warning(f"**{rec}** — the application is near threshold and may need analyst review.")
    else:
        st.error(f"**{rec}** — modeled risk is above the acceptable threshold for the selected policy.")

    st.markdown("### Quick Interpretation")
    drivers = []
    if fico < 660:
        drivers.append("Lower credit score is increasing modeled default risk.")
    if dti > 28:
        drivers.append("Debt-to-income is relatively elevated, which weakens repayment flexibility.")
    if util > 60:
        drivers.append("High revolving utilization is putting pressure on the overall risk profile.")
    if delinq > 0:
        drivers.append("Prior delinquency activity is materially increasing the risk score.")
    if loan / max(income, 1) > 0.30:
        drivers.append("Loan size is high relative to borrower income.")
    if inquiries >= 4:
        drivers.append("Recent inquiry volume suggests heavier recent credit activity.")
    if not drivers:
        drivers.append("The application appears relatively stable under the current assumptions.")

    for item in drivers:
        st.write(f"- {item}")

# -----------------------------
# Portfolio mode
# -----------------------------
st.markdown("---")
st.markdown("## Portfolio Analytics")
st.write(
    "Upload a CSV of applications to review portfolio-level credit quality, expected loss, "
    "and decision mix. This helps move the tool from single-borrower analysis toward an analyst workflow."
)

required_columns = [
    "fico",
    "income",
    "dti",
    "loan",
    "emp_years",
    "delinq",
    "util",
    "inquiries",
    "term",
]

with st.expander("See required CSV format"):
    st.code(
        """fico,income,dti,loan,emp_years,delinq,util,inquiries,term
720,95000,14.5,12000,6,0,24,1,36
645,54000,29.0,18000,2,1,67,3,60
690,82000,19.5,15000,4,0,38,2,36""",
        language="csv",
    )

uploaded_file = st.file_uploader(
    "Upload a portfolio CSV",
    type=["csv"],
    help="Upload a file with the required columns to generate portfolio summaries and decision distributions.",
)

if uploaded_file is not None:
    try:
        portfolio_df = pd.read_csv(uploaded_file)
        missing_cols = [col for col in required_columns if col not in portfolio_df.columns]

        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
        else:
            scored_rows = []

            for _, row in portfolio_df.iterrows():
                row_pd = estimate_pd(
                    row["fico"],
                    row["income"],
                    row["dti"],
                    row["loan"],
                    row["emp_years"],
                    row["delinq"],
                    row["util"],
                    row["inquiries"],
                    row["term"],
                )
                row_lgd = estimate_lgd(row["fico"], row["util"], row["dti"])
                row_el = row_pd * row_lgd
                row_decision = decision(row_pd, row_el, policy)
                row_grade = risk_grade(row_pd)

                scored = row.to_dict()
                scored["pd"] = row_pd
                scored["lgd"] = row_lgd
                scored["expected_loss"] = row_el
                scored["grade"] = row_grade
                scored["decision"] = row_decision
                scored_rows.append(scored)

            scored_df = pd.DataFrame(scored_rows)

            st.markdown("### Portfolio Summary")
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("Applications", f"{len(scored_df):,}")
            p2.metric("Average PD", f"{scored_df['pd'].mean():.2%}")
            p3.metric("Average LGD", f"{scored_df['lgd'].mean():.2%}")
            p4.metric("Average Expected Loss", f"{scored_df['expected_loss'].mean():.2%}")

            p5, _, p6, _ = st.columns(4)
            p5.metric("Approval Rate", f"{scored_df['decision'].eq('Approve').mean():.2%}")
            p6.metric("Review Rate", f"{scored_df['decision'].eq('Review').mean():.2%}")

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown("#### Decision Distribution")
                decision_counts = scored_df["decision"].value_counts()
                st.bar_chart(decision_counts)

            with chart_col2:
                st.markdown("#### Risk Grade Distribution")
                grade_counts = scored_df["grade"].value_counts().sort_index()
                st.bar_chart(grade_counts)

            st.markdown("#### Portfolio Detail")
            st.dataframe(scored_df, use_container_width=True)

    except Exception as exc:
        st.error(f"There was a problem reading the portfolio file: {exc}")

# -----------------------------
# Supporting business section
# -----------------------------
st.markdown("---")
st.markdown("## Underwriting Guidance")
st.write(
    "This tool is meant to support decision-making, not replace judgment. Teams can use the output "
    "to standardize first-pass reviews, compare policy settings, and identify applications that deserve closer analysis."
)

guide_col1, guide_col2, guide_col3 = st.columns(3)
guide_col1.markdown(
    "### Approval Zone\n"
    "Applications in this range generally show stronger credit quality, lower leverage pressure, "
    "and more manageable expected loss."
)
guide_col2.markdown(
    "### Review Zone\n"
    "These files may still be viable, but usually benefit from analyst review, compensating factors, "
    "or tighter structure."
)
guide_col3.markdown(
    "### Decline Zone\n"
    "Applications in this range exceed the selected policy tolerance and may warrant rejection "
    "or substantial restructuring."
)

st.markdown("---")
st.caption(
    "Demo note: this app uses explainable scorecard logic for presentation purposes. "
    "It can later be upgraded with trained models, downloadable reporting, and deeper portfolio monitoring."
)