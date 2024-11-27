import re

def reformat_log(file_path):
    data = {
        'Optimal Solution': [],
        'Crossover implementation': [],
        'Score_Log': []
    }
    
    with open(file_path, 'r') as file:
        content = file.read()
        
    # Regular expressions for extracting the data
    optimal_solution_pattern = re.compile(r'Optimal solution = (\d*\.?\d+)')
    crossover_impl_pattern = re.compile(r'Crossover implementation: (\w+)')
    score_log_pattern = re.compile(r'whole score log: \[(.*?)\]')
    
    # Extract each configuration's details and populate the dictionary
    optimal_solution = optimal_solution_pattern.findall(content)
    crossover_impl = crossover_impl_pattern.findall(content)
    score_logs = score_log_pattern.findall(content)
    
    # Convert extracted strings to appropriate types and add to data dictionary
    # data['Population_Size'] = list(map(int, populations))
    # data['Crossover_Percentage'] = list(map(float, crossovers))
    data['Optimal Solution'] = list(map(float, optimal_solution))
    data['Crossover implementation'] = list(map(str, crossover_impl))
    
    # Convert each score log into a list of floats
    for log in score_logs:
        scores = list(map(float, log.split(',')))
        data['Score_Log'].append(scores)
    
    return data

# Example usage:
file_path = 'knapPI_2_2000_1000_1'  # Replace with your file path
formatted_data = reformat_log(file_path)
print(formatted_data)
 
