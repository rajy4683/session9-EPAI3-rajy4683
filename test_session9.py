from session9 import *
from datetime import datetime
import pytest
from io import StringIO 
import sys
import time
import inspect
import os
import session9
import re
from faker import Faker
from time import perf_counter

README_CONTENT_CHECK_FOR = [
    "generate_company_details",
    "generate_market_prices",
    "generate_stock_data",
    "generate_fake_lists",
    "calculate_vitals",
    "retrieve_details_for_tuple"
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session9)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        # if (len(space) % 4 == 2):
        #     print("Your script contains misplaced indentations", space)
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


def test_generate_company_details():
    """
    Checks whether the generate_company_details performs as intended
    """
    max_count = 200
    a,b = session9.generate_company_details(max_count)
    assert len(a) == len(b), "Config error: Company and Ticker arrays are mismatched"
    assert len(a) == max_count or len(b) != max_count, "Config error: Didn't get valid lengths"

def test_generate_market_prices():
    """
    Checks whether the generate_market_prices gives acceptable values given the conditions
    """
    out_put = session9.generate_market_prices()
    assert len(out_put) == 4, "Wrong number of output parameters" 
    max_count = 200

    open,high,low,close = session9.generate_market_prices()
    
    assert high >= low or high >= open, "Price error: High must be greater than or equal to low/open "

    max_cutoff = 0.2
    min_cutoff = 0.2
    open,high,low,close = session9.generate_market_prices(max_cutoff, min_cutoff)
    assert high <= open*(1+max_cutoff), "Price error: High price should be within upper cutoff"
    assert low >= open*(1 - min_cutoff), "Price error: Low price shouldn't be greater than min cutoff"

    max_cutoff = -0.2
    min_cutoff = 0.2
    with pytest.raises(ValueError) as execinfo:
        session9.generate_market_prices(max_cutoff, min_cutoff)

    max_cutoff = 0.5
    min_cutoff = -0.2
    with pytest.raises(ValueError) as execinfo:
        session9.generate_market_prices(max_cutoff, min_cutoff)

def test_generate_stock_data():
    """
    To test the working of final stock data generator function: generate_stock_data
    """
    max_count = 200
    comp_list,tick_list = session9.generate_company_details(max_count)
    
    with pytest.raises(Exception) as execinfo:
        session9.generate_stock_data(comp_list,tick_list[:-1])

    all_out = session9.generate_stock_data(comp_list,tick_list)
    assert len(all_out) == 5, "Ticker error: Expecting 5 outputs: stock_market_list, open, high, low, close"

    all_stocks,*_  = session9.generate_stock_data(comp_list,tick_list)
    assert all_stocks[0]._fields == session9.single_stock_type._fields, "Ticker Error: Fields mismatched"
    assert len(all_stocks) == max_count, "Ticker error: Didn't get expected number of Tickers"
    # assert len(all_out) == 5, "Ticker error: Expecting 5 outputs: stock_market_list, open, high, low, close"

def test_generate_fake_lists():
    """
    To test the working of profile generator
    """    
    max_count = 20
    all_out = session9.generate_fake_lists(max_count)
    mandatory_fields = ['current_location', 'blood_group','name', 'birthdate']
    
    # print(type(all_out[0]))
    assert len(all_out) == 2  and len(all_out[0]) == max_count and len(all_out[1]) == max_count, "Profile Gen Error: Wrong output parameters"
    assert all_out[0][0]._fields == session9.named_profile._fields, "Profile Error: Fields are mismatched"
    assert list(all_out[0][0]._fields) == list(Faker().profile().keys()), "Profile Error: Fields differ from Faker fields"
    assert any([True if i in list(all_out[0][0]._fields) else False for i in mandatory_fields ]) == True, "Profile Error: Mandatory fields missing"

def test_retrieve_details_for_tuple():
    max_count = 100
    profile_tuple, profile_dict = session9.generate_fake_lists(max_count)
    start_tuple = perf_counter()
    session9.retrieve_details_for_tuple(profile_tuple)
    end_tuple=perf_counter()
    diff_tuple = end_tuple - start_tuple

    start_dict = perf_counter()
    session9.retrieve_details_for_tuple(profile_dict)
    end_dict=perf_counter()
    diff_dict = end_dict - start_dict
    assert abs(round(1000*diff_dict,2) - round(1000*diff_tuple,2)) < 2, "SpeedTest: Tuples must be faster"

def test_calculate_vitals():
    profile_list_dict = [ Faker().profile() ]*4
    curr_time = datetime.date(datetime.now())
    curr_age = curr_time - profile_list_dict[0]['birthdate']
    oldest_val = int(curr_age.days/365.245)
    curr_lat = float(profile_list_dict[0]['current_location'][0])
    curr_long = float(profile_list_dict[0]['current_location'][1])

    bg,avg_age, oldest, avg_lat, avg_long = session9.calculate_vitals(profile_list_dict, type(profile_list_dict[0]))
    assert bg == profile_list_dict[0]['blood_group'], "Vitals Error: Parameter Most Common Blood Group is not expected"
    assert oldest == oldest_val, "Vitals Error: Parameter oldest age is not valid"
    assert round(curr_lat, 2) == round(avg_lat, 2), "Vitals Error: location average is not valid"
    assert round(curr_long, 2) == round(avg_long, 2), "Vitals Error: location average is not valid"