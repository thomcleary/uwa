""" functions to compare country names in owid data and time series data """

import getCovidData as gcd
import editTimeSeriesFiles as etsf
import filenames as fn
import csv


def get_owid_countries():
    """ returns list of countries in owid data """
    return gcd.get_owid_data().keys()


def get_time_series_countries(time_series_file):
    """ returns list of countries in time series files """
    COUNTRY_NAME_COL = 1

    with open(time_series_file, "r") as ts_csv:
        rows = list(csv.reader(ts_csv, delimiter=","))

    country_names = []
    for row in rows[1:]:  # skip header
        country = row[COUNTRY_NAME_COL].strip()

        if country not in country_names:
            country_names.append(country)

    return country_names


def compare_time_series_countries():
    """ raises assertion error if country names are different between any of the time
        series files
    """
    name_sets = []
    for filename in fn.FILENAMES_OLD.values():
        name_sets.append(set(get_time_series_countries(filename)))

    for index, name_set in enumerate(name_sets):
        for j in range(index+1, len(name_sets)):
            assert name_set == name_sets[j]


def compare_owid_time_series_countries(time_series="original"):
    """ returns true if countries are the same between owid and time series,
        else false
    """
    if time_series == "original":
        time_series_file = fn.FILENAMES["confirmed"] # all the same so any will do
    elif time_series == "edited":
        time_series_file = fn.FILENAMES_NEW["confirmed"]
    else:
        raise ValueError("time_series: 'original', 'edited'")

    return set(get_owid_countries()) == set(get_time_series_countries(time_series_file))


def get_missing_countries(return_missing, compare_against):
    missing = []
    for name in return_missing:
        if name not in compare_against and name not in missing:
            missing.append(name)

    return missing


def create_country_diff_txt():
    """ creates a txt file listing the countries that are not present in the
        opposite file
    """
    time_series_file = fn.FILENAMES["confirmed"] # all the same so any will do
    
    owid_names = get_owid_countries()
    time_series_names = get_time_series_countries(time_series_file)

    owid_missing = get_missing_countries(owid_names, time_series_names)
    time_series_missing = get_missing_countries(time_series_names, owid_names)

    with open("txtFiles/missing_country_names.txt", "w") as text_file:
        text_file.write("-"*80 + "\n")
        text_file.write("OWID Country Names\n")
        text_file.write("-"*80 + "\n")
        for name in owid_missing:
            text_file.write("{}\n".format(name))
        text_file.write("-"*80 + "\n")

        text_file.write("TimeSeries Country Names\n")
        text_file.write("-"*80 + "\n")
        for name in time_series_missing:
            text_file.write("{}\n".format(name))
        text_file.write("-"*80 + "\n")



def main():
    compare_time_series_countries()
    # if no assertion raised timeseries share same country names

    same = compare_owid_time_series_countries()
    if not same:
        print("--- OWID and Time Series Country Names differ.")
        create_country_diff_txt()
        print("--- Country difference list created.")
        etsf.changeCountryNames()
        print("--- Time Series files edited.")

    # compare new time series to owid
    same = compare_owid_time_series_countries(time_series="edited")
    if same:
        print("--- OWID and Time Series Country Names now match.")
    else:
        print("--- OWID and Time Series Names still differ.")



if __name__ == "__main__":
    main()
