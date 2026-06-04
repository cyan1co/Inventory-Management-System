def read_products(filename):
    """
    It reads product data from a file and returns a list of product dictionaries.
    
    Args:
        filename (str): The name of the file containing product data.
        
    Returns:
        list: A list of dictionaries, where each dictionary contains product information
              including id, name, brand, quantity, cost price, origin, and selling price.
    """
    products = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Splitting each line into parts using comma and space as separator
                parts = line.strip().split(', ')
                if len(parts) == 6:  # Now expecting 6 parts including ID
                    # Creating a dictionary for each product with calculated selling price
                    product = {
                        "id": int(parts[0]),
                        "name": parts[1],
                        "brand": parts[2],
                        "quantity": int(parts[3]),
                        "cost_price": float(parts[4]),
                        "origin": parts[5],
                        "selling_price": float(parts[4]) * 2  # 200% markup
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
    Displays product information in a formatted table.
    
    Args:
        products (list): List of product dictionaries to display.
    """
    if not products:
        print("No products to display.")
        return
    
    print("\n=== ✦ Available Products ✦ ===\n")
    
    # Define column headers and widths
    headers = ["Product ID", "Product Name", "Brand", "Country", "Stock", "Cost Price", "Selling Price"]
    widths = [10, 19, 10, 15, 8, 12, 12]
    
    # Print header
    header_format = " | ".join(f"{{:<{width}}}" for width in widths)
    print(header_format.format(*headers))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    
    # Print each product
    for product in products:
        row = [
            product['id'],
            product['name'],
            product['brand'],
            product['origin'],
            str(product['quantity']),
            f"Rs. {product['cost_price']}",
            f"Rs. {product['selling_price']}"
        ]
        print(header_format.format(*row))
    
    print()  