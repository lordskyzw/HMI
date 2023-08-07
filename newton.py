# Mathematics laboratory
# the function to work with is: F(Dp) = (0.0022)turbidity [I’ll use a mean for tubebudity to make it constant] - 0.0236ferric + 0.0044flow
# define a function which normalizes turbidity to be between the range of 0 & 1


def normalize(arg):
    normalized_turbidity = (arg - 1.23) / (309 - 1.23)
    return normalized_turbidity


def random_turbidity(arg):
    """This function does the following:
    1)takes in the turbity column
    2) counts the number of unique entries in the column
    3) uses that number as the number of weights
    4) the weight number is then used in the sample function to generate a random turbidity value
    """
    # weights = arg.value_counts()
    # random_value = arg.sample(n=1, weights=weights)
    # random_value = random_value.to_list()

    return 0.6


def main_equation(flow: float, ferric_chloride: float, turbidity: float):
    """This function executes the dp equation and returns the value of dp
    1)it takes the turbidity in the parameters and normalizes it
    2)it calculates the dp using the parameters except with normalized turbidity"""
    global normalized_turbidity
    normalized_turbidity = normalize(turbidity)
    dp = (
        ((0.0022) * normalized_turbidity)
        - ((0.0236) * ferric_chloride)
        + ((0.0044) * flow)
    )
    return dp


def flow_optimizer(ferric_chloride: float):
    """this returns the optimized flow value"""
    global normalized_turbidity
    optimum_dp = 1.5
    optimized_flow = (
        -(((0.0022) * normalized_turbidity) - ((0.0236) * ferric_chloride) - optimum_dp)
        / 0.0044
    )
    return optimized_flow


def ferric_optimizer(flow: float):
    """this returns the optimized ferric chloride value"""
    global normalized_turbidity
    optimum_dp = 1.5
    optimized_ferric_chloride = (
        (0.0022) * normalized_turbidity - (0.0044) * flow + optimum_dp
    ) / (0.0236)

    return optimized_ferric_chloride
