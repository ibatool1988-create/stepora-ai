
import streamlit as st
from app import ask_stepora

st.set_page_config(
    page_title="STEPORA AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: #F8FAFC;
    color: #19385C;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #19385C !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: #19385C;
    color: white;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-weight: 700;
    border: none;
}

.stButton > button:hover {
    background: #468C9C;
    color: white;
}

.hero {
    background: linear-gradient(120deg, #EAF2F7, #FFFFFF);
    padding: 38px;
    border-radius: 20px;
    margin-bottom: 24px;
}

.feature {
    background: #EAF2F7;
    border-radius: 14px;
    padding: 18px;
    min-height: 105px;
}

.result-heading {
    margin-top: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #DCE8F0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("### 🎓 STEPORA AI")
st.caption("SEE WHAT COUNTS. KNOW WHAT'S NEXT.")

st.divider()

left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown("""
    <div class="hero">
        <h1>Your future starts<br>with a clear path.</h1>
        <p style="font-size:19px;color:#385570;">
        Discover how your education and experience
        can help you reach your career goals in New York.
        </p>
        <p>🎓 Verify Your Credits &nbsp;&nbsp; 📍 Explore Career Pathways</p>
        <p>📋 Get Personalized Next Steps</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.subheader("Build Your Career Pathway")
    st.write("Tell us about your education and career goals.")

    education = st.text_input(
        "Your Current Education",
        placeholder="e.g., High School, Bachelor's in Chemistry"
    )

    country = st.text_input(
        "Where did you complete your education?",
        placeholder="e.g., Pakistan"
    )

    career = st.selectbox(
        "Career Goal",
        [
            "Clinical Laboratory Technologist",
            "Registered Nurse",
            "Teacher",
            "Dental Hygienist",
            "Radiologic Technologist",
            "Pharmacy Technician"
        ]
    )

    location = st.selectbox(
        "Where do you live?",
        ["New York", "Other State"]
    )

    schedule = st.selectbox(
        "Preferred Study Schedule",
        ["Flexible", "Evening", "Weekend", "Hybrid", "Full-time"]
    )

    build = st.button(
        "Explore My Path →",
        use_container_width=True
    )

st.write("")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="feature"><b>🏛️ New York Focus</b><p>NYSED licensing requirements</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="feature"><b>🛡️ Trusted Information</b><p>Official sources and verified guidance</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="feature"><b>📚 Compare Programs</b><p>Education options to explore</p></div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="feature"><b>📈 Plan with Confidence</b><p>Understand your next steps</p></div>', unsafe_allow_html=True)

st.markdown('<div class="result-heading"><h2>Your Personalized Career Pathway</h2></div>', unsafe_allow_html=True)

if build:
    if not education.strip() or not country.strip():
        st.warning("Please enter your education and country.")
    elif career != "Clinical Laboratory Technologist":
        st.info("This career pathway is coming soon. Clinical Laboratory Technologist is currently supported.")
    else:
        profile = (
            f"My highest education is {education}. "
            f"I completed my education in {country}. "
            f"I live in {location}. "
            f"I want to become a {career}. "
            f"My preferred study schedule is {schedule}."
        )

      
        with st.spinner("Building your personalized pathway..."):
            try:
                result = ask_stepora(profile)
                import re

                result = re.sub(r'(?<!\w)`345', '$345', result)
                result = re.sub(r'(?<!\w)`50', '$50', result)

                st.markdown(result)
            except Exception:
                st.error(
                    "STEPORA could not generate your pathway. "
                    "Please check the AI connection and try again."
                )
else:
    st.info("Complete the form above and select Explore My Path to see your personalized guidance.")

st.divider()
st.caption("STEPORA AI · See What Counts. Know What's Next.")
