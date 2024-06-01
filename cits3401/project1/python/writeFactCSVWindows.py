import getCovidData as gcd
import writeDimCSVsWindows as wdc

""" Writes the covid data related to the fact table,
    extracted from the time series csv files,
    to csv files for the fact table in CovidDW
"""

FOLDER = "csvFilesWindows/"

def write_fact_covid_data_csv():
    """ FactCovidData.csv
    (,DateID,LocationID,CountrySizeID,LifeExpectancyID,ConfirmedCases,Deaths,Recoveries)
    """
    MEASURES      = "measures"
    DATE_ID_IDX   = 0
    CONFIRMED_IDX = 0
    DEATHS_IDX    = 1
    RECOVERED_IDX = 2

    covid_data = gcd.get_covid_data()
    countries = covid_data.keys()

    lines = []

    for country in countries:
        country_data = covid_data[country]
        measure_data = country_data[MEASURES]

        for date_key in measure_data.keys():
            date_id         = date_key[DATE_ID_IDX]
            location_id     = country_data["location_id"]
            country_size_id = country_data["country_size_id"]
            life_exp_id     = country_data["life_exp_id"]
            confirmed       = measure_data[date_key][CONFIRMED_IDX]
            deaths          = measure_data[date_key][DEATHS_IDX]
            recovered       = measure_data[date_key][RECOVERED_IDX]

            line = ",{},{},{},{},{},{},{}\n".format(
                date_id,
                location_id,
                country_size_id,
                life_exp_id,
                confirmed,
                deaths,
                recovered)

            lines.append(line)

    wdc.write_lines(lines, FOLDER + "FactCovidData.csv")


def main():
    write_fact_covid_data_csv()


if __name__ == "__main__":
    main()