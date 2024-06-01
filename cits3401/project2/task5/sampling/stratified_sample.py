import csv
import random

FULL_SAMPLE = "./full_clean_mobile_data.csv"

REDUCED_SAMPLE = "./reduced_clean_mobile_data.csv"

SAMPLE_SIZE_PERCENTAGE = 0.1 # 10%


def reduce_data(data_rows):
    """ reduce data rows to 10% of original size by random sampling """

    population_size = len(data_rows)
    sampled_rows = []

    while (len(sampled_rows) / population_size) < SAMPLE_SIZE_PERCENTAGE:
        random_index = random.randrange(0, population_size)

        sampled_rows.append(data_rows[random_index])

    return sampled_rows



def get_stratified_sample(data):
    """ stratify the data on PRICE_CATEGORY and return data with
        SAMPLE_SIZE_PERC amount of data for each
    """

    col_names = data[0]

    high_data = []
    not_high_data = []

    for row in data[1:]:
        if row[-1] == "high":
            high_data.append(row)
        else:
            not_high_data.append(row)

    reduced_high_data = reduce_data(high_data)
    reduced_not_high_data = reduce_data(not_high_data)

    reduced_data = []
    reduced_data.append(col_names)

    for row in reduced_high_data:
        reduced_data.append(row)
        
    for row in reduced_not_high_data:
        reduced_data.append(row)

    return reduced_data



def get_mobile_price_data(mobile_csv_file):
    """ return a list of rows from csv_file """

    with open(mobile_csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        return list(csv_reader)


def create_csv(data_rows):
    with open(REDUCED_SAMPLE, "w") as outfile:
        csv_writer = csv.writer(outfile, delimiter=",")

        for row in data_rows:
            csv_writer.writerow(row)



def main():
    data = get_mobile_price_data(FULL_SAMPLE)

    reduced_data = get_stratified_sample(data)

    create_csv(reduced_data)


if __name__ == "__main__":
    main()