import numpy as np
from sklearn.linear_model import LinearRegression


def fit_and_get_error(x, y, region):
    start, end = region

    model = LinearRegression()
    model.fit(x[start : end + 1].reshape(-1, 1), y[start : end + 1])
    # Calculate the predicted values
    y_pred = model.predict(x[start : end + 1].reshape(-1, 1))

    # Calculate the error (element-wise)
    error = np.abs(y[start : end + 1] - y_pred)
    return np.sum(error)


def perform_shift(x, y, left_region, right_region):
    # either return one or two regions after shifting
    left_start, _ = left_region
    _, right_end = right_region

    merged_region = (left_start, right_end)

    regions_to_error = [(merged_region, fit_and_get_error(x, y, merged_region))]
    for i in range(right_end - left_start - 2):
        new_left_start = left_start + i + 1
        new_right_start = new_left_start + 1
        new_left_region = (left_start, new_left_start)
        new_right_region = (new_right_start, right_end)
        left_error = fit_and_get_error(x, y, new_left_region)
        right_error = fit_and_get_error(x, y, new_right_region)
        total_error = left_error + right_error
        regions_to_error.append(((new_left_region, new_right_region), total_error))
    regions_to_error.sort(key=lambda x: x[1])
    # print(regions_to_error)
    regions = regions_to_error[0][0]
    regions = list(regions)
    return regions


import copy


# Iterative shifting of breakpoints
def shifting_approximation(x, y, subsections: list[tuple[float, float]]):
    assert (
        len(subsections) >= 2
    ), f"cannot merge subsections because you only have one or less section.\npassed: {subsections}"

    subsections = [(x, y) for x, y in subsections]
    subsections.sort(key=lambda x: x[0])

    last_sections = []
    current_sections = copy.deepcopy(subsections)
    # Iterate until the maximum subsection count is reached

    # i = 0
    while set(last_sections) != set(current_sections):
        # print(f'iteration: #{i}')
        # i+=1
        last_sections = copy.deepcopy(current_sections)
        left_region = current_sections[0]
        right_region = current_sections[1]

        new_subsections = perform_shift(x, y, left_region, right_region)

        for candidate in current_sections[2:]:
            last_new_candidate = new_subsections.pop(-1)
            outputs = perform_shift(x, y, last_new_candidate, candidate)
            new_subsections.extend(outputs)

        # Update the subsections
        current_sections = new_subsections
    return current_sections


# Example usage
x = np.linspace(0, 10, 100)
y = x**2
# y = np.sin(x)


def get_overall_error(x, y, regions):
    error = 0
    for region in regions:
        error += fit_and_get_error(x, y, region)
    return error


# randomize and shift?
import random

def get_random_regions(population, size):
    start = 0
    end = population -1
    candidates = list(range(1, population-1))
    assert len(candidates) > 0, f"wrong population and size: ({population}, {size})"
    chosen = random.sample(candidates, k=size)
    chosen.sort()
    ret = []
    for _s, _e in zip([start, *chosen[:-1]], [*chosen[1:], end]):
        ret.append((_s, _e))
    return ret

region_to_size = lambda regions: [y - x for x, y in regions]

# no better than uniform regions
subsections = get_random_regions(100, 10)
# 6.52 -> 6.52
# subsections = [(i * 10, (i + 1) * 10 - 1) for i in range(10)]
# 5.76 -> 4.54
# subsections = [(0, 6), (7, 12), (13, 24), (25, 31), (32, 37), (38, 49), (50, 56), (57, 62), (63, 74), (75, 81), (82, 87), (88, 99)]
# 7.94 -> 7.10
# subsections = [(0, 6), (7, 12), (13, 24), (25, 31), (32, 37), (38, 49), (50, 62), (63, 74), (75, 87), (88, 99)]
print(
    "Before:",
    subsections,
    region_to_size(subsections),
    get_overall_error(x, y, subsections),
    sep="\n",
)
subsections = shifting_approximation(x, y, subsections)
print(
    "After:",
    subsections,
    region_to_size(subsections),
    get_overall_error(x, y, subsections),
    sep="\n",
)
