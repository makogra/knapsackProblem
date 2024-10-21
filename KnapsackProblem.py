
class KnapsackProblem:
    def __init__(self, size, weight, data):
        self.size = int(size)
        self.weight = int(weight)
        self.data = data

    def __str__(self):
        result = f"""
        size = {self.size}
        weight =  {self.weight}
        """
        i = 1
        for data_pair in self.data:
            result += "val" + str(i) + " = " + data_pair[0] + " weight" + str(i) + " = " + data_pair[1]
            i += 1
        return result
