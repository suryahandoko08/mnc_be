def calculate_change(total_purchase, amount_paid):

    denominations = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]

    # Check if the amount paid is less than the total purchase
    if amount_paid < total_purchase:
        return False, "insufficient payment"
    
    # Calculate the change
    change = amount_paid - total_purchase

    rounded_change = (change // 100) * 100

    # Prepare the result for denominations
    denomination_result = []
    
    for denom in denominations:
        quantity = rounded_change // denom
        if quantity > 0:
            rounded_change -= quantity * denom
            if denom >= 1000: 
                denomination_result.append(f"{quantity} notes of {denom:,}")
            else:  # For coins
                denomination_result.append(f"{quantity} coins of {denom:,}")

    return change, rounded_change, denomination_result

# Example usage
total1 = 700649
paid1 = 800000
change1, rounded_change1, denominations1 = calculate_change(total1, paid1)
print(f"Change to be given by the cashier: {change1:,}, rounded down to {rounded_change1:,}")
print("Denominations:")
for denomination in denominations1:
    print(denomination)

total2 = 575650
paid2 = 580000
change2, rounded_change2, denominations2 = calculate_change(total2, paid2)
print(f"\nChange to be given by the cashier: {change2:,}, rounded down to {rounded_change2:,}")
print("Denominations:")
for denomination in denominations2:
    print(denomination)

total3 = 657650
paid3 = 600000
result3 = calculate_change(total3, paid3)
if result3[0] is False:
    print("\nFalse,", result3[1])
