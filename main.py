from read import read_products, display_products
from operation import decrease_quantity, increase_quantity, generate_invoice, generate_restock_invoice, add_product
from datetime import datetime

def main():
    filename = "products.txt"
    
    while True:
        # Displaying menu
        print("\n=== Inventory Management System ===")
        print("1. Display Inventory")
        print("2. Add New Product")
        print("3. Restock Product")
        print("4. Sell Product")
        print("5. Exit")
        
        # Getting user's choice
        while True:
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                if 1 <= choice <= 5:
                    break
                print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")
        
        # Handling user's choice
        if choice == 1:
            # Displaying inventory
            product_list = read_products(filename)
            display_products(product_list)
            
        elif choice == 2:
            # Adding new product
            try:
                # Get product details
                while True:
                    try:
                        product_id = int(input("Enter product ID: "))
                        if product_id > 0:
                            break
                        print("Product ID must be greater than 0")
                    except ValueError:
                        print("Please enter a valid number")
                
                name = input("Enter product name: ")
                brand = input("Enter brand name: ")
                while True:
                    try:
                        quantity = int(input("Enter initial quantity: "))
                        if quantity > 0:
                            break
                        print("Quantity must be greater than 0")
                    except ValueError:
                        print("Please enter a valid number")
                cost_price = float(input("Enter cost price: "))
                origin = input("Enter country of origin: ")
                
                # Adding the product
                success = add_product(filename, product_id, name, brand, quantity, cost_price, origin)
                
                if success:
                    print("\n--- Updated Inventory ---")
                    product_list = read_products(filename)
                    display_products(product_list)
                else:
                    print("\nFailed to add product.")
            except ValueError:
                print("Invalid input. Please enter valid numbers for ID, quantity and cost price.")
            
        elif choice == 3 or choice == 4:
            # Getting item ID
            while True:
                try:
                    item_id = int(input("Enter the product ID: "))
                    if item_id > 0:
                        break
                    print("Product ID must be greater than 0")
                except ValueError:
                    print("Please enter a valid number")
            
            # Getting quantity
            while True:
                try:
                    quantity = int(input(f"Enter quantity to {'restock' if choice == 3 else 'sell'}: "))
                    if quantity > 0:
                        break
                    print("Quantity must be greater than 0")
                except ValueError:
                    print("Please enter a valid number")
            
            # Processing quantity change
            if choice == 3:
                success = increase_quantity(filename, item_id, quantity)
                # Generating restock invoice for successful restock
                if success:
                    invoice = generate_restock_invoice(filename, item_id, quantity)
                    if invoice:
                        print("\nGenerating restock invoice...")
                        print(invoice)
                        # Saving invoice to file
                        try:
                            current_time = datetime.now()
                            timestamp = f"{current_time.year}{current_time.month:02d}{current_time.day:02d}_{current_time.hour:02d}{current_time.minute:02d}{current_time.second:02d}"
                            with open(f"restock_invoice_{timestamp}.txt", 'w') as f:
                                f.write(invoice)
                            print("Restock invoice saved to file.")
                        except Exception as e:
                            print(f"Error saving restock invoice: {e}")
            else:
                # Asking if user wants to use the promotion
                use_promotion = input("Do you want to use Buy Three Get One Free promotion? (yes/no): ")
                is_promotion = use_promotion in ['yes', 'y']
                success = decrease_quantity(filename, item_id, quantity, is_promotion)
                
                # Generating invoice for successful purchase
                if success:
                    invoice = generate_invoice(filename, item_id, quantity, is_promotion)
                    if invoice:
                        print("\nGenerating invoice...")
                        print(invoice)
                        # Save invoice to file
                        try:
                            current_time = datetime.now()
                            timestamp = f"{current_time.year}{current_time.month:02d}{current_time.day:02d}_{current_time.hour:02d}{current_time.minute:02d}{current_time.second:02d}"
                            with open(f"sale_invoice_{timestamp}.txt", 'w') as f:
                                f.write(invoice)
                            print("Sale invoice saved to file.")
                        except Exception as e:
                            print(f"Error saving invoice: {e}")
            
            if success:
                print("\n--- Updated Inventory ---")
                product_list = read_products(filename)
                display_products(product_list)
            else:
                print("\nOperation failed.")
                
        elif choice == 5:
            print("Thank you for using the Inventory Management System!")
            break

if __name__ == "__main__":
    main() 