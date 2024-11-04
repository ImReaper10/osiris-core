
# Advanced Features of Client SDK: How to Use

This guide covers advanced API functions available in the Client SDK, demonstrating how to effectively use each function, with code examples and expected results.

All of the functions below use a simulated network request. The exact way we do this is to just simply wait a small amount of time, and then locally call a function from within python. This is not how it will work once we have something to connect to. For now, built in to the functions below we have 4 functions you can call, `add`, `sub`, `mult`, and `div`. Each of these function simply add, subtract, multiply, or divide two number inputs respectivly. If you want to add your own function to test with, scroll to the bottom of the page to view the `osirisclient.register` function. Note that, the features of the core part of the SDK may behave differently (meaning other functions that aren't part of the advanced features below may behave in different ways).

---

## Table of Contents
1. [Batch Function Calls - `callFunctionBatch`](#batch-function-calls---callfunctionbatch)
2. [Retry Function Calls - `retryFunctionCall`](#retry-function-calls---retryfunctioncall)
3. [Enable Real-Time Monitoring - `enableRealTimeMonitoring`](#enable-real-time-monitoring---enablerealtimemonitoring)
4. [Stream Function Output - `streamFunctionOutput`](#stream-function-output---streamfunctionoutput)
5. [Circuit Breaker - `callFunctionWithCircuitBreaker`](#circuit-breaker---callfunctionwithcircuitbreaker)
6. [Caching Function Results - `cacheFunctionResult`](#caching-function-results---cachefunctionresult)
7. [Invalidate Cache - `invalidateCache`](#invalidate-cache---invalidatecache)
8. [Aggregate Results - `aggregateFunctionResults`](#aggregate-results---aggregatefunctionResults)
9. [Parallel Function Calls - `callFunctionsInParallel`](#parallel-function-calls---callfunctionsinparallel)

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

The `retryFunctionCall` API is used to retry a function call in case of a network failure or function exception. It retries the call up to a specified number of times before throwing an exception if all attempts fail.

#### Parameters:
- `function_name` (str): The name of the function to call.
- `*args` (tuple): Arguments to pass to the function.
- `retries` (int, optional): Number of retry attempts. Default is 3.
- `logging` (bool, optional): Whether or not to log each failure.

#### Global Function:
- Use `set_chance_of_network_failure(float from 0 to 1)` to change the chance of a network failure, by default it is 0.

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

### Enable Real-Time Monitoring - `enableRealTimeMonitoring`

The `enableRealTimeMonitoring` API enables logging of function call details, including start time, end time, and result. This is helpful for tracking function execution in real-time. Also lets you know if there was an exception or not, and if so, what it was. This may behave differently once we are no longer simulating requests.

#### Parameters:
- None

#### Returns:
- None

#### Example Usage:
```python
enableRealTimeMonitoring()
result = add(10, 5)
print(result)  # Should output logs with timestamps.
```

---

### Stream Function Output - `streamFunctionOutput`

The `streamFunctionOutput` API allows real-time streaming of function outputs, which can be useful for long-running operations. However, currently it does not actually do what it will do in the future, rather it just simulates it by sending random messages, followed by at the end the result of the function. In the future, it will output what the function outputs on the backend.

#### Parameters:
- `function_name` (str): The name of the function to call.
- `*args` (tuple): Arguments to pass to the function.

#### Returns:
- An iterator that yields the output in stages.

#### Example Usage:
```python
for message in streamFunctionOutput("add", 5, 2):
    print(message)  # Outputs messages in stages.
```

---

### Circuit Breaker - `callFunctionWithCircuitBreaker`

The `callFunctionWithCircuitBreaker` API prevents repetitive function calls if failures occur, using a failure threshold and cooldown period. Meaning, if you call a function `failure_threshold` amount of times, and each of those times it failed. If you call it again using `callFunctionWithCircuitBreaker` within `cooldown_period` seconds,  it will not let you.

#### Parameters:
- `function_name` (str): The name of the function to call.
- `*args` (tuple): Arguments to pass to the function.
- `failure_threshold` (int): Maximum allowed failures before activating circuit breaker.
- `cooldown_period` (int): Time in seconds to wait after threshold reached.

#### Returns:
- Function result or circuit breaker message.

#### Example Usage:
```python
result = callFunctionWithCircuitBreaker("div", 10, 0, failure_threshold=2, cooldown_period=10)
print(result)  # Expected output: Circuit breaker message after threshold.
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

### Invalidate Cache - `invalidateCache`

The `invalidateCache` API removes a cached result, allowing fresh results to be fetched for subsequent calls.

#### Parameters:
- `function_name` (str): The name of the function.
- `*args` (tuple): Arguments to match the cached function call.

#### Returns:
- None

#### Example Usage:
```python
result = cacheFunctionResult("add", 4, 3, ttl=60)
invalidateCache("add", 4, 3)
result = cacheFunctionResult("add", 4, 3, ttl=60) # Will call the function again, rather than using cached result
```

---

### Aggregate Results - `aggregateFunctionResults`

The `aggregateFunctionResults` API allows multiple function calls to be called, and stored in a single result. Note if two calls are to the same function, only the last one will show up in the results unless you change the name.

#### Parameters:
- `function_calls` (list): A list of dictionaries, each with:
  - `function_name` (str): The name of the function to call.
  - `args` (tuple): Arguments to pass to the function.
  - `name` (str): Name of output in the result

#### Returns:
- List of results for each function call.

#### Example Usage:
```python
function_calls = [
    {"function_name": "add", "args": (10, 5)},
    {"function_name": "mult", "args": (3, 7)}, #Notice that this result gets overridden
    {"function_name": "mult", "args": (5, 2)},
    {"function_name": "sub", "args": (3, 7)},
    {"function_name": "sub", "args": (3, 7), "name": "sub2"}, #Notice that this one does not
]
results = aggregateFunctionResults(function_calls)
print(results)  # Expected output: {"add": 15, "mult": 10, "sub": -4, "sub2": -4}
```

---

### Parallel Function Calls - `callFunctionsInParallel`

The `callFunctionsInParallel` API allows multiple function calls to be made concurrently using threads, making it faster to execute functions that are independent of each other. The result is given in an array, such that each index represents the order the function was in the original `function_calls` array

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
The `register` function allows additional functions to be tested with the advanced features. Note: This is just a temporary development function, and in the future you will not add functions to the Osiris platform this way, this is just so you can add a function to test with.

**Usage:**
```python
def test(a, b):
    return a * b * b

register("test", test)

result = callFunctionsInParallel([
    {"function_name": "add", "args": [1, 2]},
    {"function_name": "test", "args": [5, 2]}
])

print(result)  # Expected output: [3, 20]
```

#### `make_request`
The `make_request` function simulates requests and delays, mimicking real-world latency. This is the function that a majority of the above functions use.

**Usage:**
```python
make_request("add", (2, 3))  # Expected output: 5 after a short delay
```
