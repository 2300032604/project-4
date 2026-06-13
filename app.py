import streamlit as st

st.set_page_config(page_title="AI Call Center Supervisor Assistant", layout="wide")

st.title("📞 AI Call Center Supervisor Assistant")

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
    placeholder="Paste customer-agent conversation here..."
)

if st.button("Analyze"):

    if not transcript.strip():
        st.warning("Please paste a transcript.")
        st.stop()

    lines = [i.strip() for i in transcript.split("\n") if i.strip()]
    text = transcript.lower()

    # -----------------------------
    # Sentiment Analysis
    # -----------------------------

    positive_words = [
        "thank", "thanks", "good",
        "great", "happy", "excellent",
        "resolved", "appreciate"
    ]

    negative_words = [
        "issue", "problem", "angry",
        "bad", "complaint", "delay",
        "poor", "unhappy", "frustrated"
    ]

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        sentiment = "Positive"
    elif neg > pos:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # -----------------------------
    # Risk Level
    # -----------------------------

    if sentiment == "Negative":
        risk = "High"
    elif sentiment == "Neutral":
        risk = "Medium"
    else:
        risk = "Low"

    # -----------------------------
    # Key Discussion Points
    # -----------------------------

    customer_points = []

    for line in lines:
        lower = line.lower()

        if lower.startswith("customer") or lower.startswith("patient"):
            customer_points.append(
                line.split(":", 1)[1].strip()
                if ":" in line else line
            )

    # -----------------------------
    # Summary Generation
    # -----------------------------

    summary = []

    if customer_points:
        summary.append(
            f"The customer contacted regarding {category.lower()} services."
        )

        for point in customer_points[:4]:
            summary.append(point)

    else:
        summary.append(
            "Customer interaction was reviewed successfully."
        )

    # -----------------------------
    # Next Best Actions
    # -----------------------------

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
#-----------------------------
    # Display Results
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📝 Summary")

        for item in summary:
            st.write("•", item)

        st.subheader("😊 Sentiment")
        st.info(sentiment)

        st.subheader("⚠ Risk Level")

        if risk == "High":
            st.error(risk)
        elif risk == "Medium":
            st.warning(risk)
        else:
            st.success(risk)

    with col2:

        st.subheader("📌 Key Discussion Points")

        if customer_points:
            for point in customer_points:
                st.write("•", point)
        else:
            st.write("No customer points found.")

        st.subheader("🎯 Next Best Actions")

        for action in actions[category]:
            st.write("✅", action)

    # -----------------------------
    # Metrics
    # -----------------------------

    st.subheader("📊 Call Statistics")

    c = 0
    a = 0

    for line in lines:
        low = line.lower()

        if low.startswith("customer") or low.startswith("patient"):
            c += 1

        elif low.startswith("agent"):
            a += 1

    m1, m2, m3 = st.columns(3)

    m1.metric("Customer Messages", c)
    m2.metric("Agent Messages", a)
    m3.metric("Total Lines", len(lines))

    # -----------------------------
    # Supervisor Recommendation
    # -----------------------------

    st.subheader("👨‍💼 Supervisor Recommendation")

    st.write(
        f"""
Review the conversation and ensure that all
recommended actions for the {category.lower()} case
are completed. Monitor customer satisfaction and
follow up where necessary.
"""
    )
    #
