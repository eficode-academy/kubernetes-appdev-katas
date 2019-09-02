# Utility functions

import random

def get_random_age():
    return str(random.randint(0,100))

def get_random_name():
    return random.choice(['Graham', 'John', 'Terry', 'Eric', 'Michael'])
