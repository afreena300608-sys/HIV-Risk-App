
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="HIV Risk Awareness Tool",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown("""
<div style='text-align:center'>
    <h1>🩺 HIV Risk Awareness & Self-Assessment Tool</h1>
    <h3 style='color:gray;'>Grade 12 Capstone Project by <b>Afreen, Sahana and Lakshika</b></h3>
    <p style='color:gray; font-size:17px'>
        This educational tool helps users understand potential HIV exposure risk.  
        <br><b>This is NOT a diagnostic test — only a healthcare provider can diagnose.</b>
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------
with st.sidebar:
    st.header("📘 About This Project")
    st.write("This Grade 12 capstone project aims to:")
    st.write("• Spread awareness about HIV risks")
    st.write("• Educate on prevention and testing")
    st.write("• Encourage early testing and safe practices")
    st.write("---")
    st.header("📞 Health Resources")
    st.write("- Local hospitals and clinics")
    st.write("- Government HIV testing centers")
    st.write("- Community health organizations")
    st.write("---")
    st.info("Your responses are private and not stored.")

# -------------------------------------------------------
# MAIN FORM
# -------------------------------------------------------
st.subheader("📝 Answer the Questions Below")

with st.form("risk_form"):

    st.markdown("### 1️⃣ Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=12, max_value=100, value=18)
        gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Non-binary/Other"])
    with col2:
        relationship = st.selectbox("Relationship status", ["Single", "In a relationship", "Married", "Prefer not to say"])
        sexual_activity = st.selectbox("Sexual activity in last 3 months", ["No", "Yes, 1 partner", "Yes, multiple partners"])

    st.markdown("### 2️⃣ Protection & Partner Information")
    col3, col4 = st.columns(2)
    with col3:
        condom_use = st.selectbox("How often do you use condoms?", ["Always", "Mostly", "Sometimes", "Never"])
        unprotected_72 = st.checkbox("Had unprotected sex in the last 72 hours?")
    with col4:
        partner_status = st.selectbox("Partner's HIV status", ["Negative", "Positive", "Unknown"])

    st.markdown("### 3️⃣ Needle / Blood Exposure")
    needles = st.checkbox("Shared needles/injection equipment?")
    tattoo = st.checkbox("Got a tattoo/piercing from an unlicensed place?")
    blood_contact = st.checkbox("Contact with someone else's blood?")

    st.markdown("### 4️⃣ Symptoms Checklist")
    symptoms = st.multiselect(
        "Any symptoms in the last few weeks?",
        ["Fever", "Night sweats", "Swollen lymph nodes", "Rash", "Fatigue",
         "Unexplained weight loss", "Sore throat", "None"]
    )

    st.markdown("### 5️⃣ HIV Testing History & Exposure Timeline")
    prev_test = st.selectbox("Previous HIV test", 
                             ["Never", "Over 1 year ago", "Within last 6 months", "Within last month"])
    time_exposure = st.selectbox("If exposure occurred, how long ago?", 
                                 ["No known exposure", "Less than 72 hours", "3 days – 6 weeks", "More than 6 weeks"])

    submit = st.form_submit_button("🔍 Assess My Risk")

# -------------------------------------------------------
# SCORING LOGIC
# -------------------------------------------------------
def calculate_score():
    score = 0

    if sexual_activity == "Yes, multiple partners": score += 4
    elif sexual_activity == "Yes, 1 partner": score += 1

    score += {"Always":0, "Mostly":1, "Sometimes":2, "Never":4}[condom_use]

    if partner_status == "Positive": score += 5
    if partner_status == "Unknown": score += 2

    if unprotected_72: score += 4

    if needles: score += 6
    if tattoo: score += 2
    if blood_contact: score += 2

    high_symptoms = ["Fever", "Night sweats", "Unexplained weight loss", "Swollen lymph nodes"]
    if any(sym in symptoms for sym in high_symptoms): score += 2

    if prev_test == "Never": score += 1

    return score

def categorize(score):
    if score >= 12:
        return "High Risk", "🟥 HIGH RISK — Please get an HIV test as soon as possible."
    elif score >= 6:
        return "Medium Risk", "🟧 MEDIUM RISK — Testing is recommended."
    else:
        return "Low Risk", "🟩 LOW RISK — Low estimated risk. Testing is still the only confirmation."

# -------------------------------------------------------
# SHOW RESULTS
# -------------------------------------------------------
if submit:
    score = calculate_score()
    category, message = categorize(score)

    st.markdown("---")
    st.markdown(f"## 🧪 Your Result: **{category}**")

    if "High" in category:
        st.error(message)
    elif "Medium" in category:
        st.warning(message)
    else:
        st.success(message)

    if time_exposure == "Less than 72 hours":
        st.warning("⚠️ If exposure occurred within 72 hours, visit a healthcare provider immediately — PEP may prevent infection.")

    # -------------------------------------------------------
    # ADDITIONAL SECTION: Recommended Tests
    # -------------------------------------------------------
    st.markdown("### 🧬 Recommended Medical Tests")
    st.write("""
Below are commonly recommended HIV-related tests depending on exposure and timing:

**1. HIV Antigen/Antibody (4th Generation Test)**  
- Detects HIV earlier than older tests  
- Usually recommended after 2–6 weeks  

**2. HIV Rapid Antibody Test**  
- Gives results in minutes  
- Suitable for screening  

**3. HIV RNA / PCR Test (NAT Test)**  
- Detects HIV earliest (10–14 days after exposure)  
- Recommended for high-risk or very recent exposure  

**4. Follow-up testing**  
- A second test may be needed at 6 weeks and 3 months  
""")

    # -------------------------------------------------------
    # MESSAGE FOR SPECIALIST
    # -------------------------------------------------------
    st.markdown("### 🩺 Message for the Healthcare Specialist")
    st.info("""
This individual completed an educational HIV risk self-assessment tool.  
They may require:
- Proper evaluation by a clinician  
- Counseling about risk reduction  
- Appropriate HIV testing based on exposure timing  
- Guidance about PrEP or PEP depending on risk level  
""")

    # Summary
    st.markdown("### 📄 Summary of your answers")
    st.write(f"- Age: {age}")
    st.write(f"- Sexual activity: {sexual_activity}")
    st.write(f"- Condom use: {condom_use}")
    st.write(f"- Partner HIV status: {partner_status}")
    st.write(f"- Symptoms: {', '.join(symptoms)}")
    st.write(f"- Needle/Blood exposure: {'Yes' if (needles or tattoo or blood_contact) else 'No'}")
    st.write(f"- Time since exposure: {time_exposure}")

    st.markdown("---")
    st.write(f"**Assessment completed on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

