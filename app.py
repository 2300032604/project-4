import streamlit as st

st.set_page_config(
    page_title="AI Call Center Supervisor Assistant",
    page_icon="📞",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: #e5e7eb;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1200px;
}

.hero {
    text-align: center;
    padding: 45px 20px;
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid #1e293b;
    border-radius: 22px;
    margin-bottom: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}

.hero-badge {
    display: inline-block;
    background: rgba(37, 99, 235, 0.15);
    color: #60a5fa;
    border: 1px solid #2563eb;
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 12px;
}

.hero-title span {
    color: #38bdf8;
}

.hero-subtitle {
    font-size: 18px;
    color: #94a3b8;
    max-width: 760px;
    margin: auto;
    line-height: 1.6;
}

.card {
    background: #0f172a;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #1e293b;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #60a5fa;
    margin-bottom: 14px;
}

.stTextArea textarea {
    background-color: #020617;
    color: #e5e7eb;
    border-radius: 14px;
    border: 1px solid #334155;
}

.stRadio label {
    color: #e5e7eb;
}

.stButton button {
    background: linear-gradient(90deg, #2563eb, #0284c7);
    color: white;
    border-radius: 12px;
    padding: 0.75rem 2.2rem;
    font-weight: 700;
    border: none;
}

.stButton button:hover {
    background: linear-gradient(90deg, #1d4ed8, #0369a1);
    color: white;
}

div[data-testid="stMetric"] {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 18px;
    border-radius: 16px;
}

hr {
    border: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-badge">AI Powered Supervisor Dashboard</div>
    <div class="hero-title">AI Call Center <span>Supervisor Assistant</span></div>
    <div class="hero-subtitle">
        Analyze customer-agent conversations, identify sentiment, detect risk level,
        extract key discussion points, and generate next best actions for supervisors.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

category = st.radio(
    "Select Category",
    [
        "Loan",
        "Insurance",
        "Telecom",
        "E-Commerce",
        "Health",
        "Credit Card",
        "Complaint / Support",
        "General"
    ],
    horizontal=True
)

transcript = st.text_area(
    "Paste Call Transcript",
    height=300,
    placeholder="Customer: I am facing an issue with my loan application.\nAgent: I will check your details."
)

analyze = st.button("Analyze Call")

st.markdown('</div>', unsafe_allow_html=True)

if analyze:

    if not transcript.strip():
        st.warning("Please paste a transcript.")
        st.stop()

    lines = [i.strip() for i in transcript.split("\n") if i.strip()]
    text = transcript.lower()

    positive_words = [
        "thank", "thanks", "good", "great", "happy",
        "excellent", "resolved", "appreciate", "satisfied"
    ]

    negative_words = [
        "issue", "problem", "angry", "bad", "complaint",
        "delay", "poor", "unhappy", "frustrated", "not working"
    ]

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        sentiment = "Positive"
        risk = "Low"
    elif neg > pos:
        sentiment = "Negative"
        risk = "High"
    else:
        sentiment = "Neutral"
        risk = "Medium"

    customer_points = []

    for line in lines:
        lower = line.lower()
        if lower.startswith("customer") or lower.startswith("patient"):
            customer_points.append(
                line.split(":", 1)[1].strip() if ":" in line else line
            )

    summary = []

    if customer_points:
        summary.append(f"The customer contacted regarding {category.lower()} services.")
        for point in customer_points[:4]:
            summary.append(point)
    else:
        summary.append("Customer interaction was reviewed successfully.")

    actions = {
        "Loan": [
            "Verify customer documents",
            "Check loan eligibility",
            "Perform credit assessment",
            "Schedule follow-up call"
        ],
        "Insurance": [
            "Verify policy details",
            "Review claim information",
            "Validate supporting documents",
            "Update customer"
        ],
        "Telecom": [
            "Check network/service status",
            "Create technical ticket",
            "Verify account details",
            "Follow up with customer"
        ],
        "E-Commerce": [
            "Verify order details",
            "Check shipment status",
            "Process refund/replacement if needed",
            "Notify customer"
        ],
        "Health": [
            "Verify patient details",
            "Confirm appointment/treatment",
            "Share medical instructions",
            "Schedule follow-up"
        ],
        "Credit Card": [
            "Verify eligibility",
            "Review application",
            "Perform KYC verification",
            "Update application status"
        ],
        "Complaint / Support": [
            "Create support ticket",
            "Escalate issue",
            "Assign responsible team",
            "Track resolution"
        ],
        "General": [
            "Review customer request",
            "Provide assistance",
            "Follow up if required",
            "Close interaction"
        ]
    }

    customer_count = 0
    agent_count = 0

    for line in lines:
        low = line.lower()

        if low.startswith("customer") or low.startswith("patient"):
            customer_count += 1
        elif low.startswith("agent"):
            agent_count += 1

    st.markdown("### 📊 Call Overview")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Customer Messages", customer_count)
    m2.metric("Agent Messages", agent_count)
    m3.metric("Total Lines", len(lines))
    m4.metric("Risk Level", risk)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Call Summary</div>', unsafe_allow_html=True)

        for item in summary:
            st.write("•", item)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">😊 Sentiment Analysis</div>', unsafe_allow_html=True)

        if sentiment == "Positive":
            st.success(sentiment)
        elif sentiment == "Negative":
            st.error(sentiment)
        else:
            st.info(sentiment)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 Key Discussion Points</div>', unsafe_allow_html=True)

        if customer_points:
            for point in customer_points:
                st.write("•", point)
        else:
            st.write("No customer points found.")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Next Best Actions</div>', unsafe_allow_html=True)

        for action in actions[category]:
            st.write("✅", action)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👨‍💼 Supervisor Recommendation</div>', unsafe_allow_html=True)

    st.write(
        f"""
        Review the conversation carefully and ensure all recommended actions for the 
        **{category.lower()}** case are completed. Monitor customer satisfaction, 
        assign ownership, and follow up where necessary.
        """
    )

    st.markdown('</div>', unsafe_allow_html=True)
