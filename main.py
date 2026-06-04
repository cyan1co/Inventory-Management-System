from read import read_products, display_products
from operation import decrease_quantity, increase_quantity, generate_invoice
from datetime import datetime

def main():
    filename = "products.txt"
    
    while True:
        # Displaying menu
        print("\n=== Inventory Management System ===")
        print("1. Display Inventory")
        print("2. Increase Product Quantity")
        print("3. Decrease Product Quantity")
        print("4. Exit")
        
        # Getting user's choice
        while True:
            try:
                choice = int(input("\nEnter your choice (1-4): "))
                if 1 <= choice <= 4:
                    break
                print("Please enter a number between 1 and 4")
            except ValueError:
                print("Please enter a valid number")
        
        # Handling user's choice
        if choice == 1:
            # Displaying inventory
            product_list = read_products(filename)
            display_products(product_list)
            
        elif choice == 2 or choice == 3:
            # Getting item name
            item = input("Enter the name of item: ").lower()
            
            # Getting quantity
            while True:
                try:
                    quantity = int(input(f"Enter quantity to {'increase' if choice == 2 else 'decrease'}: "))
                    if quantity > 0:
                        break
                    print("Quantity must be greater than 0")
                except ValueError:
                    print("Please enter a valid number")
            
            # Processing quantity change
            if choice == 2:
                success = increase_quantity(filename, item, quantity)
            else:
                # Ask if user wants to use the promotion
                use_promotion = input("Do you want to use Buy Three Get One Free promotion? (yes/no): ").lower()
                is_promotion = use_promotion in ['yes', 'y']
                success = decrease_quantity(filename, item, quantity, is_promotion)
                
                # Generate invoice for successful purchase
                if success:
                    invoice = generate_invoice(filename, item, quantity, is_promotion)
                    if invoice:
                        print("\nGenerating invoice...")
                        print(invoice)
                        # Save invoice to file
                        try:
                            with open(f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
                                f.write(invoice)
                            print("Invoice saved to file.")
                        except Exception as e:
                            print(f"Error saving invoice: {e}")
            
            if success:
                print("\n--- Updated Inventory ---")
                product_list = read_products(filename)
                display_products(product_list)
            else:
                print("\nOperation failed.")
                
        elif choice == 4:
            print("Thank you for using the Inventory Management System!")
            break

if __name__ == "__main__":
    main() 