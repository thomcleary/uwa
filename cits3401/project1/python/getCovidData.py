""" Extract Covid Data from the listed xlsx and csv files """

import csv
import pandas as pd
import filenames as fn


def get_country_size_id(population):
    """ return countrySizeID for small, medium or large """

    country_size_ids = {
        "Small" : 1,
        "Medium" : 2,
        "Large" : 3
    }

    ONE_MILLION = 1000000

    population = int(population)

    if population >= 40 * ONE_MILLION: 
        return country_size_ids["Large"]

    if population <= 2 * ONE_MILLION:  
        return country_size_ids["Small"]

    return country_size_ids["Medium"]


def get_life_exp_id(life_exp):
    """ return life_exp_id of rounded down expectancy to closest multiple of 25 
        up to 75 
    """
    life_exp_ids = {
        "true" : 1,
        "false" : 2
    }

    if life_exp > 75:
        return life_exp_ids["true"]
        
    return life_exp_ids["false"]


def init_measures(owid_data):
    """ add time_series dates to measures_dict in data and initialise
        confirmed, deaths, recovered all to 0
    """
    dates = get_time_series_dates(fn.FILENAMES_NEW["confirmed"])

    for country in owid_data.keys():
        date_dict = {}
        for date in dates:
            date_dict[date] = [0, 0, 0]
        owid_data[country]["measures"] = date_dict


def get_owid_data(filename=fn.FILENAMES["owid.xlsx"]):
    """ get rows of (country, region, population, life_exp) from owid.xlsx """

    DATA_COLUMNS   = "B,C,AJ,AW" ##region,country,population,lifeExpectancy
    REGION_COL     = 0
    COUNTRY_COL    = 1
    POPULATION_COL = 2
    LIFE_EXP_COL   = 3

    data = {}

    try:
        owid_data = pd.read_pickle("owid_cached.pkl")
    except:
        owid_data = pd.read_excel(filename, usecols=DATA_COLUMNS)
        owid_data.to_pickle("owid_cached.pkl")

    location_id = 1

    for _, row in owid_data.iterrows():
        region  = row[REGION_COL]
        
        if not isinstance(region, str): # if country does not have region world,international
            continue

        region  = region.strip()
        country = row[COUNTRY_COL].strip()

        if country not in data.keys():
            data[country] = {
                "location_id"       : location_id,
                "region"            : region,
                "country_size_id"   : get_country_size_id(row[POPULATION_COL]),
                "life_exp_id"       : get_life_exp_id(row[LIFE_EXP_COL]),
                "measures"          : {}
                # Dictionary of (key, month, quarter, year) : [confirmed, deaths, recovered]
            }
            location_id += 1

    init_measures(data)

    return data


def get_quarter(month_num):
    """ returns the quarter that month is in for the year """
    return (month_num + 2) // 3


def get_time_series_dates(time_series_filename):
    """ returns list of (dateid, monthName, quarterNum, yearNum) values
        (requires filename arg for comparing dates in multiple files)
    """

    DATE_START_COL = 4

    # All files have 405 dates for slice [DATE_START_COL:]
    # Tested that all dates are the same between the files so can use any one file
    with open(time_series_filename, "r") as csv_confirmed:

        dates = list(csv.reader(csv_confirmed, delimiter=","))[0][DATE_START_COL:]

        month_quarter_year_dates = []

        for date in dates:
            split_date = date.strip().split("/")

            month_quarter_year = [
                int(split_date[0]),
                get_quarter(int(split_date[0])),
                int("20" + split_date[2])
            ]

            if month_quarter_year not in month_quarter_year_dates:
                month_quarter_year_dates.append(month_quarter_year)


        # add date_id to each date
        for index, date in enumerate(month_quarter_year_dates):
            date.insert(0, index+1) # insert DateID
            month_quarter_year_dates[index] = tuple(date) # so they can be a key in a dictionary

        return month_quarter_year_dates


def date_to_key(date, key_value):
    """ turns mm/dd/yy into (dateid, monthName, quarter, year) tuple """
    split_date = date.strip().split("/")

    return tuple([
        key_value,
        get_month_num(date),
        get_quarter(int(split_date[0])),
        int("20" + split_date[2])
    ])


def get_month_num(date):
    """ return month name of mm/dd/yy string date """
    return int(date.strip().split("/")[0])


def validate_measure(measure):
    """ returns integer of absolute value of measure else returns 0 """
    try:
        return int(measure)
    except:
        raise ValueError("Could not convert {} to an int".format(measure))


def insert_time_series_data(data_dict, filename, measure_type):
    """ returns dictionary from get_owid_data() with measures : {} filled for
        each country
    """
    HEADER_ROW     = 0
    DATA_START_ROW = 1

    COUNTRY_COL    = 1
    DATE_START_COL = 4

    LOTS_OF_CASES  = 1000

    MEASURES       = "measures"

    measure_types = {
        "confirmed" : 0,
        "deaths"    : 1,
        "recovered" : 2
    }

    meausure_index = measure_types[measure_type]

    # start from here
    with open(filename, "r") as csv_file:
        rows = list(csv.reader(csv_file, delimiter=","))

        dates = rows[HEADER_ROW][DATE_START_COL:]
        data  = rows[DATA_START_ROW:]

        for row in data:
            country = row[COUNTRY_COL]

            date_id = 1
            date_index = 0
            date_key = date_to_key(dates[date_index], date_id)
            previous_date_month = date_key[1]

            previous_month_total = 0
            last_non_zero_day_total = 0
            month_total = 0

            stopped_reporting = False
     
            for measure in row[DATE_START_COL:]:

                # if we have moved to the next month in a row, add 1 to date_id
                month = get_month_num(dates[date_index])
                if month != previous_date_month:
                    
                    # if the measures have changed to 0s eg 0,0,0,...
                    if month_total - previous_month_total == -previous_month_total:
                        # if we have already seen a significant value it is 
                        # probably not correction
                        if previous_month_total > LOTS_OF_CASES:
                            month_total = last_non_zero_day_total

                            # We have hit the point where the country has stopped reporting
                            # Can stop adding values after this one
                            data_dict[country][MEASURES][date_key][meausure_index] += (month_total - previous_month_total)
                            stopped_reporting = True
                            break

                    data_dict[country][MEASURES][date_key][meausure_index] += (month_total - previous_month_total)

                    date_id    += 1
                    previous_date_month = month
                    previous_month_total = month_total
                    month_total = 0 # will stay 0 if country stopped reporting

                    date_key = date_to_key(dates[date_index], date_id)         


                measure = validate_measure(measure)

                if month_total != 0:
                    last_non_zero_day_total = month_total

                month_total += (measure - month_total)

                date_index += 1

            if not stopped_reporting:
                # add measure to the last month
                data_dict[country][MEASURES][date_key][meausure_index] += (month_total - previous_month_total)


def add_data_to_dictionary(data_dict):
    """ add the time series data to the dictionary """
    insert_time_series_data(data_dict, fn.FILENAMES_NEW["confirmed"], "confirmed")
    insert_time_series_data(data_dict, fn.FILENAMES_NEW["deaths"], "deaths")
    insert_time_series_data(data_dict, fn.FILENAMES_NEW["recovered"], "recovered")


def get_covid_data():
    data = get_owid_data(fn.FILENAMES["owid.xlsx"])
    add_data_to_dictionary(data)
    return data


def main():
    """ testing """
    data = get_owid_data(fn.FILENAMES["owid.xlsx"])
    add_data_to_dictionary(data)
    print(data["United States"]["measures"][(15, 3, 1, 2021)])


if __name__ == "__main__":
    main()
