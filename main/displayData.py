import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

"""
This file displays all the graphs for specific data for each
county in Washington State. The data from the Report Card Graduation
Rates 2014 - 2020 csv file from Data.WA.gov is being used. All of the
graphs look at school years 2014-15 to 2018-19, Cohort 7, and a range
of StudentGroupTypes and StudentGroups.

The only columns analyzed are...
SchoolYear [ex. 2014-15]
County [ex. Stevens, King]
StudentGroupType [ex. Race, LowIncome, Gender]
StudentGroup [ex. White, Asian, Female, Male, Low-Income, Non-Low Income]
Cohort [ex. Seven Year]
GraduationRate [ex. 0.82]
Dropout [ex. 0.2]
"""


def by_county(data, student_group_type):
    """
    A method that filters the data from the Report Card Graduation
    Rates 2014 - 2020 csv file from Data.WA.gov by the given student_type.
    The average graduation rate is taken from the years 2014-2019 for
    Cohort 7.
    """
    counties = data[['SchoolYear', 'County', 'StudentGroupType',
                     'StudentGroup', 'Cohort', 'GraduationRate']]
    counties = counties[(((counties['SchoolYear'] == '2014-15') |
                          (counties['SchoolYear'] == '2015-16') |
                          (counties['SchoolYear'] == '2016-17') |
                          (counties['SchoolYear'] == '2017-18') |
                          (counties['SchoolYear'] == '2018-19')) &
                         (counties['StudentGroupType'] == student_group_type) &
                         (counties['Cohort'].apply(str.lower) ==
                          'seven year'))]
    counties = counties.groupby(['County', 'StudentGroup'],
                                as_index=False).mean()
    return counties


def grad_or_drop_by_county(data):
    """
    A method that filters the data from the Report Card Graduation
    Rates 2014 - 2020 csv file from Data.WA.gov, by all students that
    either graduate or drop out. The average graduation rate is taken
    from the years 2014-2019 for Cohort 7.
    """
    counties = data[['SchoolYear', 'County', 'StudentGroupType',
                     'StudentGroup', 'Cohort', 'GraduationRate', 'Dropout']]
    counties = counties[(((counties['SchoolYear'] == '2014-15') |
                          (counties['SchoolYear'] == '2015-16') |
                          (counties['SchoolYear'] == '2016-17') |
                          (counties['SchoolYear'] == '2017-18') |
                          (counties['SchoolYear'] == '2018-19')) &
                         (counties['StudentGroupType'] == 'All') &
                         (counties['Cohort'].apply(str.lower) ==
                          'seven year'))]
    counties = counties.groupby(['County', 'StudentGroup'],
                                as_index=False).mean()
    return counties


def plot_map(state_bounds):
    """
    Map that plots the Washington State County map,
    used for reference.
    """
    state_bounds.plot()
    plt.title('Washington State Counties')
    plt.savefig('CountyMap.png')


def plot_rate(data, grad_type):
    """
    Method that either plots the average graduation rate from 2014-2019
    for each county or the average dropout rate from 2014-2019 for each
    county.
    """
    if(grad_type == 'GraduationRate'):
        group = 'Graduate'
    else:
        group = 'Drop Out'
    fig, ax = plt.subplots(1)
    ax.axis('off')
    data.plot(color='#8C8C8C', ax=ax, edgecolor="black", linewidth=0.7)
    data.plot(column=grad_type, legend=True, ax=ax,
              legend_kwds={'orientation': 'horizontal',
                           'label': 'Percentage of All Students to \
                               ' + group + ' (Gray = Missing Data)'},
              edgecolor="black", linewidth=0.7)
    plt.title('Washington ' + group + ' Rates by County',
              fontsize=15, fontweight='bold')
    plt.savefig(group + '_map.png')


def plot_student_group(data, student_group_type):
    """
    Method that takes a merged dataframe and a specified student
    group type and graphs that group's average graduation rate
    from 2014-2019.
    """
    data = data[data['StudentGroup'] == student_group_type]
    fig, ax = plt.subplots(1)
    ax.axis('off')
    data.plot(color='#8C8C8C', ax=ax, edgecolor="black", linewidth=0.7)
    data.plot(column='GraduationRate', legend=True, ax=ax, vmin=0.3, vmax=0.9,
              legend_kwds={'orientation': 'horizontal',
                           'label': 'Percentage of Students to Graduate \
                               (Gray = Missing Data)'},
              edgecolor="black", linewidth=0.7)
    plt.title('Washington ' + student_group_type +
              ' \nGraduation Rates by County', fontsize=12,
              fontweight='bold')

    if(student_group_type == 'Native Hawaiian/ Other Pacific Islander'):
        plt.savefig('HawaiianOrPacificIslander_map.png')
    elif(student_group_type == 'Black/ African American'):
        plt.savefig('BlackOrAfricanAmerican.png')
    elif(student_group_type == 'Hispanic/ Latino of any race(s)'):
        plt.savefig('HispanicOrLatino.png')
    else:
        plt.savefig(student_group_type + '_map.png')


def main():
    # DataFrame for the Report Card file from 2014-2020
    grad_rates = pd.read_csv('Documents/Graduation_Rates_14_20.csv',
                             low_memory=False)
    # GeoDataFrame for the Washington county shape file
    wa_bounds = gpd.read_file('Documents/WA_County_Bndys/WA_County_Bndys.shp')

    # Filtered DataFrames by a specified StudentGroupType
    gender_by_county = by_county(grad_rates, 'Gender')
    income_by_county = by_county(grad_rates, 'LowIncome')
    race_by_county = by_county(grad_rates, 'Race')

    # Filtered DataFrame for All Students, shows GraduationRate and Dropout
    rates_by_county = grad_or_drop_by_county(grad_rates)

    # Merged GeoDataFrames, with a specified filtered DataFrame and the
    #   Washington State County Shape GeoDataFrame
    gender_merge = wa_bounds.merge(gender_by_county, left_on='JURISDIC_1',
                                   right_on='County', how='left')
    income_merge = wa_bounds.merge(income_by_county, left_on='JURISDIC_1',
                                   right_on='County', how='left')
    race_merge = wa_bounds.merge(race_by_county, left_on='JURISDIC_1',
                                 right_on='County', how='left')
    rates_merge = wa_bounds.merge(rates_by_county, left_on='JURISDIC_1',
                                  right_on='County', how='left')

    # Plots the Washington State County Map
    plot_map(wa_bounds)

    # Plots all the specified Student Groups with the according merged
    #   GeoDataFrame
    plot_student_group(gender_merge, 'Female')
    plot_student_group(gender_merge, 'Male')
    plot_student_group(income_merge, 'Non-Low Income')
    plot_student_group(income_merge, 'Low-Income')
    plot_student_group(race_merge, 'Asian')
    plot_student_group(race_merge, 'Black/ African American')
    plot_student_group(race_merge, 'Hispanic/ Latino of any race(s)')
    plot_student_group(race_merge, 'Native Hawaiian/ Other Pacific Islander')
    plot_student_group(race_merge, 'Two or More Races')
    plot_student_group(race_merge, 'White')

    # Plots the Graduation Rate and Dropout Rate for all students
    plot_rate(rates_merge, 'GraduationRate')
    plot_rate(rates_merge, 'Dropout')


if __name__ == '__main__':
    main()
