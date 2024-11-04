import unittest
import sys
import threading
from unittest.mock import patch
import time
sys.path.insert(0, "../")

import advancedfeatures as client

class API1Tests(unittest.TestCase):

    def test_expected_response(self):
        res = client.callFunctionBatch([{"function_name": "mult", "args": [5,6]}])
        self.assertEqual(res, [30])
        res = client.callFunctionBatch([{"function_name": "add", "args": [1,2]}, {"function_name": "sub", "args": [4,2]}])
        self.assertEqual(res, [3, 2])
        res = client.callFunctionBatch([{"function_name": "sub", "args": [1000,40]}, {"function_name": "add", "args": [4,10]}])
        self.assertEqual(res, [960, 14])
        
    def test_errors(self):
        res = client.callFunctionBatch([{"function_name": "add", "args": [1]}, {"function_name": "not_a_function", "args": []}, {"function_name": "div", "args": [1,0]}])
        self.assertTrue(type(res[0]) == client.FunctionRequestError and "TypeError" in str(res[0]))
        self.assertTrue(type(res[1]) == ValueError)
        self.assertTrue(type(res[2]) == client.FunctionRequestError and "ZeroDivisionError" in str(res[2]))


class API2Tests(unittest.TestCase):
    def test_retry_success(self):
        client.chance_of_network_failure = 0
        global count
        count = 0
        def check_thread():
            global count
            try:
                result = client.retryFunctionCall("add", 5, 5, retries=3, logging=False)
                if result == 10:
                    count+=1
            except Exception as err:
                pass
        threads = []
        for i in range(100):
            thread = threading.Thread(target=check_thread)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        self.assertEqual(count, 100)

    def test_retry_failure(self):
        client.chance_of_network_failure = 1
        global count
        count = 0
        def check_thread():
            global count
            try:
                result = client.retryFunctionCall("add", 5, 5, retries=3, logging=False)
            except:
                count+=1
                pass
        threads = []
        for i in range(100):
            thread = threading.Thread(target=check_thread)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        self.assertEqual(count, 100)

class API5Tests(unittest.TestCase):
    def setUp(self):
        if hasattr(client.callFunctionWithCircuitBreaker, 'failure_count'):
            client.callFunctionWithCircuitBreaker.failure_count = {}
        if hasattr(client.callFunctionWithCircuitBreaker, 'last_failure_time'):
            client.callFunctionWithCircuitBreaker.last_failure_time = {}
    
    def test_successful_call(self):
        result = client.callFunctionWithCircuitBreaker("add", 5, 5, failure_threshold=3, cooldown_period=2)
        self.assertEqual(result, 10)

    def test_circuit_breaker_triggered(self):
        client.register("div", client.div)

        for _ in range(2):  
            try:
                client.callFunctionWithCircuitBreaker("div", 10, 0, failure_threshold=3, cooldown_period=5)
                self.assertTrue(False)
            except Exception as err:
                print(err)
                print(client.callFunctionWithCircuitBreaker.failure_count)
                self.assertTrue(isinstance(err, client.FunctionRequestError))

        try:
            client.callFunctionWithCircuitBreaker("div", 10, 0, failure_threshold=3, cooldown_period=5)
            self.assertTrue(False)
        except Exception as err:
            self.assertTrue(isinstance(err, Exception) and "Circuit breaker triggered" in str(err))

    def test_circuit_breaker_resets_after_cooldown(self):
        client.register("div", client.div)
        
        for _ in range(3):  
            with self.assertRaises(Exception):
                client.callFunctionWithCircuitBreaker("div", 10, 0, failure_threshold=3, cooldown_period=2)
        
        time.sleep(2)

        try:
            result = client.callFunctionWithCircuitBreaker("div", 10, 2, failure_threshold=3, cooldown_period=2)
            self.assertEqual(result, 5)  
        except Exception as context:
            self.fail(f"Expected successful call after cooldown but got exception: {str(context)}")

class API6Tests(unittest.TestCase):
    def setUp(self):
        # Clear the cache before each test
        if hasattr(client.cacheFunctionResult, "cache"):
            del client.cacheFunctionResult.cache

    def test_cache_hit(self):
        global callcount
        callcount = 0
        def temp_test(a,b):
            global callcount
            callcount+=1
            return a+b
        client.register("add2",temp_test)
        result1 = client.cacheFunctionResult("add2", 7, 8)
        result2 = client.cacheFunctionResult("add2", 7, 8)
        self.assertEqual(result1, 15)
        self.assertEqual(result2, 15)
        self.assertEqual(callcount, 1)  # Cached, so only called once

    def test_cache_miss_due_to_expiry(self):
        global callcount
        callcount = 0
        def temp_test(a,b):
            global callcount
            callcount+=1
            return a+b
        client.register("add2",temp_test)
        result1 = client.cacheFunctionResult("add2", 7, 8, ttl=0.5)
        self.assertEqual(result1, 15)  # This should compute 7 + 8

        time.sleep(1)  # Wait for cache to expire

        result2 = client.cacheFunctionResult("add2", 7, 8, ttl=0.5)
        self.assertEqual(result2, 15)  # This should compute 7 + 8 again after expiry
        
        self.assertEqual(callcount, 2)

    def test_cache_error_handling(self):
        try:
            res = client.cacheFunctionResult("div", 10, 0)
            self.assertTrue(False)
        except Exception as err:
            self.assertTrue(type(err) == client.FunctionRequestError and "ZeroDivisionError" in str(err))


class API9Tests(unittest.TestCase):

    def test_expected_response(self):
        res = client.callFunctionsInParallel([{"function_name": "mult", "args": [5,6]}])
        self.assertEqual(res, [30])
        res = client.callFunctionsInParallel([{"function_name": "add", "args": [1,2]}, {"function_name": "sub", "args": [4,2]}])
        self.assertEqual(res, [3, 2])
        res = client.callFunctionsInParallel([{"function_name": "sub", "args": [1000,40]}, {"function_name": "add", "args": [4,10]}])
        self.assertEqual(res, [960, 14])
        
    def test_errors(self):
        res = client.callFunctionsInParallel([{"function_name": "add", "args": [1]}, {"function_name": "not_a_function", "args": []}, {"function_name": "div", "args": [1,0]}])
        self.assertTrue(type(res[0]) == client.FunctionRequestError and "TypeError" in str(res[0]))
        self.assertTrue(type(res[1]) == ValueError)
        self.assertTrue(type(res[2]) == client.FunctionRequestError and "ZeroDivisionError" in str(res[2]))


if __name__ == '__main__':
    unittest.main()