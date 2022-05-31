"""
Zach Koverman
CSE 163 AE
6/2/22
This module defines a function that creates interactive choropleth maps of
education outcomes by county in Washington state using the python library
plotly. Maps are saved as html files and can be opened in a web browser.
"""

import plotly.express as px
import json


def plot_rates_maps(gdf, show_maps=True):
    """
    Saves five html files containing interactive maps of Washington state,
    showing the average rates for which students in each county in the 2008
    through 2012 seven-year cohorts dropped out of high school, graduated high
    school, did not enroll in college, enrolled in a 2-year / community or
    technical college, and enrolled in a 4-year college. If bool show_maps is
    True, then the function also shows each map in its own web browser tab.
    """
    # Getting a json file with data for mapping counties in the United States
    with open("Documents/geojson-counties-fips.json") as f:
        counties = json.load(f)

    # Dropout Rates
    fig_drop = px.choropleth_mapbox(gdf, geojson=counties,
                                    locations="County FIPS Code",
                                    color="Dropout Rate",
                                    center={"lat": 47.38695210127829,
                                            "lon": -120.52247111357288},
                                    mapbox_style="open-street-map",
                                    hover_name="JURISDIC_2",
                                    title="Average High School Dropout Rate "
                                          "by County in Washington, 7-Year "
                                          "Cohorts2008 through 2012",
                                    color_continuous_scale="plasma",
                                    opacity=.75,
                                    zoom=5.5)

    # HS Graduation Rates
    fig_grad = px.choropleth_mapbox(gdf, geojson=counties,
                                    locations="County FIPS Code",
                                    color="HS Graduation Rate",
                                    center={"lat": 47.38695210127829,
                                            "lon": -120.52247111357288},
                                    mapbox_style="open-street-map",
                                    hover_name="JURISDIC_2",
                                    title="Average High School Graduation "
                                          "Rate by County in Washington, "
                                          "7-Year Cohorts 2008 through 2012",
                                    color_continuous_scale="plasma",
                                    opacity=.75,
                                    zoom=5.5)

    # Not Enrolled in College Rates
    fig_stop = px.choropleth_mapbox(gdf, geojson=counties,
                                    locations="County FIPS Code",
                                    color="Not Enrolled in College Rate",
                                    center={"lat": 47.38695210127829,
                                            "lon": -120.52247111357288},
                                    mapbox_style="open-street-map",
                                    hover_name="JURISDIC_2",
                                    title="Average Rate of High School "
                                          "Graduates Not Enrolling in College"
                                          " by County in Washington, 7-Year "
                                          "Cohorts 2008 through 2012",
                                    color_continuous_scale="plasma",
                                    opacity=.75,
                                    zoom=5.5)

    # 2-Year / CTC Rates
    fig_2yr = px.choropleth_mapbox(gdf, geojson=counties,
                                   locations="County FIPS Code",
                                   color="2-Year / CTC Rate",
                                   center={"lat": 47.38695210127829,
                                           "lon": -120.52247111357288},
                                   mapbox_style="open-street-map",
                                   hover_name="JURISDIC_2",
                                   title="Average Rate of Enrollment in "
                                         "2-Year / CTC by County in "
                                         "Washington, 7-Year Cohorts 2008 "
                                         "through 2012",
                                   color_continuous_scale="plasma",
                                   opacity=.75,
                                   zoom=5.5)

    # 4-Year Rates
    fig_4yr = px.choropleth_mapbox(gdf, geojson=counties,
                                   locations="County FIPS Code",
                                   color="4-Year Rate",
                                   center={"lat": 47.38695210127829,
                                           "lon": -120.52247111357288},
                                   mapbox_style="open-street-map",
                                   hover_name="JURISDIC_2",
                                   title="Average Rate of Enrollment in "
                                         "4-Year Colleges by County in "
                                         "Washington, 7-Year Cohorts 2008 "
                                         "through 2012",
                                   color_continuous_scale="plasma",
                                   opacity=.75,
                                   zoom=5.5)

    # Saving
    fig_drop.write_html("Documents/Interactive_Maps/"
                        "map_dropout_rates.html")
    fig_grad.write_html("Documents/Interactive_Maps/"
                        "map_hs_graduation_rates.html")
    fig_stop.write_html("Documents/Interactive_Maps/"
                        "map_enrolled_college_rates.html")
    fig_2yr.write_html("Documents/Interactive_Maps/map_2yr_ctc_rates.html")
    fig_4yr.write_html("Documents/Interactive_Maps/map_4yr_rates.html")

    # Showing maps if desired
    if show_maps:
        fig_drop.show()
        fig_grad.show()
        fig_stop.show()
        fig_2yr.show()
        fig_4yr.show()
