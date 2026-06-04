from read import read_products
from write import write_products
from datetime import datetime

def generate_invoice(filename, item_id, quantity, is_promotion=False):
    """
    Generates an invoice for a purchase.
    
    Args:
        filename (str): The name of the file containing product data
        item_id (int): The ID of the item purchased
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
            if p['id'] == item_id:
                product = p
                break
        
        if not product:
            print(f"Error: Product with ID {item_id} not found")
            return None

        # Calculate total items and cost
        if is_promotion:
            if quantity < 3:
                print("For this promotion, you must buy at least 3 items")
                return None
            free_items = quantity // 3
            total_items = quantity + free_items
            subtotal = quantity * product['selling_price']
        else:
            free_items = 0
            total_items = quantity
            subtotal = quantity * product['selling_price']

        # Calculate VAT (13%)
        vat_amount = subtotal * 0.13
        total_cost = subtotal + vat_amount

        # Get current time
        current_time = datetime.now()
        date_str = f"{current_time.year}-{current_time.month:02d}-{current_time.day:02d}"
        time_str = f"{current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}"

        # Generate invoice
        invoice = f"""
=== INVOICE ===
Date: {date_str} {time_str}

Product Details:
---------------
ID: {product['id']}
Name: {product['name']}
Brand: {product['brand']}
Quantity Purchased: {quantity}
Free Items: {free_items}
Total Items: {total_items}
Price per Item: Rs. {product['selling_price']}
Subtotal: Rs. {subtotal:.2f}
VAT (13%): Rs. {vat_amount:.2f}
Total Cost: Rs. {total_cost:.2f}

Thank you for your purchase!
===================
"""
        return invoice
                
    except Exception as e:
        print(f"An error occurred while generating invoice: {e}")
        return None

def decrease_quantity(filename, item_id, quantity, is_promotion=False):
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
            if product['id'] == item_id:
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
            print(f"Error: Product '{item_id}' not found")
            return False
        
        # Writing the updated inventory back to the file
        return write_products(filename, products)
                
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def increase_quantity(filename, item_id, quantity):
    """
    Increases the quantity of a specified product in the inventory.
    
    Args:
        filename (str): The name of the file containing product data
        item_id (int): The ID of the item to update
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
            if product['id'] == item_id:
                product_found = True
                if quantity <= 0:
                    print("Quantity must be greater than 0")
                    return False
                
                # Updating the product quantity
                product['quantity'] += quantity
                print(f"Successfully increased quantity of {product['name']} by {quantity}.")
                break
        
        if not product_found:
            print(f"Error: Product with ID {item_id} not found")
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
            if product['name'] == item_name:
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

def add_product(filename, product_id, name, brand, quantity, cost_price, origin):
    """
    Adds a new product to the inventory.
    
    Args:
        filename (str): The name of the file containing product data
        product_id (int): The ID of the product
        name (str): The name of the product
        brand (str): The brand of the product
        quantity (int): The initial quantity
        cost_price (float): The cost price of the product
        origin (str): The country of origin
        
    Returns:
        bool: True if operation was successful, False otherwise
    """
    try:
        products = read_products(filename)
        if not products:
            # If file is empty or doesn't exist, start with empty list
            products = []
        
        # Checking if product ID already exists
        for product in products:
            if product['id'] == product_id:
                print(f"Error: Product ID {product_id} already exists")
                return False
        
        # Creating new product dictionary
        new_product = {
            "id": product_id,
            "name": name,
            "brand": brand,
            "quantity": quantity,
            "cost_price": cost_price,
            "origin": origin,
            "selling_price": cost_price * 2  # 200% markup
        }
        
        # Add new product to list
        products.append(new_product)
        
        # Write updated products back to file
        return write_products(filename, products)
                
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def generate_restock_invoice(filename, item_id, quantity):
    """
    Generates an invoice for restocking products.
    
    Args:
        filename (str): The name of the file containing product data
        item_id (int): The ID of the item restocked
        quantity (int): The quantity restocked
        
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
            if p['id'] == item_id:
                product = p
                break
        
        if not product:
            print(f"Error: Product with ID {item_id} not found")
            return None

        # Calculating costs
        subtotal = quantity * product['cost_price']
        vat_amount = subtotal * 0.13
        total_cost = subtotal + vat_amount

        # Get current time
        current_time = datetime.now()
        date_str = f"{current_time.year}-{current_time.month:02d}-{current_time.day:02d}"
        time_str = f"{current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}"

        # Generate invoice
        invoice = f"""
=== RESTOCK INVOICE ===
Date: {date_str} {time_str}

Product Details:
---------------
ID: {product['id']}
Name: {product['name']}
Brand: {product['brand']}
Quantity Restocked: {quantity}
Cost Price per Item: Rs. {product['cost_price']}
Subtotal: Rs. {subtotal:.2f}
VAT (13%): Rs. {vat_amount:.2f}
Total Cost: Rs. {total_cost:.2f}

Thank you for your restock!
===================
"""
        return invoice
                
    except Exception as e:
        print(f"An error occurred while generating restock invoice: {e}")
        return None 
