def write_products(filename, products):
    """
    Writes product data to a file.
    
    Args:
        filename (str): The name of the file to write to
        products (list): List of product dictionaries to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w') as file:
            for product in products:
                file.write(f"{product['name']}, {product['brand']}, {product['quantity']}, {product['cost_price']}, {product['origin']}\n")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False 