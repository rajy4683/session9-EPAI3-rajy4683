from faker import Faker
from collections import namedtuple
import random
import numpy as np
from datetime import datetime

single_stock_type = namedtuple('Ticker',"""Company Symbol Open High Low Close Weight""")
named_profile = namedtuple('Profile',
['job',
'company',
'ssn',
'residence',
'current_location',
'blood_group',
'website',
'username',
'name',
'sex',
'address',
'mail',
'birthdate'])

def generate_company_details(count = 100):
    """
    Returns two lists i.e name of company and stocker ticker of each company
    """
#     stocks_list = []
    unique_ticker = []
    company_name_list=[]
    fake = Faker()
    Faker.seed(0)
    for _ in range(count*3):
        company_name = fake.company()
        ticker = company_name.split(" ")[0][:4].upper()
        if ticker in unique_ticker or company_name in company_name_list:
            print("Already present", company_name, ticker)       
        else:
    #         validated_stock_entry = single_stock_type(company_name, ticker,*[None]*4)
    #         stocks_list.append(validated_stock_entry)
            unique_ticker.append(ticker)
            company_name_list.append(company_name)
    return company_name_list[:count], unique_ticker[:count]

def generate_market_prices(upper_cutoff=0.6, lower_cutoff=0.6):
    """
    Generates Open, high, low and close prices from a random uniform distribution (1, 10000)
    The upper_cutoff and lower_cutoff are used as max and min bounds based on the open value.
    Basic constraints to be met are:
    1. Open <= High
    2. High >= Low
    """
    if(upper_cutoff < 0 or lower_cutoff < 0 or lower_cutoff > 1 or upper_cutoff > 2):
        raise ValueError

    open_price = random.uniform(1, 10000)
    random_high_price = random.uniform(open_price, open_price*(1+upper_cutoff))

    min_low_price_range = open_price*(1-lower_cutoff)
    random_low_price = random.uniform(min_low_price_range, random_high_price)
    close_price = random.uniform(min([random_low_price,open_price,random_high_price]), max([random_low_price,open_price,random_high_price]))
    high_price=max([open_price, random_high_price, random_low_price, close_price])
    low_price=min([open_price, random_high_price, random_low_price, close_price])
    return open_price, high_price, low_price, close_price

def generate_stock_data(company_name_list, unique_ticker, weights=None):
    """
    Creates a pseudo-stock market status based on the company, list, ticker and weights
    Returns:
        list: generated pseudo stock market data
        float: Open value based on weighted average of the indices
        float: High value based on weighted average of the indices
        float: Low value based on weighted average of the indices
        float: Close value based on weighted average of the indices   
    """
    stocks_list = []
    ticker_length = len(unique_ticker)
    company_name_list_length = len(company_name_list)
    if(company_name_list_length != ticker_length):
        print("Length of company list{company_name_list_length} doesn't match length of ticker length {ticker_length}")
        raise Exception
    if(weights is None):
        weights = np.random.random_sample((ticker_length,)).round(2)
    for company_name,ticker,weight in zip(company_name_list, unique_ticker, weights):
        price_list = generate_market_prices()
        stocks_list.append(single_stock_type(company_name, ticker,*price_list,weight))

    open_total = high_total = low_total = close_total = total_weight = 0.0
    for single_stock in stocks_list:
        open_total += single_stock.Open*single_stock.Weight
        high_total += single_stock.High*single_stock.Weight
        low_total += single_stock.Low*single_stock.Weight
        close_total += single_stock.Close*single_stock.Weight
        total_weight += single_stock.Weight
    return stocks_list, open_total/total_weight, high_total/total_weight,low_total/total_weight,close_total/total_weight

def generate_fake_lists(count = 10000):
    """
    Generates fake profiles and Returns 2 lists:
        list: List of NamedTuple
        list: List of dicts
    """
    profile_list = []
    profile_dict_list = []
    fake = Faker()
    Faker.seed(0)
    for _ in range(count):
        current_entry = fake.profile()
        profile_list.append(named_profile(**current_entry))
        profile_dict_list.append(current_entry)
    return profile_list, profile_dict_list

def calculate_vitals(profile_list: list, profile_element_type: type):
    """
    Inner function that performs the real calculations.
    Inputs:
        list: List of dicts or List of namedtuple
        type: Type of the element
    Output:
        str: most common blood_group
        float: average age of the profiles in the list
        int: age of the oldest member in the list
        float: average latitude
        float: average longitude
    """
    bg_count = {'B+':0, 'O-':0, 'AB-':0, 'A-':0, 'AB+':0, 'A+':0, 'O+':0, 'B-':0}
    current_date = datetime.date(datetime.now())
    oldest_member_age = 0
    age_sum = 0.
    current_pos_long_sum = 0.
    current_pos_lat_sum = 0.
    mean_gregorian_years = 365.245
    if not isinstance(profile_list, list):
        print("Expecting a list of namedtuples")
        raise TypeError
    for list_entry in profile_list:
        if not isinstance(list_entry, profile_element_type):
            print(f"Element is not of valid type {profile_element_type}")
            raise TypeError
        if (profile_element_type == dict):
            _,_,_,_,current_pos,blood_group, _, _,name,*_,dob = list_entry.values()
        else:
            _,_,_,_,current_pos,blood_group, _, _,name,*_,dob = list_entry
        bg_count[blood_group] += 1### Adding the blood group
        current_pos_lat_sum += float(current_pos[0])
        current_pos_long_sum += float(current_pos[1])
        current_profile_age = (current_date - dob).days 
        age_sum += current_profile_age            
        if current_profile_age > oldest_member_age:
            oldest_member_age = current_profile_age
    bg_count = dict(sorted(bg_count.items(), key=lambda item: item[1]))
    return bg_count.popitem()[0],\
            age_sum/(mean_gregorian_years*len(profile_list)), \
            int(oldest_member_age/mean_gregorian_years), \
            current_pos_lat_sum/len(profile_list),\
            current_pos_long_sum/len(profile_list)

def retrieve_details_for_tuple(profile_list: list):
    """
    Wrapper function that takes a list of dicts or a list of namedtuples
    and returns the following:
    str: most common blood_group
    float: average age of the profiles in the list
    int: age of the oldest member in the list
    float: average latitude
    float: average longitude
    """
    ### take a random element from the list and retrieve the type
    element_type = type(profile_list[random.randint(1, len(profile_list)-1)])
    #     print(f"Elements are of type {element_type}")
    return calculate_vitals(profile_list, element_type)