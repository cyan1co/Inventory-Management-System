from read import read_products
from write import write_products
from datetime import datetime

def generate_invoice(filename, item_name, quantity, is_promotion=False):
    """
    Generates an invoice for a purchase.
    
    Args:
        filename (str): The name of the file containing product data
        item_name (str): The name of the item purchased
        quantity (int): The quantity purchased
        is_promotion (bool): Whether the purchase used buy three get one free promotion
        
    Returns:
        str: The generated invoice text, or None if operation failed
    """
    try:
        products = read_products(filename)
        if not products:
            return None

        # Finding the product in the inventory
        product = None
        for p in products:
            if p['name'].lower() == item_name.lower():
                product = p
                break
        
        if not product:
            print(f"Error: Product '{item_name}' not found")
            return None

        # Calculate total items and cost
        if is_promotion:
            if quantity < 3:
                print("For this promotion, you must buy at least 3 items")
                return None
            free_items = quantity // 3
            total_items = quantity + free_items
            total_cost = quantity * product['selling_price']
        else:
            free_items = 0
            total_items = quantity
            total_cost = quantity * product['selling_price']

        # Generate invoice
        invoice = f"""
=== INVOICE ===
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Product Details:
---------------
Name: {product['name']}
Brand: {product['brand']}
Quantity Purchased: {quantity}
Free Items: {free_items}
Total Items: {total_items}
Price per Item: Rs. {product['selling_price']}
Total Cost: Rs. {total_cost}

Thank you for your purchase!
===================
"""
        return invoice
                
    except Exception as e:
        print(f"An error occurred while generating invoice: {e}")
        return None

def decrease_quantity(filename, item_name, quantity, is_promotion=False):
    """
    Decreases the quantity of a specified product in the inventory.
    If is_promotion is True, implements buy three get one free logic.
    
    Args:
        filename (str): The name of the file containing product data
        item_name (str): The name of the item to update
        quantity (int): The quantity to decrease by
        is_promotion (bool): Whether to apply buy three get one free promotion
        
    Returns:
        bool: True if operation was successful, False otherwise
    """
    try:
        products = read_products(filename)
        if not products:
            return False

        # Finding the product in the inventory
        product_found = False
        for product in products:
            if product['name'].lower() == item_name.lower():
                product_found = True
                if quantity <= 0:
                    print("Quantity must be greater than 0")
                    return False
                
                if is_promotion:
                    if quantity < 3:
                        print("For this promotion, you must buy at least 3 items")
                        return False
                    # Calculate total items to take (including free items)
                    total_items = quantity + (quantity // 3)
                    if total_items > product['quantity']:
                        print(f"Error: Not enough stock available for the promotion. Current stock: {product['quantity']}")
                        return False
                    
                    # Updating the product quantity
                    product['quantity'] -= total_items
                    print(f"Successfully processed buy three get one free promotion:")
                    print(f"- Bought: {quantity} items")
                    print(f"- Got free: {quantity // 3} items")
                    print(f"- Total items taken: {total_items}")
                    print(f"- Total cost: Rs. {quantity * product['selling_price']}")
                else:
                    if quantity > product['quantity']:
                        print(f"Error: Not enough stock available. Current stock: {product['quantity']}")
                        return False
                    
                    # Updating the product quantity
                    product['quantity'] -= quantity
                    print(f"Successfully decreased quantity of {product['name']} by {quantity}.")
                break
        
        if not product_found:
            print(f"Error: Product '{item_name}' not found")
            return False
        
        # Writing the updated inventory back to the file
        return write_products(filename, products)
                
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def increase_quantity(filename, item_name, quantity):
    """
    Increases the quantity of a specified product in the inventory.
    
    Args:
        filename (str): The name of the file containing product data
        item_name (str): The name of the item to update
        quantity (int): The quantity to increase by
        
    Returns:
        bool: True if operation was successful, False otherwise
    """
    try:
        products = read_products(filename)
        if not products:
            return False

        # Finding the product in the inventory
        product_found = False
        for product in products:
            if product['name'].lower() == item_name.lower():
                product_found = True
                if quantity <= 0:
                    print("Quantity must be greater than 0")
                    return False
                
                # Updating the product quantity
                product['quantity'] += quantity
                print(f"Successfully increased quantity of {product['name']} by {quantity}.")
                break
        
        if not product_found:
            print(f"Error: Product '{item_name}' not found")
            return False
        
        # Writing the updated inventory back to the file
        return write_products(filename, products)
                
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def buy_three_get_one_free(filename, item_name, quantity):
    """
    Processes a buy three get one free promotion.
    
    Args:
        filename (str): The name of the file containing product data
        item_name (str): The name of the item to update
        quantity (int): The quantity to buy (must be at least 3)
        
    Returns:
        bool: True if operation was successful, False otherwise
    """
    try:
        products = read_products(filename)
        if not products:
            return False

        # Finding the product in the inventory
        product_found = False
        for product in products:
            if product['name'].lower() == item_name.lower():
                product_found = True
                if quantity < 3:
                    print("For this promotion, you must buy at least 3 items")
                    return False
                if quantity > product['quantity']:
                    print(f"Error: Not enough stock available. Current stock: {product['quantity']}")
                    return False
                
                # Calculate total items to take (including free items)
                total_items = quantity + (quantity // 3)
                if total_items > product['quantity']:
                    print(f"Error: Not enough stock available for the promotion. Current stock: {product['quantity']}")
                    return False
                
                # Updating the product quantity
                product['quantity'] -= total_items
                print(f"Successfully processed buy three get one free promotion:")
                print(f"- Bought: {quantity} items")
                print(f"- Got free: {quantity // 3} items")
                print(f"- Total items taken: {total_items}")
                print(f"- Total cost: Rs. {quantity * product['selling_price']}")
                break
        
        if not product_found:
            print(f"Error: Product '{item_name}' not found")
            return False
        
        # Writing the updated inventory back to the file
        return write_products(filename, products)
                
    except Exception as e:
        print(f"An error occurred: {e}")
        return False 