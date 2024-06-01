# CITS1401: Computational Thinking with Python
# Project 1

# Name: Thomas Cleary
# Student Number: 21704985


import os

    
# Gets user input for filename, metric and action.
# Returns None if an input is invalid. Else returns inputs.
def get_inputs():
    file_name = input("Enter the file name containing World Happiness computation data: ")
    if not os.path.isfile(file_name):
        error("File not found.")
        return
    
    metric = sanitize(input("\nSelect a metric to compute the data.\n[min, median, mean, harmonic_mean]: "))
    if metric not in ["min", "median", "mean", "harmonic_mean", "harmonic mean"]:
        error("Invalid metric option.")
        return
    
    action = sanitize(input("\nChoose an action to be performed on the data.\n[list, correlation]: "))
    if action not in ["list", "correlation"]:
        error("Invalid action option.")
        return
    
    print()
    return [file_name, metric, action]


# Reads country data file into 2 dimensional list (list of data for each country).
# Converts data to appropriate type.
# Returns None if there is an error opening the file.
def read_file(file_name):
    try:
        country_file = open(file_name, 'r')
        country_file.readline()
        
    except FileNotFoundError:
        error("File not found.")
        return
    
    except:
        error("Unknown file error occured.")
        return
    
    happiness_data = []

    for line in country_file:
        country_data = line.split(',')
        
        # Remove '\n' from last elements
        # Convert data to float, or None if data is missing
        for i in range(1, len(country_data)):
            data_point = sanitize(country_data[i])
            
            if data_point == "":
                country_data[i] = None
                
            else:
                country_data[i] = float(data_point)
        
        happiness_data.append(country_data)
            
    country_file.close()
    
    if len(happiness_data) < 1:
        error("No country data in file.")
        return
    
    return happiness_data


# Takes happiness data of each country.
# Returns the 2d list of min and max values of each category.
def get_min_max(happiness_data):
    min_maxes = []
    
    # Set inital values of min/max
    for data in happiness_data[0][2:]:
        min_max = []
        for i in range(2):
            min_max.append(data)
            
        min_maxes.append(min_max)

    # Compare remaining data points against eachother to collect min/max values of all columns
    for data in happiness_data[1:]:
        for value in data[2:]:
            
            if value is not None:
                mm_index = data.index(value) - 2
    
                if value < min_maxes[mm_index][0]: # value < current minimum?
                    min_maxes[mm_index][0] = value
                
                elif value > min_maxes[mm_index][1]: # value > current maximum?
                    min_maxes[mm_index][1] = value
    
    return min_maxes


# Normalises each category of data in happiness_data.
# Returns normalised version of happiness data.
def normalise_data(happiness_data, min_max_data):
    for country in happiness_data:
        index = 2
        for data in country[2:]:
            if data is not None:
                min_value = min_max_data[index-2][0]
                max_value = min_max_data[index-2][1]
                country[index] = (country[index] - min_value) / (max_value - min_value)
            
            index += 1
    
    return happiness_data


# Decides which metric to compute based on previous user input
def compute_metric(metric, normalised_data):
    if metric == "min":
        return compute_min(normalised_data)
    
    elif metric == "median":
        return compute_median(normalised_data)
    
    elif metric == "mean":
        return compute_mean(normalised_data)
    
    else:
        return compute_harmonic_mean(normalised_data)


# Takes normalised happiness data.
# Returns 2D list of country-score(min) pairs.
def compute_min(data):
    countries = []
    remove_value(data, None)
    
    for country in data:
        min_pair = []
        min_pair.append(country[0])
        
        try:
            min_value = country[2]
            
            for value in country[3:]:
                    if value < min_value:
                        min_value = value
            
            min_pair.append(min_value)
            countries.append(min_pair)
        
        except IndexError:
            print(country[0] + " has no data and has been excluded.")
                    
    return countries


# Takes normalised happiness data.
# Returns 2D list of country-score(median) pairs.
def compute_median(data_list):
    remove_value(data_list, None)
    
    countries = []
    
    for country in data_list:
        values = sorted(country[2:]) # THIS IS WHAT YOU FORGOT  AND YOU LOST A MARK LOL
        num_values = len(values)
        completed = False
        
        if num_values % 2 == 0:
            
            if num_values == 0:
                print(country[0] + " has no data and has been excluded.\n")
                
            else:
                top_mid = int(num_values / 2)
                bottom_mid = int(top_mid - 1)
            
                median = (values[bottom_mid] + values[top_mid]) / 2
                completed = True
        else:
            
            if num_values == 1:
                median = values[0]
                
            else:
                median = values[num_values % 2]
            
            completed = True
        
        if completed:
            median_pair = []
            median_pair.append(country[0])
            median_pair.append(median)
            countries.append(median_pair)
    
    return countries


