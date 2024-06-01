import csv

from clean_mobile_data import clean_mobile_data, CLEAN_CSV

MOBILE_PRICE_CSV = "../../provided_data_files/mobile_price.csv"
INCONSISTENT_TXT = "./inconsistencies.txt"
CLEAN_INCONSISTENT_TXT = "./final_inconsistencies.txt"


###############################################################################
# Functions to check data values 
###############################################################################

def is_int(value):
    """ check if value is an int """
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    """ check if value is an float """
    try:
        float(value)
        if "." not in value:
            return False
        return True

    except ValueError:
        return False


def is_yes_no(value):
    values = ["yes", "no"]
    if value in values:
        return True
    return False


def is_binary(value):
    try:
        value = int(value)
        if value == 0 or value == 1:
            return True
        return False
    except ValueError:
        return False


def check_battery_power(data):
    """ check if the value of data conforms to ColumnDescription.xlsx """
    return is_int(data)

def check_blue(data):
    """ check if the value of data conforms to ColumnDescription.xlsx """
    return is_yes_no(data)

def check_clock_speed(data):
    """ check if the value of data conforms to ColumnDescription.xlsx """
    return is_float(data)

def check_dual_sim(data):
    return is_yes_no(data)

def check_fc(data):
    return is_int(data)

def check_four_g(data):
    return is_binary(data)

def check_int_memory(data):
    return is_int(data)

def check_m_dep(data):
    return is_float(data)

def check_mobile_wt(data):
    return is_int(data)

def check_n_cores(data):
    return is_int(data)

def check_pc(data):
    return is_int(data)

def check_px_height(data):
    return is_int(data)

def check_px_width(data):
    return is_int(data)

def check_ram(data):
    return is_int(data)

def check_sc_h(data):
    return is_int(data)

def check_sc_w(data):
    return is_int(data)

def check_talk_time(data):
    return is_int(data)

def check_three_g(data):
    return is_yes_no(data)

def check_touch_screen(data):
    return is_binary(data)

def check_wifi(data):
    return is_yes_no(data)

def check_price_category(data):
    return is_binary(data)

###############################################################################

def check_for_inconsistencies(mobile_data):
    column_names = mobile_data[0][1:]

    inconsistencies = {}

    for name in column_names:
        inconsistencies[name] = []

    for row in mobile_data[1:]:
        row_data = row[1:]

        functions = [
            check_battery_power,
            check_blue,
            check_clock_speed,
            check_dual_sim,
            check_fc,
            check_four_g,
            check_int_memory,
            check_m_dep,
            check_mobile_wt,
            check_n_cores,
            check_pc,
            check_px_height,
            check_px_width,
            check_ram,
            check_sc_h,
            check_sc_w,
            check_talk_time,
            check_three_g,
            check_touch_screen,
            check_wifi,
            check_price_category,
        ]

        for index, function_data in enumerate(zip(functions, row_data)):
            function, data = function_data

            consistent = function(data)
            if not consistent:

                if isinstance(data, str):
                    data = data.strip()

                if data == "":
                    data = "EMPTY STRING"

                # only add inconsistency once
                if data not in inconsistencies[column_names[index]]:
                    inconsistencies[column_names[index]].append("{}".format(data))

    return inconsistencies


def get_mobile_price_data(mobile_csv_file):
    """ return a list of rows from csv_file """

    with open(mobile_csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        return list(csv_reader)


def create_output(filename, inconsistencies):
    with open(filename, "w") as output_file:
        
        no_problems = True
        for key in inconsistencies:
            if len(inconsistencies[key]) > 0:
                no_problems = False
                break
        
        if no_problems:
            print("NO INCONSISTENCIES REMAINING", file=output_file)
            return

        for key in inconsistencies:
            msg_list = inconsistencies[key]

            if len(msg_list) > 0:
                print('#' * 80, file=output_file)
                print("Column Name = {}".format(key), file=output_file)
                for msg in msg_list:
                    print(msg, file=output_file)


def main():
    """ 
    produces a text file with information about inconsistent data in 
    each column of mobile_price.csv
    """

    data = get_mobile_price_data(MOBILE_PRICE_CSV)

    inconsistencies = check_for_inconsistencies(data)

    create_output(INCONSISTENT_TXT, inconsistencies)

    clean_mobile_data()

    clean_data = get_mobile_price_data(CLEAN_CSV)

    new_inconsistencies = check_for_inconsistencies(clean_data)

    create_output(CLEAN_INCONSISTENT_TXT, new_inconsistencies)


if __name__ == "__main__":
    main()
