import numpy as np
from scipy.optimize import least_squares

# Helper function for trilateration
def trilaterate(satellite_positions, pseudoranges):
    # Define a function for validating input.
    def validate_input(satellite_data, pseudoranges):
        # Check if the input is a list of dictionaries for satellite_data
        if not isinstance(satellite_data, list) or not all(isinstance(sat, dict) and 'position' in sat for sat in satellite_data):
            return False, "satellite_data must be a list of dictionaries with 'position' key."
    
        # Check if the position is a list/tuple of length 3
        for sat in satellite_data:
            if not isinstance(sat['position'], (list, tuple)) or len(sat['position']) != 3:
                return False, "Each satellite position must be a list or tuple of length 3."

        # Check if pseudoranges are a list of numerical values
        if not isinstance(pseudoranges, list) or not all(isinstance(p, (int, float)) for p in pseudoranges):
            return False, f"pseudoranges must be a list of numerical values, but received: {pseudoranges}"

        return True, ""
    
    # Validate the inputs
    valid, message = validate_input(satellite_positions, pseudoranges)
    if not valid:
        print(f"[ERROR]: {message}")  # Output the error message
        return False, message  # Return the error

    # Initial guess for the receiver's position (x, y, z)
    initial_guess = [0, 0, 0]

    # Define residuals function for optimization
    def residuals(guess, satellite_positions, pseudoranges):
        res = []
        for i, sat_pos in enumerate(satellite_positions):
            # Calculate distance between the guess and satellite position
            distance = np.linalg.norm(np.array(guess) - np.array(sat_pos))
            # Residual is the difference between distance and pseudorange
            res.append(distance - pseudoranges[i])
        return res
    
    # Use least squares optimization to find the receiver's position
    result = least_squares(residuals, initial_guess, args=(satellite_positions, pseudoranges))
    
    # Return the optimized position (x, y, z)
    return True, result.x
