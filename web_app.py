import streamlit as st
from app import ask_stepora

st.set_page_config(
    page_title="STEPORA AI",
    page_icon="🎓",
    layout="centered"
)

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
                st.markdown(result)
            except Exception:
                st.error(
                    "STEPORA could not generate your pathway. "
                    "Please check the AI connection and try again."
                )