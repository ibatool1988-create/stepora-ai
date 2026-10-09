import streamlit as st
from app import ask_stepora

st.set_page_config(
    page_title="STEPORA AI",
    page_icon="🎓",
   layout="centered"
)    
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background-color: #FAF9F6;
    color: #203A5E;
}

h1, h2, h3 {
    color: #203A5E !important;
    font-weight: 800 !important;
}

p, label {
    font-size: 17px !important;
    line-height: 1.7 !important;
}

.stButton > button {
    background-color: #203A5E;
    color: white;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 17px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #648B90;
    color: white;
}
</style>
""", unsafe_allow_html=True)


st.title("🎓 STEPORA AI")
st.subheader("See What Counts. Know What's Next.")

st.write(
    "Discover how your education and experience may connect "
    "to career opportunities in New York."
)

education = st.text_input("What is your highest education?")
country = st.text_input("Where did you complete your education?")

career = st.selectbox(
    "Which career are you interested in?",
    [
        "Clinical Laboratory Technologist",
        "Registered Nurse",
        "Dental Hygienist",
        "Radiologic Technologist",
        "Pharmacy Technician",
        "Teacher"
    ]
)

location = st.text_input("Where do you live?", value="New York")
schedule = st.selectbox(
    "What is your preferred study schedule?",
    ["Flexible", "Evening", "Weekend", "Hybrid", "Full-time"]
)

if st.button("Build My Path"):
    if not education or not country:
        st.warning("Please enter your education and country.")
    elif career != "Clinical Laboratory Technologist":
        st.info(
            "This career pathway is coming soon. "
            "Our verified prototype currently supports "
            "Clinical Laboratory Technologist."
        )
    else:
        profile = (
            f"My highest education is {education}. "
            f"I completed my education in {country}. "
            f"I live in {location}. "
            f"I want to become a {career}. "
            f"My preferred study schedule is {schedule}."
        )

        with st.spinner("Building your pathway..."):
            try:
                result = ask_stepora(profile)
                st.markdown(result.replace("$", r"\$"))
            except Exception:
                st.error(
                    "STEPORA could not generate your pathway. "
                    "Please check the AI connection and try again."
                )