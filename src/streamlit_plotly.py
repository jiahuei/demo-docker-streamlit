r"""
Created on 21/9/2021 5:52 PM
@author: jiahuei

streamlit run streamlit_plotly.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

# from numpy.polynomial import Polynomial as T


def main():
    st.title("Plotly Demo: COVID-19 Vaccination Data Visualisation")

    # CSV data file
    upload_help = "Provide the OWID CSV file"
    uploaded_file = st.sidebar.file_uploader(upload_help)
    if uploaded_file is None:
        st.info(f"{upload_help}, by uploading it in the sidebar")
        return

    # Convert to Pandas DF
    df_raw = pd.read_csv(uploaded_file)
    df = df_raw.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Filter by date
    key = "people_fully_vaccinated_per_hundred"
    df = df.loc[df[key].dropna().index]
    date = st.slider(
        "Select a date",
        min_value=df["date"].min().to_pydatetime(),
        max_value=df["date"].max().to_pydatetime(),
        value=pd.to_datetime("today").normalize().to_pydatetime(),
        step=None,
    )
    df = df.loc[pd.to_datetime(date) - df["date"] <= pd.Timedelta(14, unit="d")]
    df = df.loc[pd.to_datetime(date) - df["date"] >= pd.Timedelta(0, unit="d")]

    # Keep only recent data
    df_filtered = (
        df.sort_values("date")
        .groupby("iso_code")
        .tail(1)
        .sort_values(key, ascending=False)
        .loc[
            :,
            [
                "iso_code",
                "continent",
                "location",
                "date",
                "new_cases_smoothed_per_million",
                "new_deaths_smoothed_per_million",
                "icu_patients_per_million",
                "positive_rate",
                "people_vaccinated_per_hundred",
                "people_fully_vaccinated_per_hundred",
                "total_boosters_per_hundred",
                "gdp_per_capita",
                "human_development_index",
                "median_age",
                "aged_65_older",
            ],
        ]
    )
    shortlisted_countries = (
        "malaysia",
        "thailand",
        "singapore",
        "china",
        "iceland",
        "italy",
        "germany",
        "united kingdom",
        "united states",
        "united arab emirates",
        "israel",
        "chile",
        "algeria",
        "pakistan",
        "india",
        "world",
    )
    df_filtered["shortlisted_countries"] = df_filtered["location"].map(
        lambda x: x
        if x.lower() in shortlisted_countries
        else " "  # Empty string will cause issues with plotly
    )

    # Drop / Fill NA
    x = "gdp_per_capita"
    y = "people_fully_vaccinated_per_hundred"
    df_filtered = df_filtered.dropna(subset=[x, y])
    df_filtered["continent"] = df_filtered["continent"].fillna("Unspecified")

    # Compute linear regression line
    # c, m = (
    #     T.fit(df_filtered["gdp_per_capita"], df_filtered["people_fully_vaccinated_per_hundred"], 1)
    #     .convert()
    #     .coef
    # )

    # Plot
    if len(df_filtered) > 0:
        fig = px.scatter(
            data_frame=df_filtered,
            x=x,
            y=y,
            color="continent",
            text="shortlisted_countries",
            opacity=0.6,
            hover_name="location",
            hover_data=["date"],
            trendline="ols",
            trendline_scope="overall",
            title="Vaccination Rate against GDP per Capita",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select another date")

    st.markdown("---")
    with st.expander("Debugging info"):
        st.subheader("DF: Raw")
        st.dataframe(df_raw.iloc[:100])
        st.subheader("DF: Date-filtered")
        st.dataframe(df.iloc[:100])
        st.subheader("DF: Filtered, cleaned")
        st.dataframe(df_filtered.iloc[:100])


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
