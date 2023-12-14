def round_to_significant_decimals(number: float, num_significant_decimals: int) -> float:
    """
    Rounds a number to a specified number of significant decimals.

    Parameters:
    - number (float): The input number to be rounded.
    - num_significant_decimals (int): The number of significant decimals.

    Returns:
    - float: The rounded number.
    """
    # Convert the number to a string to handle significant decimals
    non_decimal_part = int(number)
    decimal_part_str = str(number).split(".")[1]

    # If the number already has the desired number of significant decimals, return it
    if len(decimal_part_str) == num_significant_decimals:
        return number

    # Find the index of the last non-zero digit to the left of the significant decimals
    idx_last_zero_left = -1
    for idx, digit in enumerate(decimal_part_str):
        if digit != "0":
            idx_last_zero_left = idx
            break

    # Extract significant decimals and zeros to the left
    significant_decimals = decimal_part_str[idx_last_zero_left: idx_last_zero_left + num_significant_decimals + 2]
    zeros_to_left = decimal_part_str[:idx_last_zero_left]

    # Initialize variables for rounding
    last_significant_decimal = 0
    round_decimal = int(significant_decimals[num_significant_decimals])

    # Determine the rounding based on the value of the digit at num_significant_decimals
    if round_decimal > 5:
        last_significant_decimal += 1

    # Check for rounding when the digit at num_significant_decimals is 5
    if round_decimal == 5:
        next_round_decimal = int(significant_decimals[num_significant_decimals + 1])
        if next_round_decimal > 5:
            last_significant_decimal += 1

    # Calculate the rounded significant decimals and construct the new decimal part
    significant_decimals = str(int(significant_decimals[:num_significant_decimals]) + last_significant_decimal)
    new_decimal_part = float("0." + zeros_to_left + significant_decimals)

    # Combine the non-decimal and decimal parts to get the rounded number
    rounded_number = non_decimal_part + new_decimal_part

    return rounded_number
