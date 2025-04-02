from mcp.client import MCPClient
import sys

def main():
    # Create a client instance
    client = MCPClient()
    
    try:
        # Connect to the running server
        print("Connecting to MCP server...")
        client.connect()
        print("Connected successfully!")
        
        while True:
            print("\nAvailable operations:")
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            print("5. Power")
            print("6. Square Root")
            print("7. Cube Root")
            print("8. Factorial")
            print("9. Log")
            print("10. Remainder")
            print("11. Sin")
            print("12. Cos")
            print("13. Tan")
            print("14. Get Greeting")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-14): ")
            
            if choice == "0":
                break
                
            try:
                if choice in ["1", "2", "3", "4", "5", "10"]:
                    a = float(input("Enter first number: "))
                    b = float(input("Enter second number: "))
                    
                    if choice == "1":
                        result = client.call("add", a, b)
                    elif choice == "2":
                        result = client.call("subtract", a, b)
                    elif choice == "3":
                        result = client.call("multiply", a, b)
                    elif choice == "4":
                        result = client.call("divide", a, b)
                    elif choice == "5":
                        result = client.call("power", a, b)
                    elif choice == "10":
                        result = client.call("remainder", a, b)
                        
                elif choice in ["6", "7", "8", "9", "11", "12", "13"]:
                    a = float(input("Enter number: "))
                    
                    if choice == "6":
                        result = client.call("sqrt", a)
                    elif choice == "7":
                        result = client.call("cbrt", a)
                    elif choice == "8":
                        result = client.call("factorial", int(a))
                    elif choice == "9":
                        result = client.call("log", a)
                    elif choice == "11":
                        result = client.call("sin", a)
                    elif choice == "12":
                        result = client.call("cos", a)
                    elif choice == "13":
                        result = client.call("tan", a)
                        
                elif choice == "14":
                    name = input("Enter name: ")
                    result = client.call(f"greeting://{name}")
                    
                else:
                    print("Invalid choice. Please try again.")
                    continue
                    
                print(f"\nResult: {result}")
                
            except Exception as e:
                print(f"Error: {str(e)}")
                
    except Exception as e:
        print(f"Connection error: {str(e)}")
    finally:
        client.disconnect()
        print("\nDisconnected from server.")

if __name__ == "__main__":
    main() 