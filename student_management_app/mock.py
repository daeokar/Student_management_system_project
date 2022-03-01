import unittest

def add(a , b):
    try :
        c = a+b
        return c
    except ValueError:
        print("invalid")



class AddTest(unittest.TestCase):   # TestClass --- 
    def test_add_with_two_int(self): # instance method                          # testcase  --- test
        res = add(10, 20)
        self.assertNotEqual(res, 40)  # actual_value, expected value

    def test_add_with_two_str(self):
        res = add("Python", " Language")
        self.assertEqual(res, "Python Language")

    def test_add_with_int_str(self):  
        res = add(10, " Language")
        self.assertEqual(res, "Invalid Inputs")


a = AddTest()
print(a)

