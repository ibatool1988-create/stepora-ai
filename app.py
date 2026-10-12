import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from verified_data import VERIFIED_CAREER_DATA
from verified_data import VERIFIED_CAREER_DATA


load_dotenv()

SYSTEM_PROMPT = """
OUTPUT FORMATTING RULES:
- Display all dollar amounts clearly, such as $345 and $50.
- Never use backticks around dollar amounts.
- Do not use broken Markdown formatting.
- Use clear headings, readable paragraphs, and bullet points.
 - Keep examination requirements accurate:
  The converted passing score of at least 75 applies to the qualifying
  ASCPi MLS examination taken on or after January 1, 2015.
- Do not state that the converted score of 75 applies to the ASCP MLS examination.
- Current ASCP MLS certification satisfies the NYSED examination requirement.
  CRITICAL ACCURACY RULES:
- AMT MLS certification may satisfy an NYSED education alternative,
  but it does not automatically satisfy the examination requirement.
- NYSED education pathway 3 requires a bachelor's or master's degree
  from a qualifying NAACLS-accredited MLS program.
- Do not recommend an associate's degree alone as satisfying
  Clinical Laboratory Technologist licensure requirements.
- Do not claim that all science bachelor's degrees automatically qualify.
  Additional qualifying training or experience may be required.
  - A bachelor's degree in biology, chemistry, or another science alone
  does not automatically satisfy NYSED Clinical Laboratory Technologist
  education requirements. Additional qualifying training or experience
  may be required under the applicable pathway.

- Do not state that a foreign credential evaluation by an outside agency
  is always required. Tell the user that NYSED determines whether the
  submitted education satisfies its requirements.

- Do not describe the provisional permit as generally available to anyone
  who is still completing education. It has specific NYSED eligibility
  criteria that must be met.

- When information is not included in the verified NYSED data,
  say it must be confirmed rather than guessing or generalizing.
  - For a person starting with only a high-school diploma, do not predict that
  NYSED pathway 6 or 7 is the most likely route. Present a qualifying
  NAACLS-accredited MLS bachelor's program or NYSED-registered
  licensure-qualifying bachelor's program as a direct education option.

- Do not refer to an "NYSED-approved credential evaluation service" unless
  that requirement and provider have been verified. Tell the user to confirm
  foreign-education documentation requirements directly with NYSED.

- Do not say that ASCP MLS certification is irrelevant until separate NYSED
  education requirements are met. Current ASCP MLS certification is itself
  one of NYSED's listed education alternatives and also satisfies the
  examination requirement.
  - Always use the credential name "ASCPi MLS". Never write "ASCP MLSi".

- Do not say that a foreign high-school diploma must be equivalent to a
  U.S. bachelor's degree. Treat high-school and university education as
  different education levels.

- Do not state or estimate salaries unless salary data is included in
  VERIFIED_CAREER_DATA. If salary information is not verified, say that
  verified salary information is not currently available.

- Do not say that every applicant needs two years of clinical laboratory
  experience. Experience requirements apply only to the specific NYSED
  pathway that requires them.

- Do not state that ASCP MLS or qualifying ASCPi MLS certification can
  satisfy the examination requirement only after a separate education
  pathway has been completed. Follow the exact NYSED education-alternative
  and examination rules in VERIFIED_CAREER_DATA.

- Never invent program duration, tuition, salary, credential-evaluation
  requirements, or other facts that are not present in VERIFIED_CAREER_DATA.
  - Never state that pathway 7 is the only or most appropriate pathway
  for a person starting with a high-school diploma.
  A qualifying NAACLS-accredited MLS bachelor's program (pathway 3)
  or a NYSED-registered licensure-qualifying bachelor's program
  (pathway 4) are direct education options.

- Keep certification roles separate:
  Current ASCP MLS certification is an NYSED education alternative
  and also satisfies the examination requirement.
  Qualifying ASCPi MLS certification may also satisfy the applicable
  education and examination requirements.
  AMT MLS may satisfy an education alternative but does not
  automatically satisfy NYSED's examination requirement.

You are STEPORA AI, an AI career pathway navigator.

STEPORA's principle is:
"See What Counts. Know What's Next."

Your purpose is to help internationally educated, immigrant,
first-generation, returning, and working adults understand how
their previous education and experience may connect to U.S.
career pathways.

For this prototype, focus on New York State.

STRICT ACCURACY RULES:

1. Use only information the user actually provided.
   Never assume coursework, clinical training, work experience,
   licenses, certifications, transcript contents, grades, or
   credentials that the user did not state.
IMPORTANT: Never claim that a user's documents, transcripts,
credentials, or applications are already on file with NYSED
unless the user explicitly confirms this.

Distinguish Clinical Laboratory Technologist from Clinical
Laboratory Technician. Do not suggest that an associate's
degree alone qualifies someone for Technologist licensure.

Never call the examination the "NYSED Clinical Laboratory
Technologist exam." Instead, refer to an examination accepted
by NYSED, and direct users to the official requirements for
current examination options.
CRITICAL RULE FOR HIGH-SCHOOL-ONLY APPLICANTS:
If the user reports high school as their highest education,
do not suggest that the high-school diploma could be equivalent
to a bachelor's degree.

Explain that the applicant needs an appropriate post-secondary
education pathway. Include NYSED-registered Clinical Laboratory
Science bachelor's programs as a possible route.

Never invent an examination name. Use the exact wording
"an examination accepted by NYSED" unless the verified
official source identifies a specific examination.

Do not recommend credential evaluation for bachelor's-degree
equivalency when the user reports only high-school education.

Do not promise a preliminary credential evaluation or
pre-approval service unless the official NYSED source
explicitly confirms that service is available.

When information is missing or cannot be verified, clearly
state what is unknown. Never invent eligibility, program
approval, tuition, fees, timelines, or credential acceptance.

2. A degree title or major alone does NOT prove that a person
   completed particular courses.
   For example, if someone says they have a Biology degree,
   do not say that they completed microbiology, chemistry,
   biochemistry, laboratory training, or any other specific
   coursework unless they explicitly provided that information.

3. Never assume that a foreign degree automatically qualifies
   someone for a New York professional license.

4. Never claim that a credential evaluation organization is
   accepted by New York unless verified information provided
   to you confirms it.

5. Never claim that a school or program satisfies New York
   licensure, certification, accreditation, examination, or
   educational requirements unless verified information
   provided to you confirms it.

6. Never invent or guess:
   - licensing requirements
   - accepted credential evaluators
   - approved or accredited programs
   - tuition
   - financial-aid eligibility
   - admission requirements
   - examination requirements
   - salary
   - deadlines
   - processing times
   - program length

7. If a fact cannot be established from the user's information
   or verified information supplied to you, say:
   "This needs to be verified with the appropriate official source."

8. Clearly distinguish among:
   - CONFIRMED: directly stated by the user or supplied as verified data
   - MAY BE RELEVANT: potentially useful but not yet verified
   - NEEDS VERIFICATION: cannot yet be confirmed

9. Do not say "what already counts" about specific coursework,
   credits, training, or professional eligibility unless it is
   actually confirmed.

10. Do not tell a user "you qualify," "you are eligible," or
    "your degree meets the requirement" without sufficient
    verified information.

11. For regulated New York professions, explain that final
    eligibility must be confirmed through the appropriate
    official New York State licensing authority.

12. Do not fabricate citations, URLs, agencies, schools,
    programs, or official requirements.

13. If important information is missing, identify exactly what
    needs to be checked rather than filling the gap with an
    assumption.

14. School or program suggestions must be described only as
    options to investigate unless verified data confirms that
    they meet the applicable requirements.

15. Costs and timelines must be labeled as estimates unless
    verified current information has been supplied.

Use cautious wording such as:
"Based on the information you provided, this appears to be the
pathway most relevant to your background."

For non-controlled cases, keep the answer concise (no more than 450
words) and use exactly these seven headings, in this order:

1. Starting Point
2. What May Count
3. What Is Still Missing
4. Most Relevant Possible Pathway
5. Exam and Certification Cautions
6. Next 3 Steps
7. Official Sources

Give exactly three numbered next steps. Use only the official source URLs
supplied in VERIFIED OFFICIAL INFORMATION. Do not add an introduction,
conclusion, or other sections.

For a reported bachelor's degree in biology, say that the degree may be
relevant to NYSED education pathway 6, which requires an acceptable
bachelor's degree plus qualifying NAACLS-accredited MLS training or an
acceptable advanced certificate in clinical laboratory technology.
Do not assume the degree is acceptable, that the additional training is
complete, or that the user must earn another MLS bachelor's degree.
Explain that NYSED must verify which pathway and requirements apply.

State the certification and examination distinctions accurately:
- Current ASCP MLS certification is an NYSED education alternative and
  satisfies the examination requirement.
- The ASCPi MLS examination is accepted when taken on or after
  January 1, 2015, with a converted passing score of at least 75.
- AMT MLS may satisfy a specified NYSED education alternative, but does
  not automatically satisfy the examination requirement.

Do not state or estimate program duration, timelines, credential-
evaluation agencies or requirements, examination authorization,
salary, financial aid, or permit eligibility unless the exact fact is
explicitly stated in VERIFIED OFFICIAL INFORMATION. Otherwise omit these
topics entirely. Do not say or imply the user qualifies; direct them to
NYSED to verify final eligibility.

Be practical, brief, and explicit about uncertainty.
"""

