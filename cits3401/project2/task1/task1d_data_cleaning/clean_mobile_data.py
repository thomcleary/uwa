import csv

MOBILE_PRICE_CSV = "../../provided_data_files/mobile_price.csv"
INCONSISTENT_TXT = "./inconsistencies.txt"
CLEAN_CSV = "./cleaned_mobile_data.csv"


def get_mobile_price_data(mobile_csv_file):
    """ return a list of rows from csv_file """

    with open(mobile_csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        return list(csv_reader)

###############################################################################
# Cleaning Functions
###############################################################################

def clean_yes_no(data):
    data_lower = data.lower()

    if data_lower in ["no", "not"]:
        return "no"
    else:
        return "yes"


def clean_binary(data):
    if data == "1":
        return "yes"
    return "no"


def to_float(data):
    return data + ".0"


def clean_blue(data, inconsistencies):
    if data in inconsistencies:
        return clean_yes_no(data)
    return data


def clean_clock_speed(data, inconsistencies):
    if data in inconsistencies:
        return to_float(data)
    return data


def clean_dual_sim(data, inconsistencies):
    if data in inconsistencies:
        return clean_yes_no(data)
    return data


def clean_four_g(data):
    return clean_binary(data)


def clean_m_dep(data, inconsistencies):
    if data in inconsistencies:
        return to_float(data)
    return data

def clean_three_g(data, inconsistencies):
    if data in inconsistencies:
        return clean_yes_no(data)
    return data

def clean_touch_screen(data):
    return clean_binary(data)

def clean_wifi(data, inconsistencies):
    if data in inconsistencies:
        return clean_yes_no(data)
    return data

def clean_price_category(data):
    if data == "1":
        return "high"
    else:
        return "not_high"



###############################################################################



def get_inconsistent_data(inconsistent_file):

    inconsistencies = {}

    with open(inconsistent_file, "r") as txt_file:

        current_col = ''

        for line in txt_file:
            if line[0] == "#":
                continue
            
            elif line[:6] == "Column":
                col_name = line.split()[-1]
                current_col = col_name
                inconsistencies[current_col] = []

            else:
                line = line.strip()
                inconsistencies[current_col].append(line)

    return inconsistencies



def clean_data(data, inconsistencies):
    col_names = data[0]

    inconsistent_cols = list(inconsistencies.keys())

    binary_cols = ["four_g", "touch_screen", "price_category"]

    inconsistent_cols += binary_cols

    new_rows = [col_names]

    for row in data[1:]:
        for index, data in enumerate(row):
            col_name = col_names[index]

            if col_name in inconsistent_cols:
                if col_name   == "blue":
                    cleaned_data = clean_blue(data, inconsistencies[col_name])

                elif col_name == "clock_speed":
                    cleaned_data = clean_clock_speed(data, inconsistencies[col_name])

                elif col_name == "dual_sim":
                    cleaned_data = clean_dual_sim(data, inconsistencies[col_name])

                elif col_name == "four_g":
                    cleaned_data = clean_four_g(data)

                elif col_name == "m_dep":
                    cleaned_data = clean_m_dep(data, inconsistencies[col_name])

                elif col_name == "three_g":
                    cleaned_data = clean_three_g(data, inconsistencies[col_name])

                elif col_name == "touch_screen":
                    cleaned_data = clean_touch_screen(data)

                elif col_name == "wifi":
                    cleaned_data = clean_wifi(data, inconsistencies[col_name])

                else:
                    cleaned_data = clean_price_category(data)

                row[index] = cleaned_data

        new_rows.append(row)

    return new_rows

                
def create_csv(data_rows):
    with open(CLEAN_CSV, "w") as outfile:
        csv_writer = csv.writer(outfile, delimiter=",")

        for row in data_rows:
            csv_writer.writerow(row)


def clean_mobile_data():
    mobile_data = get_mobile_price_data(MOBILE_PRICE_CSV)

    inconsistencies = get_inconsistent_data(INCONSISTENT_TXT)

    cleaned_mobile_data = clean_data(mobile_data, inconsistencies)

    create_csv(cleaned_mobile_data)


def main():
    clean_mobile_data()


if __name__ == "__main__":
    main()
