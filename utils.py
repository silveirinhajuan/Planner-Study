import os
from datetime import datetime
from typing import Callable

import pandas as pd
import streamlit as st

FLASHCARDS_CSV = "formulas.csv"

ID = "id"
QUESTION = "question"
ANSWER = "answer"
DATE_ADDED = "date_added"
NEXT_APPEARANCE = "next_appearance"
TAGS = "tags"

N_CARDS_PER_ROW = 2
DEFAULT_TAGS = [
    "matemática",
    "física",
    "química",
    "redação",
    "inglês"
]


def get_empty_df():
    return pd.DataFrame(columns=[ID, QUESTION, ANSWER, DATE_ADDED])


def save_flashcards(flashcards_df: pd.DataFrame):
    flashcards_df[TAGS] = flashcards_df[TAGS].apply(
        lambda x: ",".join(t.lower() for t in x)
    )
    flashcards_df.to_csv(FLASHCARDS_CSV, index=False, quotechar='"', quoting=1)


def load_all_flashcards():
    if os.path.exists(FLASHCARDS_CSV):
        df = pd.read_csv(
            FLASHCARDS_CSV,
            parse_dates=[DATE_ADDED, NEXT_APPEARANCE],
        )
        df = df.drop_duplicates(subset=QUESTION, keep="first")
        df[TAGS] = df[TAGS].apply(lambda x: x.split(",") if isinstance(x, str) else x)
        return df
    else:
        return get_empty_df()


def concat_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    # If any of the DataFrames is empty, return the other
    if df1.empty:
        return df2
    elif df2.empty:
        return df1
    else:
        return pd.concat([df1, df2], ignore_index=True)


def get_due_flashcards(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) > 0:
        return df[df[NEXT_APPEARANCE] <= datetime.now()]
    else:
        return get_empty_df()


def prepare_flashcard_df(
    question: str,
    answer: str,
    id: int,
    date_added: datetime,
    next_appearance: datetime,
    tags: list,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                ID: id,
                QUESTION: question,
                ANSWER: answer,
                DATE_ADDED: date_added,
                NEXT_APPEARANCE: next_appearance,
                TAGS: tags,
            }
        ]
    )


def get_question():
    due_questions = get_due_flashcards(st.session_state.flashcards_df)
    for i, row in due_questions.iterrows():
        yield i, row


def search(text_search: str, df: pd.DataFrame) -> Callable:
    def search_df():
        if df.empty:
            st.warning("The DataFrame is empty. No data to search.")
            return

        search_items = df[QUESTION].str.contains(text_search, case=False, na=False)
        matching_rows = df[search_items]
        if matching_rows.empty:
            st.info(f"No results found for '{text_search}'.")
            return

        for n_row, row in matching_rows.reset_index().iterrows():
            i = n_row % N_CARDS_PER_ROW
            if i == 0:
                st.write("---")
                cols = st.columns(N_CARDS_PER_ROW, gap="large")
            with cols[n_row % N_CARDS_PER_ROW]:
                st.caption(f"Question {int(row[ID])}")
                st.markdown(f"**{row[QUESTION].strip()}**")
                with st.expander("Answer"):
                    st.markdown(f"*{row[ANSWER].strip()}*")

    return search_df


@st.cache_data(ttl=3600)
def convert_df(df):
    return df.to_csv().encode("utf-8")


def view_flashcards(df):
    if not df.empty:
        df[TAGS] = df[TAGS].apply(lambda x: x.split(",") if isinstance(x, str) else x)
        st.dataframe(
            df,
            use_container_width=True,
            column_order=[QUESTION, ANSWER, ID, DATE_ADDED, NEXT_APPEARANCE, TAGS],
        )
        st.download_button(
            label="Download Flashcards",
            data=convert_df(df),
            file_name="formulas.csv",
            mime="text/csv",
        )
        st.__cached__
    else:
        st.write("No flashcards available.")