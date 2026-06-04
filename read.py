def read_products(filename):
    """
    It reads product data from a file and returns a list of product dictionaries.
    
    Args:
        filename (str): The name of the file containing product data.
        
    Returns:
        list: A list of dictionaries, where each dictionary contains product information
              including name, brand, quantity, cost price, origin, and selling price.
    """
    products = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Splitting each line into parts using comma and space as separator
                parts = line.strip().split(', ')
                if len(parts) == 5:
                    # Creating a dictionary for each product with calculated selling price
                    product = {
                        "name": parts[0],
                        "brand": parts[1],
                        "quantity": int(parts[2]),
                        "cost_price": float(parts[3]),
                        "origin": parts[4],
                        "selling_price": float(parts[3]) * 2  # 200% markup
                    }
                    products.append(product)
        return products
    except FileNotFoundError:
        print("Error: File not found.")
        return []
    except Exception as e:
        print("An error occurred:", e)
        return []

def display_products(products):
    """
    Displays product information in a formatted, readable way.
    
    Args:
        products (list): List of product dictionaries to display.
    """
    if not products:
        print("No products to display.")
        return
    
    print("\n--- ✦ Available Products ✦ ---\n")
    for product in products:
        # Displaying each product's details in a formatted way
        print(f"Product Name   : {product['name']}")
        print(f"Brand          : {product['brand']}")
        print(f"Country        : {product['origin']}")
        print(f"Stock Quantity : {product['quantity']}")
        print(f"Cost Price     : Rs. {product['cost_price']}")
        print(f"Selling Price  : Rs. {product['selling_price']}")
        print("-" * 30)