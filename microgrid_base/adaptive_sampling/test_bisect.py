import numpy as np
from sklearn.linear_model import LinearRegression

# TODO: shift the breakpoints iteratively

# Adaptive Piecewise Approximation algorithm
def adaptive_piecewise_approximation(x, y, max_subsection_count, error_threshold = 0):
    # Initialize with the entire range as the first subsection
    subsections = [(0, len(x)-1)]

    # Iterate until the maximum subsection count is reached
    while len(subsections) < max_subsection_count:
        new_subsections = []
        errors = []

        # Iterate over each subsection
        for start, end in subsections:
            # TODO: change the error calculation method, fix the start & end points, fuse the connecting points
            # Perform linear regression on the subsection
            model = LinearRegression()
            model.fit(x[start:end+1].reshape(-1, 1), y[start:end+1])

            # Calculate the predicted values
            y_pred = model.predict(x[start:end+1].reshape(-1, 1))

            # Calculate the error (element-wise)
            error = np.abs(y[start:end+1] - y_pred)

            # Store the error and subsection
            errors.append(np.sum(error))
            new_subsections.append((start, end))

        # Find the subsection with the highest error
        max_error_index = np.argmax(errors)
        max_error = errors[max_error_index]
        max_error_subsection = new_subsections[max_error_index]

        # Check if the maximum error is greater than a threshold
        if max_error > error_threshold:
            # Bisect the subsection with the highest error
            start, end = max_error_subsection
            if end-start <= 1:
                break
            mid = (end+start) // 2
            new_subsections[max_error_index] = (max_error_subsection[0], mid)
            new_subsections.append((mid+1, max_error_subsection[1]))
            new_subsections.sort(key = lambda x: x[0])
        else:
            break

        # Update the subsections
        subsections = new_subsections

    return subsections

# Example usage
x = np.linspace(0, 10, 100)
y = x **2
# y = np.sin(x)

# msc = 20
# msc = 12
msc = 10
# msc = 12
subsections = adaptive_piecewise_approximation(x, y, max_subsection_count=msc)
print("Subsections:", subsections)
print("Subsection lengths:", [(end-start) for start, end in subsections])
