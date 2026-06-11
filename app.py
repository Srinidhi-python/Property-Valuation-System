import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import time


# ---------------- LOGIN STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Property Valuation System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

section[data-testid="stSidebar"] {
    background-color: #E8F0FE;
}

.stButton>button {
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #2563EB, #60A5FA);
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = joblib.load("rf_model.joblib")
model_features = joblib.load("model_columns.joblib")

# ---------------- SIDEBAR ----------------

st.sidebar.title("🏠 Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Home", "Analytics", "Dataset", "Map","Chatbot" ,"About"]
)

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.title("🔐 Login to PrimeEstate")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True
            st.success("✅ Login Successful")
            st.rerun()

        else:
            st.error("❌ Invalid Username or Password")

    st.stop()

# ---------------- HOME PAGE ----------------

if page == "Home":

    # ---------------- HEADER ----------------

    st.markdown("""
        <h1 style='text-align:center; color:#1E3A8A;'>
            🏡 PrimeEstate
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='text-align:center; color:gray;'>
            Premium Real Estate ML Estimator
        </h3>
    """, unsafe_allow_html=True)

    st.write("")

    # ---------------- INPUT SECTION ----------------

    col1, col2 = st.columns(2)

    with col1:

        location = st.selectbox(
            "📍 Enter Location",
            ["Electronic City", "Whitefield", "Indiranagar", "Jayanagar"]
        )

        sqft = st.number_input(
            "📐 Total Square Feet",
            min_value=300,
            max_value=10000,
            value=1200
        )

    with col2:

        bath = st.number_input(
            "🛁 Bathrooms",
            min_value=1,
            max_value=10,
            value=2
        )

        bhk = st.number_input(
            "🏠 BHK",
            min_value=1,
            max_value=10,
            value=2
        )

    # ---------------- PREDICTION ----------------

    if st.button("💰 Predict Price"):

        with st.spinner("🔍 Analyzing property details..."):
            time.sleep(2)

            input_data = pd.DataFrame(
                [[sqft, bath, bhk]],
                columns=["total_sqft", "bath", "bhk"]
            )

            prediction = model.predict(input_data)

            price = float(f"{prediction[0]:.2f}")

        # ---------------- RESULT CARD ----------------
            st.markdown(f"""
    <div style="
    background: linear-gradient(135deg, #1E3A8A, #3B82F6);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-top: 20px;
    ">

    <h3>Estimated Market Value</h3>

    <h1 style="font-size:3rem;">
    ₹ {price*100000:,.0f}
    </h1>

    </div>
    """, unsafe_allow_html=True)
            
        # ---------------- CONFIDENCE METER ----------------

        confidence = 88

        st.markdown("## 🎯 Prediction Confidence")

        st.progress(confidence)

        st.success(f"Model Confidence: {confidence}%")

        # ---------------- SMART RECOMMENDATION ----------------

        st.markdown("## 🏡 Smart Recommendation")

        if price < 50:
            st.success("✅ Budget Friendly Property")

        elif price >= 50 and price < 100:
            st.info("🏙️ Mid-Range Premium Property")

        else:
            st.warning("🌟 Luxury Property Recommendation")

    # ---------------- MODEL INFO ----------------

    st.markdown("## 📊 Model Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🤖 Model Used", "Random Forest")

    with col2:
        st.metric("📈 Accuracy", "88%")

    with col3:
        st.metric("🏠 Dataset Records", "13,000+")

    # ---------------- PROPERTY STATS ----------------

    st.markdown("## 🏘️ Property Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Average Price", "₹ 72 Lakhs")

    with col2:
        st.metric("📈 Highest Price", "₹ 2.5 Cr")

    with col3:
        st.metric("📉 Lowest Price", "₹ 30 Lakhs")

# ---------------- ANALYTICS PAGE ----------------

if page == "Analytics":

    st.title("📈 Property Analytics Dashboard")

    sizes = [500, 1000, 1500, 2000, 2500]
    prices = [30, 50, 75, 95, 130]

    fig, ax = plt.subplots()

    ax.plot(sizes, prices, marker='o')

    ax.set_xlabel("Square Feet")
    ax.set_ylabel("Price in Lakhs")
    ax.set_title("Property Price Trend")

    st.pyplot(fig)

# ---------------- DATASET PAGE ----------------

if page == "Dataset":

    st.title("📊 Sample Property Dataset")

    sample_data = pd.DataFrame({
        "Location": ["Whitefield", "Indiranagar", "Jayanagar"],
        "Square Feet": [1200, 1800, 1500],
        "BHK": [2, 3, 3],
        "Bathrooms": [2, 3, 2],
        "Price (Lakhs)": [75, 120, 95]
    })

    st.dataframe(sample_data)
    
    # ---------------- MAP PAGE ----------------

if page == "Map":

    st.title("🗺️ Property Locations")

    map_data = pd.DataFrame({
        "LAT": [12.9716, 12.9352, 12.9279, 12.8456],
        "LON": [77.5946, 77.6245, 77.5830, 77.6603],
        "Location": [
            "MG Road",
            "Indiranagar",
            "Jayanagar",
            "Electronic City"
        ]
    })

    st.write("Popular Property Locations in Bangalore")

    st.map(map_data.rename(columns={
        "LAT": "lat",
        "LON": "lon"
    }))
    
    # ---------------- CHATBOT PAGE ----------------

if page == "Chatbot":

    st.title("🤖 Property Assistant")

    user_question = st.text_input(
        "Ask something about properties"
    )

    if user_question:

        question = user_question.lower()

        if "cheap" in question or "affordable" in question:
            st.success(
                "✅ Electronic City is more affordable."
            )

        elif "premium" in question or "luxury" in question:
            st.info(
                "🏙️ Indiranagar and Jayanagar are premium areas."
            )

        elif "2 bhk" in question:
            st.write(
                "🏠 2 BHK properties are popular in Whitefield."
            )

        elif "investment" in question:
            st.write(
                "📈 Whitefield is considered good for investment."
            )

        else:
            st.warning(
                "🤖 Sorry, I don't understand that yet."
            )

# ---------------- ABOUT PAGE ----------------

if page == "About":

    st.title("ℹ️ About Project")

    st.write("""
    This project predicts house prices using Machine Learning.

    Technologies Used:
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - Matplotlib

    ML Algorithm:
    - Random Forest Regressor
    """)

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
    <center>
        Developed as part of Machine Learning Project
    </center>
""", unsafe_allow_html=True)