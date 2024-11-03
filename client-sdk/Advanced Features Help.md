
# Advanced Features of Client SDK: How to Use

This guide covers advanced API functions available in the Client SDK, demonstrating how to effectively use each function, with code examples and expected results.

---

## Table of Contents
1. [Batch Function Calls - `callFunctionBatch`](#batch-function-calls---callfunctionbatch)
2. [Retry Function Calls - `retryFunctionCall`](#retry-function-calls---retryfunctioncall)
3. [Caching Function Results - `cacheFunctionResult`](#caching-function-results---cachefunctionresult)
4. [Parallel Function Calls - `callFunctionsInParallel`](#parallel-function-calls---callfunctionsinparallel)

---

### Batch Function Calls - `callFunctionBatch`

The `callFunctionBatch` API allows multiple function calls to be sent in a single batch. It takes a list of function call details, executes them sequentially, and returns their results.

#### Parameters:
- `function_calls` (list): A list of dictionaries, each with:
  - `function_name` (str): The name of the function to call.
  - `args` (tuple): Arguments to pass to the function.

#### Returns:
- List of results for each function call.

#### Example Usage:
```python
function_calls = [
    {"function_name": "add", "args": (5, 3)},
    {"function_name": "sub", "args": (10, 4)}
]
results = callFunctionBatch(function_calls)
print(results)  # Expected output: [8, 6]
```

---

### Retry Function Calls - `retryFunctionCall`

The `retryFunctionCall` API is used to retry a function call in case of a network failure or function exception. Currently, for development purposes, there is a set chance of a fake network failure happening which you can see below. The function retries the call up to a specified number of times before throwing an exception if all attempts fail.

#### Parameters:
- `function_name` (str): The name of the function to call.
- `*args` (tuple): Arguments to pass to the function.
- `retries` (int, optional): Number of retry attempts. Default is 3.
- `logging` (bool, optional): Whether or not to log each failure

#### Global Function:
- Use `osirisclient.set_chance_of_network_failure(float from 0 to 1)` to change the chance of a retry failing

#### Returns:
- Result of the function call if successful.

#### Example Usage:
```python
import osirisclient as oc
try:
    oc.set_chance_of_network_failure(1)
    result = oc.retryFunctionCall("div", 10, 0, retries=2)
except Exception as e:
    print(e)  # Expected output: All retries failed error message

try:
    oc.set_chance_of_network_failure(0)
    result = oc.retryFunctionCall("div", 10, 0, retries=2)
except Exception as e:
    print(e)  # Expected output: All retries fail because of division by zero

try:
    oc.set_chance_of_network_failure(0)
    result = oc.retryFunctionCall("add", 2, 3, retries=2)
    print(result) # Should print 5
except Exception as e:
    print(e)  # Never should happen
```

---

### Caching Function Results - `cacheFunctionResult`

The `cacheFunctionResult` API caches the result of a function call to avoid redundant calls and improve efficiency. Results are cached for a specified time-to-live (TTL) in seconds.

#### Parameters:
- `function_name` (str): The name of the function to call.
- `*args` (tuple): Arguments to pass to the function.
- `ttl` (int, optional): Time-to-live for cache in seconds. Default is 300.

#### Returns:
- Cached or fresh result from the function call.

#### Example Usage:
```python
result = cacheFunctionResult("add", 4, 3, ttl=60)
print(result)  # Expected output: 7 (cached if called again within 60 seconds)
```

---

### Parallel Function Calls - `callFunctionsInParallel`

The `callFunctionsInParallel` API allows multiple function calls to be made concurrently using threads, making it faster to execute functions that are independent of each other.

#### Parameters:
- `function_calls` (list): A list of dictionaries, each with:
  - `function_name` (str): The name of the function to call.
  - `args` (tuple): Arguments to pass to the function.

#### Returns:
- List of results for each function call.

#### Example Usage:
```python
function_calls = [
    {"function_name": "add", "args": (10, 5)},
    {"function_name": "mult", "args": (3, 7)}
]
results = callFunctionsInParallel(function_calls)
print(results)  # Expected output: [15, 21]
```

---

### Helper Functions

#### `register`
The `register` function is a temporary helper function that lets you add a function to test the advanced features above with

**Usage:**
```python
import osirisclient as oc

def test(a,b):
    return a*b*b

oc.register("test", test) # You could put in a different name for the function you give (ie. oc.register("hello", test) then call the function with the function name of hello)

result = oc.callFunctionsInParallel([
    {"function_name": "add", "args": [1, 2]},
    {"function_name": "test", "args": [5, 2]}
])

# Print the result of the parallel calls
print(result) # Expected output: [3, 20]
```

#### `make_request`
The `make_request` function is a temporary helper that simulates requests and calls the relevant function using a delay to mimic real-world latency.

**Usage:**
```python
make_request("add", (2, 3))  # Expected output: 5 after a short delay
```
