"""
Zach Koverman
CSE 163 AE
6/2/22
Calls functions from dataset_processing.py and mapping.py to create
interactive choropleth maps with the plotly library. Processes datasets with
data on graduation rates, college enrollment, and geometry data for Washington
counties and merges them using functions from dataset_processing.py. Plots,
saves, and shows the maps using the function from mapping.py
"""

import dataset_processing as zdp
import mapping as zmap


def main():
    # Processing datasets
    df_grad = zdp.process_grad_rates("Documents/Graduation_Rates_14_20.csv")
    df_enroll = zdp.process_enrollment("Documents/HS_College_Enrollment.csv")
    gdf_counties = zdp.process_shapefile("Documents/WA_County_Bndys/"
                                         "WA_County_Bndys.shp")

    # Creating GeoDataFrame for mapping, plotting, and saving maps
    merged_df = zdp.create_mapping_df(df_grad, df_enroll, gdf_counties)
    zmap.plot_rates_maps(merged_df, show_maps=True)


if __name__ == "__main__":
    main()
