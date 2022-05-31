import geopandas as gpd

def main():
    # make counties map
    counties = gpd.read_file("Documents/WA_County_Bndys/WA_County_Bndys.shp")
    print(counties.columns)
    """counties.plot()
    plt.savefig("washingtdon_map.png")"""
    
    
if __name__ == "__main__":
    main()