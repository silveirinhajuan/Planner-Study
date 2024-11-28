from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from utils import (
    ANSWER,
    DATE_ADDED,
    DEFAULT_TAGS,
    ID,
    NEXT_APPEARANCE,
    QUESTION,
    TAGS,
    concat_df,
    get_question,
    load_all_flashcards,
    prepare_flashcard_df,
    save_flashcards,
    search,
    view_flashcards,
)

# -------------- app config ---------------
st.set_page_config(page_title="Hey!", page_icon="🚀", layout="centered")
st.subheader("Bem-vindo, Juan!")

# ---------------- SESSION STATE ----------------
if "flashcards_df" not in st.session_state:
    st.session_state.flashcards_df = load_all_flashcards()


# external css
def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")


def update_flashcards(new_flashcard_df: pd.DataFrame):
    if not new_flashcard_df.empty:
        st.session_state.flashcards_df = concat_df(
            st.session_state.flashcards_df, new_flashcard_df
        )
        save_flashcards(st.session_state.flashcards_df)


def update_next_appearance(id: int, next_appearance: datetime):
    if next_appearance is not None:
        st.session_state.flashcards_df.loc[
            st.session_state.flashcards_df[ID] == id, NEXT_APPEARANCE
        ] = next_appearance
        save_flashcards(st.session_state.flashcards_df)


# ---------------- Main page ----------------

tab1, tab2, tab3, tab4 = st.tabs(["Review", "Add", "Search", "View All"])

with tab1:
    try:
        q_no, row = next(get_question())
        st.markdown(
            f"""
            <div class="blockquote-wrapper">
            <div class="blockquote">
            <h1><span style="color:#ffffff">{row[QUESTION]}</span></h1>
            <h4>&mdash; Question no. {row[ID]}</em></h4></div></div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Show Answer"):
            st.latex(row[ANSWER])

        next_appearance = None
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            easy_submit_button: bool = st.button(label="Easy", use_container_width=True)
            if easy_submit_button:
                prev_time_diff = row[NEXT_APPEARANCE] - row[DATE_ADDED]
                next_appearance_days = min(prev_time_diff.days + 2, 60)
                next_appearance = datetime.now() + timedelta(days=next_appearance_days)
        with col2:
            medium_submit_button: bool = st.button(
                label="Medium", use_container_width=True
            )
            if medium_submit_button:
                next_appearance = datetime.now() + timedelta(days=2)
        with col3:
            hard_submit_button: bool = st.button(label="Hard", use_container_width=True)
            if hard_submit_button:
                next_appearance = datetime.now() + timedelta(days=1)

        if next_appearance is not None:
            update_next_appearance(row[ID], next_appearance)
            st.info(
                f"""Next Apperance of this card will be {next_appearance.date().strftime("%d-%m-%Y")}!""",
                icon="🎉",
            )
            st.rerun()
    except StopIteration:
        st.info("Hey! You have completed all the flashcards. Good Job!", icon="🙌")

with tab2:
    with st.form("add_flashcard_form", clear_on_submit=True):
        question = st.text_input("Question")
        answer = st.text_area("Answer")
        tags = st.multiselect("Tags", DEFAULT_TAGS, default=DEFAULT_TAGS[-1])
        submit_button = st.form_submit_button("Add Flashcard")
        if submit_button:
            if question and answer:
                date_added = datetime.now()
                new_flashcard = prepare_flashcard_df(
                    question,
                    answer,
                    id=int(len(st.session_state.flashcards_df) + 1),
                    date_added=date_added,
                    next_appearance=(date_added + timedelta(days=-1)),
                    tags=tags if isinstance(tags, list) else [tags],
                )
                update_flashcards(new_flashcard)
                st.success("Flashcard added successfully!")
            else:
                st.warning("Please enter question and answer!")


with tab3:
    text_search = st.text_input("Search in questions", value="")
    if text_search:
        search(text_search, st.session_state.flashcards_df)()

with tab4:
    options = st.multiselect("Tags", DEFAULT_TAGS)
    show_all = st.checkbox("Show All", value=True)
    if show_all:
        view_flashcards(st.session_state.flashcards_df)
    elif options:
        try:
            filtered_df = st.session_state.flashcards_df[
                st.session_state.flashcards_df[TAGS].apply(
                    lambda x: any(tag in x for tag in options)
                )
            ]
            view_flashcards(filtered_df)
        except KeyError:
            st.warning("No flashcards found with the selected tags!")