def get_openai_client():
    api_key = os.getenv("NEBIUS_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["NEBIUS_API_KEY"]
        except (KeyError, StreamlitSecretNotFoundError):
            api_key = None

    if not api_key:
        raise RuntimeError(
            "NEBIUS_API_KEY is not set. Add your Nebius API key before running STEPORA."
        )

    return OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=api_key,
    )


def validate_stepora_response(answer, user_message):
    """Catch misleading statements before showing a pathway."""
    text = answer.lower()
    user_text = user_message.lower()

    if "ny sed clinical laboratory technologist examination" in text or "nysed clinical laboratory technologist examination" in text:
        return False, "The examination name needs verification."

    if "high school" in user_text or "high-school" in user_text:
        misleading = [
            "high-school diploma is equivalent to a bachelor's degree",
            "high-school credentials are equivalent to a bachelor's degree",
            "residency in new york makes you eligible",
        ]
        if any(phrase in text for phrase in misleading):
            return False, "The education or eligibility guidance needs correction."
    import re

    
    exam_score_error = re.search(
        r"\bascp\s+mls\s+exam(?:ination)?\b"
        r"[^\n.]{0,150}"
        r"(?:converted\s+(?:passing\s+)?score|"
        r"(?:passing\s+)?converted\s+score)",
        text,
        re.IGNORECASE,
    )

    if exam_score_error:
        return False, (
            "The converted passing score must not be "
            "attributed to the ASCP MLS examination."
        )


    return True, ""


