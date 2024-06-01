""" Change the country names in the time series files to match the owid data """

import filenames as fn
import re
import csv


def changeCountryNames():
    """ changes the country names in each time_series file and saves them
        as new files
    """
    PROVINCE_NAME_COL = 0
    COUNTRY_NAME_COL  = 1
    HONG_KONG         = "Hong Kong"

    CRUISE_SHIPS      = ["Diamond Princess", "MS Zaandam"]

    
    # index positions match between find_strings and replace_strings
    find_strings = [
        "Burma",              "Cabo Verde",          "Congo \(Brazzaville\)",   
        "Congo \(Kinshasa\)", "Holy See",            "Korea, South", 
        "Micronesia",         "Taiwan\*",            "Timor-Leste",
        "US",                 "West Bank and Gaza"
    ]

    replace_strings = [
        "Myanmar",                      "Cape Verde", "Congo",
        "Democratic Republic of Congo", "Vatican",    "South Korea",
        "Marshall Islands",             "Taiwan",     "Timor",
        "United States",                "Palestine"
    ]

    # Change Country Names
    for old_filename, new_filename in zip(fn.FILENAMES_OLD.values(), fn.FILENAMES_NEW.values()):
        with open(old_filename, "r") as old_csv:
            old_csv_text = old_csv.read()

        new_csv_text = old_csv_text
        for find_string, replace_string in zip(find_strings, replace_strings):
            new_csv_text = re.sub(find_string, replace_string, new_csv_text)

        with open(new_filename, "w") as new_csv:
            new_csv.write(new_csv_text)

    # Remove Cruise Ship Rows and Change China -> Hong Kong for correct line
    for new_filename in fn.FILENAMES_NEW.values():
        with open(new_filename, "r") as with_ships_csv:
            reader = csv.reader(with_ships_csv, delimiter=",")

            row_list = []
            for row in reader:
                if row[PROVINCE_NAME_COL] == HONG_KONG:
                    row[COUNTRY_NAME_COL] =  HONG_KONG  # Change Country China -> Hong Kong
                row_list.append(row)
                if row[COUNTRY_NAME_COL] in CRUISE_SHIPS:
                    row_list.remove(row)

        with open(new_filename, "w") as no_ships_csv:
            writer = csv.writer(no_ships_csv)
            writer.writerows(row_list)
