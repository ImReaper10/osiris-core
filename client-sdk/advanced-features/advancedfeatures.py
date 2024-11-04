import time
import random
import threading
import contextlib
import io
import sys
from typing import Iterator
from datetime import datetime

#API 1
def callFunctionBatch(function_calls: list) -> list:
    results = []
    for call in function_calls:
        results.append(make_request(call["function_name"],call["args"]))
    return results


chance_of_network_failure = 0

# API 2
def retryFunctionCall(function_name: str, *args, retries: int = 3, logging: bool = True) -> any:
    attempt = 0
    while attempt < retries:
        if random.uniform(0, 1) < chance_of_network_failure:
            if logging:
                print(f"Attempt {attempt + 1} failed due to network failure")
            attempt += 1
            if attempt < retries:
                time.sleep(2)
        else:
            res = make_request(function_name, args)  
            if isinstance(res,Exception):
                if logging:
                    print(f"Attempt {attempt + 1} failed: " + str(res))
                attempt+=1
                if attempt < retries:
                    time.sleep(2)
            else:
                return res
    raise Exception(f"All {retries} retries failed.")

# API 3
real_time_monitoring = False
def enableRealTimeMonitoring() -> None:
    global real_time_monitoring
    real_time_monitoring = True
    
# API 4
def streamFunctionOutput(function_name: str, *args: list) -> Iterator:
    return make_request_2(function_name, *args)

# API 5 
def callFunctionWithCircuitBreaker(function_name: str, *args: list, failure_threshold: int = 5, cooldown_period: int = 60) -> any:
    if not hasattr(callFunctionWithCircuitBreaker, 'failure_count'):
        callFunctionWithCircuitBreaker.failure_count = {}
    if not hasattr(callFunctionWithCircuitBreaker, 'last_failure_time'):
        callFunctionWithCircuitBreaker.last_failure_time = {}

    current_time = time.time()

    if function_name in callFunctionWithCircuitBreaker.last_failure_time:
        time_since_last_failure = current_time - callFunctionWithCircuitBreaker.last_failure_time[function_name]
        if time_since_last_failure < cooldown_period and callFunctionWithCircuitBreaker.failure_count[function_name] >= failure_threshold:
            raise Exception(f"Circuit breaker triggered after {failure_threshold} failed attempts. Please try again after {cooldown_period - time_since_last_failure} seconds.")
        elif time_since_last_failure > cooldown_period and callFunctionWithCircuitBreaker.failure_count[function_name] >= failure_threshold:
            callFunctionWithCircuitBreaker.failure_count[function_name] = 0 # Cooldown is over
    
    try:
        result = make_request(function_name, args)
        if isinstance(result, Exception):
             raise result
        callFunctionWithCircuitBreaker.failure_count[function_name] = 0
        return result
    except FunctionRequestError as err:
        current_time = time.time()
        callFunctionWithCircuitBreaker.failure_count[function_name] = callFunctionWithCircuitBreaker.failure_count.get(function_name, 0) + 1
        callFunctionWithCircuitBreaker.last_failure_time[function_name] = current_time

        if callFunctionWithCircuitBreaker.failure_count[function_name] >= failure_threshold:
            raise Exception(f"Circuit breaker triggered after {failure_threshold} failed attempts for '{function_name}'. Please try again later.")

        raise err

# API 6
def cacheFunctionResult(function_name: str, *args, ttl: int = 300) -> any:
    if not hasattr(cacheFunctionResult, "cache"):
        cacheFunctionResult.cache = {} 
    cache_key = (function_name, args)
    current_time = time.time()
    if cache_key in cacheFunctionResult.cache:
        result, expiry = cacheFunctionResult.cache[cache_key]
        if current_time < expiry:
            return result 
    result = make_request(function_name, args)
    if isinstance(result, Exception):
        raise result
    cacheFunctionResult.cache[cache_key] = (result, current_time + ttl)
    return result


# API 7
def invalidateCache(function_name: str, *args: list) -> None:
    if not hasattr(cacheFunctionResult, "cache"):
        return
    cache_key = (function_name, tuple(args))
    if cache_key in cacheFunctionResult.cache:
        del cacheFunctionResult.cache[cache_key]

# API 8
def aggregateFunctionResults(function_calls: list) -> dict:
    results = {}
    for call in function_calls:
        function_name = call.get("function_name")
        name = call.get("name", function_name)
        results[name] = make_request(function_name, call["args"])
    return results

#API 9
def callFunctionsInParallel(function_calls: list) -> list:
    threads = []
    results = [None]*len(function_calls)
    i = 0
    def thread_setup(a,b,c):
        results[c] = make_request(a,b)
    for call in function_calls:
        thread = threading.Thread(target=thread_setup, args=(call["function_name"],call["args"],i))
        thread.start()
        threads.append(thread)
        i+=1
    for thread in threads:
        thread.join()
    return results
        

#For now use this to make our requests until we have something we can actually connect to, also note that for API 4, I think we have to modify this function a bit
#For now if there is an error, I simply have this function return that error, this will be changed when we have something to connect to and know how exactly errors that we get will be given to us
#Example usage: make_request("add", (1,2))
def make_request(function_name, args):
    time.sleep(random.uniform(0.5, 1.5))
    if real_time_monitoring:
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{start_time}] Starting \"{function_name}\" with args: {args}")
    func = globals().get(function_name)
    if func is None:
        if real_time_monitoring:
            print(f"Function '{function_name}' not found.\n")
        return ValueError(f"Function \"{function_name}\" not found.")
    try:
        result = func(*args)
        if real_time_monitoring:
            execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{execution_time}] \"{function_name}\" executed- Result: {result}")
        return result
    except Exception as err:
        if real_time_monitoring:
            execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{execution_time}] \"{function_name}\" resulted in an exception- {type(err).__name__}: {err}")
        return FunctionRequestError(function_name, args, err)

#For API 4 
def make_request_2(function_name, args):
    func = globals().get(function_name)
    if func is None:
        yield ValueError(f"Function '{function_name}' not found.")
        return
    
    yield "Starting function execution..."
    time.sleep(random.uniform(0.5, 1.5))

    try:
        if callable(func):
            yield "Processing report..."
            time.sleep(random.uniform(0.5, 1.5))
            yield "Fetching data..."
            time.sleep(random.uniform(0.5, 1.5))
            yield "Finalizing..."
            time.sleep(random.uniform(0.5, 1.5))

            result = func(*args)
            try:
                yield func(*args)
            except Exception as err:
                yield FunctionRequestError(function_name, args, err)
        else:
            yield ValueError(f"Function '{function_name}' is not callable.")
    except Exception as err:
        yield err

def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mult(a,b):
    return a*b

def div(a,b):
    return a/b

class FunctionRequestError(Exception):
    def __init__(self, function_name, args, error):
        error_message = (
            f"Function '{function_name}' with args {args} "
            f"returns a {type(error).__name__} exception with message: {str(error)}"
        )
        super().__init__(error_message)

#This is just a temp function for registering a function from another place if you wanted to add more functions to test with
def register(fname, func):
    globals()[fname] = func

def set_chance_of_network_failure(chance):
    global chance_of_network_failure
    chance_of_network_failure = chance