def validate_fallback_structure(answer):
    """Require the general AI response to use the concise seven-section format."""
    import re

    required_sections = [
        "Starting Point",
        "What May Count",
        "What Is Still Missing",
        "Most Relevant Possible Pathway",
        "Exam and Certification Cautions",
        "Next 3 Steps",
        "Official Sources",
    ]
    headings = []

    for line in answer.splitlines():
        heading = re.sub(r"^\s{0,3}#{1,6}\s*", "", line.strip())
        heading = re.sub(r"^\d+[.)]\s*", "", heading).strip(" #*_:\t")
        matching_section = next(
            (
                section
                for section in required_sections
                if heading.casefold() == section.casefold()
            ),
            None,
        )
        if matching_section:
            headings.append(matching_section)
        elif re.match(r"^\s{0,3}#{1,6}\s+", line):
            headings.append(heading)

    if headings != required_sections:
        return False, "The response must contain the seven required sections in order."
    if len(answer.split()) > 450:
        return False, "The response must be no more than 450 words."

    return True, ""





def ask_stepora(user_message):
    user_lower = user_message.lower()

    if "high school" in user_lower or "high-school" in user_lower:
        return """
## Your Personalized Career Pathway

### 1. Where You Are Now
You currently have a high-school education and want to become a
**New York Clinical Laboratory Technologist**.

A high-school diploma alone does not satisfy the NYSED education
requirements for Clinical Laboratory Technologist licensure.

### 2. Your Clearest Education Routes
Two direct education options are:

- Complete a bachelor's or master's Clinical Laboratory Science/MLS
  program that is **NAACLS-accredited at the time of graduation**.
- Complete a bachelor's or master's Clinical Laboratory Technology
  program that is **registered by NYSED as licensure-qualifying**.

A general biology, chemistry, or other science bachelor's degree alone
does not automatically satisfy the licensure requirements. Additional
qualifying training or experience may be required under other NYSED pathways.

### 3. Examination and Certification
After meeting an applicable NYSED pathway, the examination requirement
must also be satisfied.

- Current **ASCP MLS** certification satisfies the NYSED examination requirement.
- Qualifying **ASCPi MLS** certification may satisfy the applicable NYSED
  education and examination requirements.
- The converted passing score of at least **75** applies to the qualifying
  ASCPi MLS examination taken on or after January 1, 2015.
- **AMT MLS** may satisfy an NYSED education alternative, but it does not
  automatically satisfy the examination requirement.

### 4. New York Fees and Permits
- NYSED licensure and first registration fee: **$345**
- Limited permit fee: **$50**

A limited permit is not available with only a high-school diploma.
It is for applicants who meet the licensure requirements except for
the examination.

A provisional permit also has specific NYSED eligibility requirements;
a high-school diploma alone is not sufficient.

### 5. Your Next 3 Steps
1. Research **NAACLS-accredited MLS bachelor's programs** and
   **NYSED-registered licensure-qualifying programs**.
2. Contact NYSED to confirm the documentation required for your
   education completed outside the United States.
3. Compare programs that fit your preferred schedule before applying.

### 6. Official Sources
- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-requirements
- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-application-forms

**See What Counts. Know What's Next.**
"""

    if "chemistry" in user_lower:
        return """
## Your Personalized Career Pathway

### 1. Where You Are Now

You have a **bachelor's degree in Chemistry** and want to become a
**New York Clinical Laboratory Technologist**.

Your chemistry degree may be useful toward an NYSED pathway, but a
chemistry bachelor's degree alone does not automatically satisfy the
Clinical Laboratory Technologist education requirement.

### 2. Your Most Relevant Education Route

One NYSED education option specifically allows an acceptable bachelor's
degree in **biology, chemistry, or physical science** together with
additional qualifying clinical laboratory training.

That additional training may include:

- Qualifying **NAACLS-accredited MLS training**, or
- A qualifying **advanced certificate in clinical laboratory technology**.

NYSED must determine whether your degree and additional training satisfy
the applicable requirements.

### 3. Other NYSED Options

Other possible education routes include:

- A bachelor's or master's MLS program that was **NAACLS-accredited at
  the time of graduation**.
- A bachelor's or master's Clinical Laboratory Technology program
  **registered by NYSED as licensure-qualifying**.
- A clinical laboratory technology program that NYSED determines is
  **substantially equivalent**.

Your existing Chemistry degree should therefore be evaluated before you
assume that you need to complete another bachelor's degree.

### 4. Examination and Certification

- Current **ASCP MLS** certification is an NYSED education alternative
  and also satisfies the examination requirement.
- Qualifying **ASCPi MLS** certification may satisfy the applicable
  education and examination requirements.
- The converted passing score of at least **75** applies to the qualifying
  ASCPi MLS examination taken on or after January 1, 2015.
- **AMT MLS** may satisfy an NYSED education alternative, but it does not
  automatically satisfy the examination requirement.

### 5. Fees and Your Next Steps

- NYSED licensure and first registration fee: **$345**
- Limited permit fee: **$50**

Your next steps are:

1. Gather your Chemistry degree, transcripts, and any laboratory-training
   documentation.
2. Ask NYSED what documentation is required for your education completed
   outside the United States.
3. Determine whether qualifying MLS training or an advanced clinical
   laboratory technology certificate can complete the appropriate
   education pathway for you.

### 6. Official Sources

- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-requirements
- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-application-forms

**See What Counts. Know What's Next.**
"""

    client = get_openai_client()
    verified_context = VERIFIED_CAREER_DATA["clinical_laboratory_technologist"]["verified_guidance"]
    verified_sources = VERIFIED_CAREER_DATA["clinical_laboratory_technologist"]["source_urls"]
    verified_sources_text = "\n".join(verified_sources)

    messages = [
         {"role": "system", "content": SYSTEM_PROMPT},
                   {"role": "system", "content": "VERIFIED OFFICIAL INFORMATION:\n" + verified_context + "\n\nONLY APPROVED SOURCE URLS:\n" + verified_sources_text},
       {"role": "user", "content":
    user_message +
    "\n\nIMPORTANT: Use only the VERIFIED OFFICIAL INFORMATION above for factual licensure requirements. "
    "Do not invent, estimate, or generalize requirements. "
    "If a fact is not in the verified information, say it is not verified. "
    "For a high-school-only applicant, present NAACLS-accredited MLS bachelor's programs "
    "and NYSED-registered licensure-qualifying bachelor's programs as direct education routes. "
    "Do not claim pathway 7 is the only route. "
    "Keep ASCP MLS, ASCPi MLS, and AMT MLS rules separate and accurate."
},
    ]

    response = client.chat.completions.create(
        model="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        messages=messages,
    )

    answer = response.choices[0].message.content
    structure_is_valid, _ = validate_fallback_structure(answer)
    if not structure_is_valid:
        retry_messages = messages + [
            {"role": "assistant", "content": answer},
            {
                "role": "user",
                "content": (
                    "Rewrite the same answer using exactly these seven sections, "
                    "in this order: Starting Point; What May Count; What Is Still "
                    "Missing; Most Relevant Possible Pathway; Exam and Certification "
                    "Cautions; Next 3 Steps; Official Sources. Keep it to 450 words "
                    "or fewer. Do not add any new facts."
                ),
            },
        ]
        response = client.chat.completions.create(
            model="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
            messages=retry_messages,
        )
        answer = response.choices[0].message.content
        structure_is_valid, structure_reason = validate_fallback_structure(answer)

    is_valid, reason = validate_stepora_response(answer, user_message)

    # Reliable hackathon demo pathway:
    # Use a controlled verified response for high-school applicants.
    if "high school" in user_message.lower() or "high-school" in user_message.lower():
        return """
## Your Personalized Career Pathway

### 1. Where You Are Now
You currently have a high-school education and want to become a
**New York Clinical Laboratory Technologist**.

A high-school diploma alone does not satisfy the NYSED education
requirements for Clinical Laboratory Technologist licensure.

### 2. Your Clearest Education Routes
Two direct education options are:

- Complete a bachelor's or master's Clinical Laboratory Science/MLS
  program that is **NAACLS-accredited at the time of graduation**.
- Complete a bachelor's or master's Clinical Laboratory Technology
  program that is **registered by NYSED as licensure-qualifying**.

A general biology, chemistry, or other science bachelor's degree alone
does not automatically satisfy the licensure requirements. Additional
qualifying training or experience may be required under other NYSED pathways.

### 3. Examination and Certification
After meeting an applicable NYSED pathway, the examination requirement
must also be satisfied.

- Current **ASCP MLS** certification satisfies the NYSED examination requirement.
- Qualifying **ASCPi MLS** certification may satisfy the applicable NYSED
  education and examination requirements.
- The converted passing score of at least **75** applies to the qualifying
  ASCPi MLS examination taken on or after January 1, 2015.
- **AMT MLS** may satisfy an NYSED education alternative, but it does not
  automatically satisfy the examination requirement.

### 4. New York Fees and Permits
- NYSED licensure and first registration fee: **$345**
- Limited permit fee: **$50**

A limited permit is not available with only a high-school diploma.
It is for applicants who meet the licensure requirements except for
the examination.

A provisional permit also has specific NYSED eligibility requirements;
a high-school diploma alone is not sufficient.

### 5. Your Next 3 Steps
1. Research **NAACLS-accredited MLS bachelor's programs** and
   **NYSED-registered licensure-qualifying programs**.
2. Contact NYSED to confirm the documentation required for your
   education completed outside the United States.
3. Compare programs that fit your preferred schedule before applying.

### 6. Official Sources
- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-requirements
- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-application-forms

**See What Counts. Know What's Next.**
"""

        if "chemistry" in user_message.lower() and "bachelor" in user_message.lower():
            return """
## Your Personalized Career Pathway

### 1. Where You Are Now

You have a **bachelor's degree in Chemistry** and want to become a
**New York Clinical Laboratory Technologist**.

Your chemistry degree may be useful toward an NYSED pathway, but a
chemistry bachelor's degree alone does not automatically satisfy the
Clinical Laboratory Technologist education requirement.

### 2. Your Most Relevant Education Route

One NYSED education option specifically allows an acceptable bachelor's
degree in **biology, chemistry, or physical science** together with
additional qualifying clinical laboratory training.

That additional training may include:

- Qualifying **NAACLS-accredited MLS training**, or
- A qualifying **advanced certificate in clinical laboratory technology**.

NYSED must determine whether your degree and additional training satisfy
the applicable requirements.

### 3. Other NYSED Options

Other possible education routes include:

- A bachelor's or master's MLS program that was **NAACLS-accredited at
  the time of graduation**.
- A bachelor's or master's Clinical Laboratory Technology program
  **registered by NYSED as licensure-qualifying**.
- A clinical laboratory technology program that NYSED determines is
  **substantially equivalent**.

Your existing Chemistry degree should therefore be evaluated before you
assume that you need to complete another bachelor's degree.

### 4. Examination and Certification

- Current **ASCP MLS** certification is an NYSED education alternative
  and also satisfies the examination requirement.
- Qualifying **ASCPi MLS** certification may satisfy the applicable
  education and examination requirements.
- The converted passing score of at least **75** applies to the qualifying
  ASCPi MLS examination taken on or after January 1, 2015.
- **AMT MLS** may satisfy an NYSED education alternative, but it does not
  automatically satisfy the examination requirement.

### 5. Fees and Your Next Steps

- NYSED licensure and first registration fee: **$345**
- Limited permit fee: **$50**

Your next steps are:

1. Gather your Chemistry degree, transcripts, and any laboratory-training
   documentation.
2. Ask NYSED what documentation is required for your education completed
   outside the United States.
3. Determine whether qualifying MLS training or an advanced clinical
   laboratory technology certificate can complete the appropriate
   education pathway for you.

### 6. Official Sources

- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-requirements
- https://www.op.nysed.gov/professions/clinical-laboratory-technologists/full-license-application-forms

**See What Counts. Know What's Next.**
"""  
    
    if not is_valid:
        return (
            "STEPORA could not safely verify this pathway. "
            + reason
            + "\n\nPlease review the official NYSED requirements."
        )

    if not structure_is_valid:
        return (
            "STEPORA could not generate the pathway in the required seven-section "
            "format. " + structure_reason
        )

    return answer


if __name__ == "__main__":
    print("\nSTEPORA AI")
    print("See What Counts. Know What's Next.\n")

    user_message = input(
        "Tell STEPORA about your education and career goal: "
    )

    print("\nBuilding your pathway...\n")

    try:
        answer = ask_stepora(user_message)
        print(answer)
    except Exception as error:
        print("\nSTEPORA could not generate the pathway.")
        print("Error:", error)  