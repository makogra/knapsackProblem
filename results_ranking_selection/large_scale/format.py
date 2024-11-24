import re

def reformat_log(file_path):
    data = {
        'Population_Size': [],
        'Crossover_Percentage': [],
        'Mutation_Percentage': [],
        'Elites': [],
        'Score_Log': []
    }
    
    with open(file_path, 'r') as file:
        content = file.read()
        
    # Regular expressions for extracting the data
    population_pattern = re.compile(r'Population Size: (\d+)')
    crossover_pattern = re.compile(r'Crossover %: ([\d.]+)')
    mutation_pattern = re.compile(r'Mutation %: ([\d.]+)')
    elites_pattern = re.compile(r'Number of Elites: (\d+)')
    score_log_pattern = re.compile(r'whole score log: \[(.*?)\]')
    
    # Extract each configuration's details and populate the dictionary
    populations = population_pattern.findall(content)
    crossovers = crossover_pattern.findall(content)
    mutations = mutation_pattern.findall(content)
    elites = elites_pattern.findall(content)
    score_logs = score_log_pattern.findall(content)
    
    # Convert extracted strings to appropriate types and add to data dictionary
    data['Population_Size'] = list(map(int, populations))
    data['Crossover_Percentage'] = list(map(float, crossovers))
    data['Mutation_Percentage'] = list(map(float, mutations))
    data['Elites'] = list(map(int, elites))
    
    # Convert each score log into a list of floats
    for log in score_logs:
        scores = list(map(float, log.split(',')))
        data['Score_Log'].append(scores)
    
    return data

# Example usage:
file_path = 'knapPI_2_2000_1000_1'  # Replace with your file path
formatted_data = reformat_log(file_path)
print(formatted_data)
 
