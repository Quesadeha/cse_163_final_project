from platform import machine
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def filter_student_group(grad_data, student_group):
    """
    Filters and returns a DataFrame by StudentGroup, grouped by county
    Assumes that the given DataFrames are derived from Graduation_Rates_14_20.csv
    """
    grad_sg = grad_data[grad_data["StudentGroup"] == student_group]
    return grad_sg.groupby("County")["GraduationRate"].mean()
    

def plot_student_group(geometry, student_groups, title, filename):
    """
    Saves a plot of graduation rates from a student group on a map of Washington state
    - working to implement it for "StudentGroup" and "NonStudentGroup" on the same fig
    """
    fig, axs = plt.subplots(2)
    
    student_groups[0] = geometry.merge(student_groups[0], how="outer", left_on="JURISDIC_1", right_on="County")
    geometry.plot(ax=axs[0], color="#ACACAC")
    student_groups[0].plot(column="GraduationRate", legend=True, ax=axs[0]) #, legend_kwds={"shrink": 0.7} isn't working
    axs[0].axis("off")
    axs[0].set_title("Graduation rates of " + title + " by county")
    
    student_groups[1] = geometry.merge(student_groups[1], how="outer", left_on="JURISDIC_1", right_on="County")
    geometry.plot(ax=axs[1], color="#ACACAC")
    student_groups[1].plot(column="GraduationRate", legend=True, ax=axs[1])
    axs[1].axis("off")
    axs[1].set_title("Graduation rates of " + title + " by county") # MAKE THIS ACCURATE
    plt.savefig(filename + "_by_county.png")       


def main():
    # GeoDataFrame for WA counties
    wa_counties = gpd.read_file("Documents/WA_County_Bndys/WA_County_Bndys.shp")
    
    # Process graduation data for analysis
    hs_grad = pd.read_csv("Documents/Graduation_Rates_14_20.csv")
    # Eliminates irrelevant columns
    hs_grad = hs_grad[["SchoolYear", "County", "StudentGroupType", "StudentGroup", "Cohort", "GraduationRate"]]
    # Filters to selected years
    hs_grad = hs_grad[((hs_grad["SchoolYear"] == "2014-15") |
                      (hs_grad["SchoolYear"] == "2015-16") |
                      (hs_grad["SchoolYear"] == "2016-17") |
                      (hs_grad["SchoolYear"] == "2017-18") |
                      (hs_grad["SchoolYear"] == "2018-19")) &
                      (hs_grad["Cohort"].apply(str.lower) == "seven year")]
    
    # Data categorized according to 504 and SPED statuses
    grad_accomm = hs_grad[(hs_grad["StudentGroupType"] == "504") | (hs_grad["StudentGroupType"] == "sped") | (hs_grad["StudentGroupType"] == "ELL")]
    
    """[("Section 504", "504 students", "504"), ("Non Section 504", "non-504 students", "non_504"), 
     ("Students with Disabilities", "SPED students", "sped"), ("Students without Disabilities", "non-SPED students", "non_sped"), 
     ("English Language Learners", "ELL students", "ell"), ("Non-English Language Learners", "non-ELL students", "non_ell")]"""
    
    grad_504 = filter_student_group(grad_accomm, "Section 504")
    grad_non_504 = filter_student_group(grad_accomm, "Non Section 504")
    grad_sped = filter_student_group(grad_accomm, "Students with Disabilities")
    grad_non_sped = filter_student_group(grad_accomm, "Students without Disabilities")
    grad_ell = filter_student_group(grad_accomm, "English Language Learners")
    grad_non_ell = filter_student_group(grad_accomm, "Non-English Language Learners")
    
    plot_student_group(wa_counties, [grad_504, grad_non_504], "504 students", "504")
    #plot_student_group(wa_counties, grad_504, "non-504 students", "non_504")
    plot_student_group(wa_counties, [grad_sped, grad_non_sped], "disabled students (SPED)", "sped")
    #plot_student_group(wa_counties, grad_504, "non-SPED students", "non_sped")
    plot_student_group(wa_counties, [grad_ell, grad_non_ell], "English-learning students (ELL)", "ell") #revise phrasing here
    #plot_student_group(wa_counties, grad_504, "English-speaking students", "non_ell")

    print("<<MY LORD, IT IS DONE>>")


if __name__=="__main__":
    main()