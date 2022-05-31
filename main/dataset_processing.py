"""
Zach Koverman
CSE 163 AE
6/2/22
This module defines functions used to process and merge datasets so that they
can be easily used to create interactive maps about high school education
outcomes for cohorts that started high school in the years 2008 through 2012.
The main tasks of these functions are taking CSV files, trimming off
unnecessary rows and columns, and returning DataFrames. Another merges
DataFrames, reformats the data, and creates a GeoDataFrame.
"""

import pandas as pd
import geopandas as gpd


def process_grad_rates(file_path):
    """
    Returns a DataFrame containing important data on high school education
    outcomes given a CSV file_path. The returned DataFrame contains county
    data on dropout and graduation rates for groups of all students with
    corresponding school years. This only includes at data for seven-year
    cohorts, which include all students who started high school at the same
    time who finished in seven years or less. Rows without seven-year cohort
    data as well as pandemic years are removed from the DataFrame.
    """
    df = pd.read_csv(file_path, low_memory=False)

    # Filtering and trimming columns
    df = df.loc[:, ["SchoolYear", "OrganizationLevel", "County",
                    "StudentGroup", "Cohort", "Dropout", "GraduationRate"]]
    is_by_county = df["OrganizationLevel"] == "County"
    is_all_students = df["StudentGroup"] == "All Students"
    is_7_year = df["Cohort"].apply(str.lower) == "seven year"
    is_selected_years = ~((df["SchoolYear"] == "2019-20") |
                          (df["SchoolYear"] == "2020-21"))

    # Applying filters and finalizing
    df = df[is_by_county & is_all_students & is_7_year & is_selected_years]
    df = df.dropna()
    return df


def process_enrollment(file_path):
    """
    Returns a DataFrame containing important data on college enrollment
    given a CSV file_path. The returned DataFrame contains county data on
    percentages of all high school graduates in each cohort either who did not
    enroll in college, enrolled in a 2-year / community or technical college,
    or enrolled in a 4-year college after graduating. This DataFrame only
    includes data on 2008 through 2012 cohorts so as to match the years with
    data available in the high school outcomes dataset.
    """
    df = pd.read_csv(file_path, low_memory=False)

    # Filtering and trimming columns
    df = df.loc[:, ["CohortYearTTL", "DistrictType", "DistrictTTL",
                    "DemographicGroup", "PSEnrollLevel", "Pct"]]
    is_selected_years = (df["CohortYearTTL"] >= 2008) & \
        (df["CohortYearTTL"] <= 2012)
    is_all_students = df["DemographicGroup"] == "All Students"
    is_county = df["DistrictType"] == "County"

    # Applying filters and finalizing
    df = df[is_selected_years & is_all_students & is_county]
    df = df.dropna()
    return df


def process_shapefile(shapefile_path):
    """
    Returns a GeoDataFrame containing data from a given shapefile
    shapefile_path.
    """
    gdf = gpd.read_file(shapefile_path)
    return gdf


def create_mapping_df(grad, enrollment, geo):
    """
    Returns a GeoDataFrame containing data from DataFrames and a GeoDataFrame
    that have already been processed to contain the desired education
    outcomes columns. Takes DataFrames grad and enrollment and GeoDataFrame
    geo. Make columns for each type of outcome in enrollment and renames
    some columns to improve readability of graphs. Merges the DataFrames and
    geo, ensuring that only entries from each with matching cohorts are kept.
    Returned GeoDataFrame has only columns that are necessary for mapping
    education outcomes.
    """
    # Merging the graduation rates and enrollment datasets
    merged_edu = grad.merge(enrollment, left_on="County",
                            right_on="DistrictTTL", how="inner")

    # Trimming down so years from enrollment matches years from grad rates
    merged_edu["SchoolYear_adj"] = \
        merged_edu["SchoolYear"].apply(lambda y: int(y[-2:]))
    merged_edu["CohortYearTTL_adj"] = \
        merged_edu["CohortYearTTL"].apply(lambda y: y % 2000)
    is_corresponding_year = (merged_edu["SchoolYear_adj"] -
                             merged_edu["CohortYearTTL_adj"]) == 7
    merged_edu = merged_edu[is_corresponding_year].reset_index()

    # Putting enrollment rates into their own columns
    is_only_ctc = merged_edu["PSEnrollLevel"] == "2 Year / CTC"
    temp_df = merged_edu[is_only_ctc]
    merged_edu["2-Year / CTC Rate"] = temp_df["Pct"]

    is_only_4year = merged_edu["PSEnrollLevel"] == "4 Year"
    temp_df = merged_edu[is_only_4year]
    merged_edu["4-Year Rate"] = temp_df["Pct"]

    is_not_enrolled = merged_edu["PSEnrollLevel"] == "Not Enrolled"
    temp_df = merged_edu[is_not_enrolled]
    merged_edu["Not Enrolled in College Rate"] = temp_df["Pct"]

    # Creating DataFrame with enrollment in better format, only needed columns
    desired_cols = ["CohortYearTTL", "DistrictType", "County", "StudentGroup",
                    "Cohort", "Dropout", "GraduationRate",
                    "2-Year / CTC Rate", "4-Year Rate",
                    "Not Enrolled in College Rate"]
    merged_edu = merged_edu.loc[:, desired_cols]
    merged_edu = merged_edu.groupby("County", as_index=False).mean()

    # Merging resulting dataframe with shape file
    final = merged_edu.merge(geo, how="inner",
                             right_on="JURISDIC_1", left_on="County")
    final = final.rename(columns={"JURISDIC_4": "County FIPS Code",
                                  "Dropout": "Dropout Rate",
                                  "GraduationRate": "HS Graduation Rate"})
    return final
