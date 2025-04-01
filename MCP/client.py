from mcp.client import MCPClient

# Create a client instance
client = MCPClient()

# Connect to the running server
client.connect()

# Call the add tool (tool names are as defined in the server)
result_add = client.call("add", 3, 4)  # Calls the 'add' function with arguments 3 and 4
print(f"Result of add: {result_add}")

# Call the multiply tool
result_multiply = client.call("multiply", 2, 5)  # Calls the 'multiply' function with arguments 2 and 5
print(f"Result of multiply: {result_multiply}")

# Call the greeting resource
greeting = client.call("greeting://Alice")  # Calls the 'greeting' resource with the 'Alice' parameter
print(f"Greeting: {greeting}")

# Optionally, disconnect after use
client.disconnect()
