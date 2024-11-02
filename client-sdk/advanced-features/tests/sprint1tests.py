import unittest
import sys

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
        self.assertTrue(type(res[0]) == TypeError)
        self.assertTrue(type(res[1]) == ValueError)
        self.assertTrue(type(res[2]) == ZeroDivisionError)
        
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
        self.assertTrue(type(res[0]) == TypeError)
        self.assertTrue(type(res[1]) == ValueError)
        self.assertTrue(type(res[2]) == ZeroDivisionError)

if __name__ == '__main__':
    unittest.main()