# Takes normalised happiness data.
# Returns 2D list of country-score(mean) pairs.
def compute_mean(data_list):
    remove_value(data_list, None)
    
    countries = []
    
    for country in data_list:
        mean_pair = []
        mean_pair.append(country[0])
        
        values = country[2:]
        total = 0
        
        for value in values:
            total += value
        
        mean = total / len(values)
        
        mean_pair.append(mean)
        countries.append(mean_pair)
    
    return countries


# Takes normalised happiness data.
# Returns a 2D list of country-score(harmonic mean) pairs.
def compute_harmonic_mean(data_list):
    remove_value(data_list, None)
    remove_value(data_list, 0)
    
    countries = []
    
    for country in data_list:
        hmean_pair = []
        hmean_pair.append(country[0])
        
        values = country[2:]
        
        numerator = len(values)
        denominator = 0
        
        for value in values:
            denominator += 1 / value
        
        hmean = numerator / denominator
        
        hmean_pair.append(hmean)
        countries.append(hmean_pair)
    
    return countries


# Prints list of countries first (highest value) to last (lowest value).
# If equal will be ranked aphabetically. 
def generate_list(country_score_pairs, metric):
    sort_descending(country_score_pairs)
    
    title = "Country\t\t\t\t\t{}".format(metric.title())
    line = "-" * 52
    print(title)
    print(line)
    
    rank = 1
    for country in country_score_pairs:
        print("{0:>3}) {1}\t\t\t\t\t{2:.4f}".format(rank, country[0], country[1]))
        rank += 1


# Prints the correlation between the official World Happiness Index and
# the ranks generated by computing the chosen metric.
def generate_spearman(country_score_pairs, happiness_data, metric):
    happiness_score_pairs = country_WHI_pair(happiness_data)
    sort_descending(happiness_score_pairs)
    sort_descending(country_score_pairs)
    
    sum_d_squared = 0
    n = len(country_score_pairs)
    
    country_rank = 0
    indexes = list(range(0, len(happiness_score_pairs))) # List of ints to track ranks of happiness_score_pairs.
    
    for country in country_score_pairs:
        index = 0
        found = False
        
        while not found:
                if country[0] == happiness_score_pairs[indexes[index]][0]:
                    sum_d_squared += (abs(country_rank - indexes.pop(index)))**2
                    found = True
                    
                else:
                    index += 1
                    
        country_rank += 1
    
    rank_correlation = 1 - (6*sum_d_squared)/(n*((n**2)-1))
    
    print("Correlation coefficient between the official World Happiness Index ranking and the rank using the "
            "{0} metric:\n{1:.4f}".format(metric, rank_correlation))


# Returns lower case string
# Leading/trailing whitespace and '\n' removed
def sanitize(string):
    return string.strip().lower()


# Returns a custom error message
def error(message):
    if message is None:
        print("Program ended.")
        
    else:
        print("Error: " + message + "\nEnding program...")


# Removes specified value from country lists in data
def remove_value(data, value):
    for country in data:
        for element in country[2:]: # [2:] == relevant data in a country list
            if element == value :
                country.remove(value)


# Returns 2D list of country-score(Official World Happiness Index Score) pairs.
def country_WHI_pair(happiness_data):
    countries = []
    
    for country in happiness_data:
        score_pair = []
        score_pair.append(country[0])
        score_pair.append(country[1])
        countries.append(score_pair)
    
    return countries


# Sorts 2D list of country-score pairs in descending order by their score.
def sort_descending(data_pairs):
    data_pairs.sort(reverse = True, key=byValue)


# Returns score in the country-score pair.
def byValue(data_pair):
    return data_pair[1]


def main():
    inputs = get_inputs()
    if inputs is None:
        error(inputs)
        return
    
    file_name, metric, action = inputs
    
    happiness_data = read_file(file_name)
    if happiness_data is None:
        error(happiness_data)
        return
    
    min_maxes = get_min_max(happiness_data)
    
    normalised_hap_data = normalise_data(happiness_data, min_maxes)

    country_score_pairs = compute_metric(metric, normalised_hap_data)
    
    if action == "list":
        generate_list(country_score_pairs, metric)
    
    else: # correlation
        generate_spearman(country_score_pairs, happiness_data, metric)


if __name__ == "__main__":
    main()