# from django.test import TestCase
from unittest import TestCase

# Create your tests here.


def sum_two(a, b):
    return a + b


class TestSum(TestCase):
    def test_sum_two(self):
        self.assertEqual(sum_two(1, 2), 3)
