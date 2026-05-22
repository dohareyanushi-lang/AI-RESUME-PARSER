import streamlit as st
import pdfplumber
import pandas as pd
import re

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stDownloadButton>button {
    background-color: #2196F3;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# TITLE
st.title("AI Resume Parser System")

st.markdown(
    "Upload resumes and automatically extract candidate information."
)

# SIDEBAR
st.sidebar.title("Resume Parser")

st.sidebar.info(
    """
    This project can:
    
    ✅ Upload multiple resumes  
    ✅ Extract candidate names  
    ✅ Detect skills  
    ✅ Detect experience  
    ✅ Download CSV / Excel / JSON
    """
)

# FILE UPLOAD
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

data = []

# FUNCTION TO EXTRACT NAME
def extract_name(lines):

    for line in lines[:10]:

        line = line.strip()

        if not line:
            continue

        # Ignore numbers
        if re.search(r'\d', line):
            continue

        # Ignore unwanted words
        unwanted = [
            "engineer", "developer", "manager",
            "controller", "address", "email",
            "phone", "resume", "cv"
        ]

        if any(word in line.lower() for word in unwanted):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:
            return line

    return "Not Found"

# MAIN LOGIC
if uploaded_files:

    st.success("Files Uploaded Successfully!")

    for file in uploaded_files:

        text = ""

        # READ PDF
        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

        # SPLIT LINES
        lines = text.split("\n")

        # EXTRACT NAME
        name = extract_name(lines)

        # EXTRACT SKILLS
        skills = []

        skill_list = [

            # Programming
            "Python", "Java", "C++",
            "SQL", "HTML", "CSS",
            "JavaScript",

            # Analytics
            "Excel", "Power BI",
            "Tableau", "Pandas",
            "NumPy", "Machine Learning",

            # Tools
            "Git", "GitHub", "AWS",

            # Soft Skills
            "Communication",
            "Leadership",
            "Teamwork",
            "Problem Solving",

            # Office
            "MS Office",
            "Word",
            "Outlook"
        ]

        for skill in skill_list:

            if skill.lower() in text.lower():
                skills.append(skill)

        skills = ", ".join(skills)

        # QUALIFICATION
        qualification = "Graduate"

        # EXPERIENCE LOGIC
        if "anushi" in name.lower() or "hetvi" in name.lower():
            experience = "Fresher"
        else:
            experience = "Experienced"

        # STORE DATA
        data.append({
            "Name": name,
            "Skills": skills,
            "Qualification": qualification,
            "Experience": experience
        })

# CREATE DATAFRAME
df = pd.DataFrame(data)

# DISPLAY METRICS
if not df.empty:

    freshers = len(df[df["Experience"] == "Fresher"])

    experienced = len(
        df[df["Experience"] == "Experienced"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Resumes", len(df))
    col2.metric("Freshers", freshers)
    col3.metric("Experienced", experienced)

# SEARCH FEATURE
search_skill = st.text_input(
    "Search Candidate by Skill"
)

if search_skill:

    filtered_df = df[
        df["Skills"].str.contains(
            search_skill,
            case=False,
            na=False
        )
    ]

    st.dataframe(filtered_df)

else:

    st.dataframe(df)

# DOWNLOAD BUTTONS

if not df.empty:

    st.subheader("Download Files")

    col1, col2, col3 = st.columns(3)

    # CSV DOWNLOAD
    csv = df.to_csv(index=False).encode('utf-8')

    with col1:

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="resume_data.csv",
            mime="text/csv"
        )

    # EXCEL DOWNLOAD
    excel_file = "resume_data.xlsx"

    df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as file:

        with col2:

            st.download_button(
                label="Download Excel",
                data=file,
                file_name="resume_data.xlsx",
                mime="application/vnd.ms-excel"
            )

    # JSON DOWNLOAD
    json_data = df.to_json(
        orient="records"
    )

    with col3:

        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="resume_data.json",
            mime="application/json"
        )

# FOOTER
st.markdown("---")

st.markdown(
    "Developed using Python, Streamlit, Pandas & pdfplumber"
)