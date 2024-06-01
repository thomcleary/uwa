import csv

CLEAN_DATA_FILE = "../task1d_data_cleaning/cleaned_mobile_data.csv"

REDUCED_CSV = "./reduced_clean_mobile_data.csv"


def get_mobile_price_data(mobile_csv_file):
    """ return a list of rows from csv_file """

    with open(mobile_csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        return list(csv_reader)


def get_new_colnames():
    return [
        "id", "battery_power", "has_bluetooth",
        "clock_speed", "has_dual_sim", "front_camera_mp",
        "has_four_g", "internal_memory", "mobile_depth",
        "mobile_weight", "num_cores", "primary_camera_mp",
        "pixels_height", "pixels_width", "ram",
        "screen_height", "screen_width", "talk_time",
        "has_three_g", "has_touch_screen", "has_wifi",
        "price_category"
    ]


def remove_attributes(data, remove_attributes):
    col_names = get_new_colnames()

    new_col_names = []

    for name in col_names:
        if name not in remove_attributes:
            new_col_names.append(name)

    with open(REDUCED_CSV, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")

        csv_writer.writerow(new_col_names)
        
        for row in data[1:]:
            new_row = []
            for index, data_point in enumerate(row):
                if col_names[index] in remove_attributes:
                    continue
                new_row.append(data_point)
            csv_writer.writerow(new_row)


def main():
    data = get_mobile_price_data(CLEAN_DATA_FILE)
    
    removed_attributes = [
        "id"
    ]

    remove_attributes(data, removed_attributes)



if __name__ == "__main__":
    main()