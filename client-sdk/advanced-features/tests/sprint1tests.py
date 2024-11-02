import unittest
import sys
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
    @patch("advancedfeatures.make_request")
    def test_retry_success(self, mock_request):
      # Simulate 2 failures and then a success
      mock_request.side_effect = [Exception("Network error"), Exception("Network error"), 10]
      result = client.retryFunctionCall("add", 5, 5, retries=3)
      self.assertEqual(result, 10)
      self.assertEqual(mock_request.call_count, 3)  # Ensure all attempts were made


    @patch("advancedfeatures.make_request")
    def test_retry_failure(self, mock_request):
        # Always fail
        mock_request.side_effect = Exception("Network error")
        with self.assertRaises(Exception) as context:
            client.retryFunctionCall("add", 5, 5, retries=3)
        self.assertEqual(str(context.exception), "All 3 retries failed.")
        self.assertEqual(mock_request.call_count, 3)  # Confirm it retries 3 times


class API6Tests(unittest.TestCase):
    def setUp(self):
        # Clear the cache before each test
        if hasattr(client.cacheFunctionResult, "cache"):
            del client.cacheFunctionResult.cache

    @patch("advancedfeatures.make_request")
    def test_cache_hit(self, mock_request):
        mock_request.return_value = 15
        result1 = client.cacheFunctionResult("add", 7, 8)
        result2 = client.cacheFunctionResult("add", 7, 8)
        self.assertEqual(result1, 15)
        self.assertEqual(result2, 15)
        self.assertEqual(mock_request.call_count, 1)  # Cached, so only called once

    @patch("advancedfeatures.make_request")
    def test_cache_miss_due_to_expiry(self, mock_request):
        mock_request.return_value = 15
        result1 = client.cacheFunctionResult("add", 7, 8, ttl=0.5)
        self.assertEqual(result1, 15)  # This should compute 7 + 8

        time.sleep(1)  # Wait for cache to expire

        result2 = client.cacheFunctionResult("add", 7, 8, ttl=0.5)
        self.assertEqual(result2, 15)  # This should compute 7 + 8 again after expiry
        
        # Check that make_request was called twice (once for each call to cacheFunctionResult)
        self.assertEqual(mock_request.call_count, 2)

    @patch("advancedfeatures.make_request")
    def test_cache_error_handling(self, mock_request):
        mock_request.side_effect = Exception("Calculation error")
        with self.assertRaises(Exception) as context:
            client.cacheFunctionResult("div", 10, 0)
        self.assertEqual(str(context.exception), "Calculation error")
        self.assertEqual(mock_request.call_count, 1)


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