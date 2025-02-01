import numpy as np
from scipy.optimize import least_squares

# Speed of light in meters per second
C = 299792458  

def validate_input(satellite_positions, pseudoranges):
    """
    Validates the input for the trilateration function.
    
    :param satellite_positions: List of satellite positions [(x, y, z, t), ...]
    :param pseudoranges: List of pseudorange distances
    :return: (bool, error_message or None)
    """
    # Ensure we have at least 4 satellites
    if len(satellite_positions) < 4 or len(pseudoranges) < 4:
        return False, "At least 4 satellite positions and pseudoranges are required."

    # Ensure satellite_positions is a list of tuples/lists with 4 elements (x, y, z, time)
    for sat in satellite_positions:
        if not isinstance(sat, (list, tuple)) or len(sat) != 4:
            return False, f"Invalid satellite position format: {sat}. Must be (x, y, z, time)."

    # Ensure pseudoranges are numerical values
    if not all(isinstance(p, (int, float)) for p in pseudoranges):
        return False, f"Invalid pseudorange values: {pseudoranges}. Must be numbers."

    return True, None

def trilaterate(satellite_positions, pseudoranges):
    """
    Uses least-squares trilateration to compute the receiver's position and clock bias.
    
    :param satellite_positions: List of (x, y, z, t) positions of satellites
    :param pseudoranges: List of distances from receiver to satellites
    :return: (latitude, longitude, altitude, time_bias) if successful, else error message
    """
    # Validate the inputs
    valid, error_message = validate_input(satellite_positions, pseudoranges)
    if not valid:
        print(f"[ERROR] {error_message}")
        return None, error_message

    # Convert lat/lon to Cartesian (if needed)
    def latlon_to_cartesian(lat, lon, alt=0):
        """Convert latitude/longitude to ECEF coordinates."""
        earth_radius = 6371000  # Approximate radius of Earth in meters
        lat, lon = np.radians(lat), np.radians(lon)
        x = (earth_radius + alt) * np.cos(lat) * np.cos(lon)
        y = (earth_radius + alt) * np.cos(lat) * np.sin(lon)
        z = (earth_radius + alt) * np.sin(lat)
        return np.array([x, y, z])

    # Convert input satellite positions from lat/lon/alt to Cartesian
    cartesian_positions = np.array([latlon_to_cartesian(*pos[:3]) for pos in satellite_positions])

    # Extract satellite timestamps
    satellite_times = np.array([pos[3] for pos in satellite_positions])

    # Initial guess
    initial_guess = np.append(np.mean(cartesian_positions, axis=0), 0)  # [x, y, z, t_bias]
    print("Initial Guess:", initial_guess)

    # Define the function to minimize (accounting for clock bias)
    def residuals(guess, sat_positions, sat_times, ranges, alpha=1e-6):
        x, y, z, t_bias = guess  # Receiver position and clock bias
        distances = np.linalg.norm(sat_positions - np.array([x, y, z]), axis=1)
        time_corrections = C * (sat_times + t_bias)  

        # Apply scaling factor alpha to bring distances to a comparable magnitude with pseudoranges
        return (alpha * distances + time_corrections) - np.array(ranges)

    # Solve using least squares optimization
    result = least_squares(residuals, initial_guess, args=(cartesian_positions, satellite_times, pseudoranges))

    # Extract final position and time bias
    final_position, time_bias = result.x[:3], result.x[3]

    # Convert back to lat/lon/alt
    def cartesian_to_latlon(x, y, z):
        """Convert ECEF (x, y, z) back to latitude, longitude, and altitude."""
        earth_radius = 6371000  # Earth's radius in meters
        lon = np.arctan2(y, x)
        hyp = np.sqrt(x ** 2 + y ** 2)
        lat = np.arctan2(z, hyp)
        alt = np.linalg.norm([x, y, z]) - earth_radius
        return np.degrees(lat), np.degrees(lon), alt

    # Convert position back to lat/lon/alt
    lat, lon, alt = cartesian_to_latlon(*final_position)

    return (lat, lon, alt, time_bias), None


if __name__ == "__main__":
    # Example satellite positions (latitude, longitude, altitude, timestamp)
    satellite_data = [
        (37.7749, -122.4194, 20000, 0.001),  # Satellite 1
        (37.7750, -122.4184, 21000, 0.002),  # Satellite 2
        (37.7760, -122.4174, 22000, 0.003),  # Satellite 3
        (37.7770, -122.4164, 23000, 0.004)   # Satellite 4
    ]

    # Example pseudoranges (distances to the receiver)
    pseudoranges = [10000, 10050, 10100, 10150]

    # Perform trilateration
    device_position, error = trilaterate(satellite_data, pseudoranges)

    if error:
        print(f"[ERROR] {error}")
    else:
        lat, lon, alt, time_bias = device_position
        print(f"Device Position (lat, lon, alt): {lat}, {lon}, {alt}")
        print(f"Clock Bias: {time_bias} seconds")
