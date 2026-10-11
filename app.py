"""Streamlit interface for the course recommendation demo."""

import streamlit as st

from model import recommend_courses


st.set_page_config(
    page_title="Course Compass | Course Finder",
    page_icon="🎓",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 860px; padding-top: 2.5rem; }
    [data-testid="stMetric"] { background: #f4f7fb; padding: 1rem; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎓 Course Compass")
st.caption("Find online courses that match what you want to learn.")

with st.form("course_search"):
    query = st.text_input(
        "What would you like to learn?",
        placeholder="For example: build a machine learning model with Python",
        help="Describe a topic, skill, or goal in your own words.",
    )
    result_count = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)
    submitted = st.form_submit_button("Find courses", type="primary", use_container_width=True)

if submitted:
    if not query.strip():
        st.info("Enter a learning goal to get started.")
    else:
        try:
            recommendations = recommend_courses(query, top_n=result_count)
        except (OSError, ValueError) as error:
            st.error(f"The course catalog could not be loaded: {error}")
        else:
            if recommendations.empty:
                st.warning(
                    "No courses matched those terms. Try a broader topic, such as “data”, “design”, or “business”."
                )
            else:
                st.subheader(f"Recommended courses ({len(recommendations)})")
                st.caption("Ranked by text similarity. Scores indicate similarity, not course quality.")
                for position, course in recommendations.iterrows():
                    with st.container(border=True):
                        left, right = st.columns([5, 1])
                        with left:
                            st.markdown(f"#### {position + 1}. {course['name']}")
                        with right:
                            st.metric("Match", f"{course['score']:.0%}")
                        description = course["description"].strip()
                        st.write(description if len(description) <= 700 else f"{description[:700].rsplit(' ', 1)[0]}…")
                        if course["slug"]:
                            st.link_button(
                                "View course on Coursera",
                                f"https://www.coursera.org/learn/{course['slug']}",
                            )

st.divider()
st.caption("A lightweight content-based demo powered by TF-IDF and cosine similarity.")
