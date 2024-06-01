""" Compare dates between the 3 edited time series files """

import filenames as fn
import getCovidData as gcd


def compare_dates():
    """ returns true if dates the same between time_series files """

    date_lists = []
    for filename in fn.FILENAMES_NEW.values():
        date_lists.append(gcd.get_time_series_dates(filename))

    for index, date_list in enumerate(date_lists):
        for j in range(index+1, len(date_lists)):
            compare_against = date_lists[j]
            for date in date_list:
                assert date in compare_against


def main():
    # raises assertion error if all 3 time series files dont show the same dates
    compare_dates()



if __name__ == "__main__":
    main()