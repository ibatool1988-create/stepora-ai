# STEPORA AI
See What Counts. Know What's Next.

## Problem
Internationally educated students and professionals often struggle to understand which prior education, credentials, and experience count toward regulated career pathways in New York. The rules are complex, and missing or unclear guidance can delay career progression.

## Solution
STEPORA AI provides personalized career-pathway guidance using verified regulatory information plus AI-assisted explanation. It helps users understand what may count, what still needs verification, and what to do next.

## How It Works
- User enters education background, country, career goal, location, and schedule preference.
- Critical NYSED licensure facts come from verified pathway logic.
- STEPORA makes a live runtime call to NVIDIA Nemotron through Nebius Token Factory for fallback/general guidance.
- Controlled verified pathways are used for high-stakes licensing facts.
- STEPORA does not rely only on free-form AI for high-stakes licensure facts.

## Hackathon Demo Scope
- Clinical Laboratory Technologist in New York
- Controlled High School pathway
- Controlled Bachelor's in Chemistry pathway
- Controlled Bachelor's in Biology pathway
- Additional careers are future expansion and are not part of the current demo scope

## Tech Stack
- Python
- Streamlit
- Nebius Token Factory
- NVIDIA Nemotron
- OpenAI-compatible API client

## Run Locally
1. Install dependencies from requirements.txt
2. Create a .env file
3. Set NEBIUS_API_KEY
4. Run: streamlit run web_app.py

## Accuracy and Safety
Verified regulatory facts are separated from generative AI explanation to reduce hallucinations and keep the guidance grounded in official pathway rules.

## Official NYSED Sources
https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-requirements
https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-application-forms

## Status
STEPORA AI is a hackathon prototype, not production-ready, and final licensure decisions should be verified with NYSED.
