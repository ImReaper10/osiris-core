# Welcome to the Osiris Client SDK

Hello, and welcome! Below are the steps on how to set up the Osiris Client SDK!

## Setting Up the SDK

To get started, follow these steps to set up the SDK in your project:

1. **Copy the Directories**: Copy the following directories into your project:
   - `core`
   - `advanced-features`

2. **Place the Main File**: Place the `osirisclient.py` file in the same directory level as `core` and `advanced-features`.

3. **Import the Module**: In your code, import `osirisclient` as shown in the example below, and you’ll be all set!

## Example Usage

Here’s a quick example of how to use `osirisclient` to call functions in parallel. This example demonstrates calling two functions, `add` and `sub`, with the specified arguments.

```python
import osirisclient

# Define functions to be called in parallel with arguments
result = osirisclient.callFunctionsInParallel([
    {"function_name": "add", "args": [1, 2]},
    {"function_name": "sub", "args": [5, 3]}
])

# Print the result of the parallel calls, should be [3, 2]
print(result)
```

This would output the results from both functions being called in parallel. Read through the `Advanced Features Help.md` to learn how to use some of the advanced functionality of the SDK.

Happy coding!

