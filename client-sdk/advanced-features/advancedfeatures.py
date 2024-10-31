import time
import random
import threading
import contextlib
import io
import sys

#API 1
def callFunctionBatch(function_calls: list) -> list:
    results = []
    for call in function_calls:
        results.append(make_request(call["function_name"],call["args"]))
    return results


# API 2
def retryFunctionCall(function_name: str, *args, retries: int = 3) -> any:
    attempt = 0
    while attempt < retries:
        result = make_request(function_name, args)
        if isinstance(result, Exception):
            print(f"Attempt {attempt + 1} failed: {result}")
            attempt += 1
            if attempt < retries:
                time.sleep(2)
        else:
            return result      
    raise Exception(f"All {retries} retries failed.")


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
    func = globals().get(function_name)
    if func is None:
        return ValueError(f"Function '{function_name}' not found.") #TODO: replace this part here with a standardized error handling for function not found *possibly*
    try:
        return func(*args)
    except Exception as err:
        return err

def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mult(a,b):
    return a*b

def div(a,b):
    return a/b
