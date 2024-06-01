""" Writes the covid data related to dimension tables,
    extracted in getCovidData.py,
    to csv files for the tables in CovidDW
"""

import getCovidData as gcd
import filenames as fn

FOLDER = "csvFilesWindows/"


def write_dim_location_csv():
    """ DimLocation.csv (LocationID, Country, Region) """

    OWID_FILENAME = fn.FILENAMES["owid.xlsx"]

    covid_data = gcd.get_owid_data(OWID_FILENAME)
    countries = covid_data.keys()

    lines = []

    for country in countries:
        location_id = covid_data[country]["location_id"]
        region      = covid_data[country]["region"]

        line = "{},{},{}\n".format(location_id, country, region)
        lines.append(line)

    write_lines(lines, FOLDER + "DimLocation.csv")


def write_dim_time_csv():
    """ DimTime.csv (TimeID, Month, Quarter, Year) """

    dates = gcd.get_time_series_dates(fn.FILENAMES_NEW["confirmed"])

    lines = []
    for date in dates:
        line = "{},{},{},{}\n".format(date[0], date[1], date[2], date[3])
        lines.append(line)

    write_lines(lines, FOLDER + "DimTime.csv")


def write_dim_country_size_csv():
    """ DimCountrySize (CountrySizeID, SizeType) """
    sizes = ["Small", "Medium", "Large"]
    lines = ["{},{}\n".format(key, size) for key, size in zip(range(1, len(sizes)+1), sizes)]

    write_lines(lines, FOLDER + "DimCountrySize.csv")


def write_dim_life_expectancy_csv():
    """ DimLifeExpectancy (LifeExpectancyID, GreaterThanAge) """
    values = ["true", "false"]

    lines = ["{},{}\n".format(key, value) for key, value in zip(range(1, len(values)+1), values)]
    write_lines(lines, FOLDER + "DimLifeExpectancy.csv")


def write_lines(lines, out_file):
    """ write list of strings to outfile """
    with open(out_file, "w") as new_file:
        for line in lines:
            new_file.write(line)


def main():
    """ call functions to write csv files """
    write_dim_life_expectancy_csv()
    write_dim_country_size_csv()
    write_dim_location_csv()
    write_dim_time_csv()


if __name__ == "__main__":
    main()
