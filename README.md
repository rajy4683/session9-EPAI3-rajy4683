# Namedtuples

The new subclass is used to create tuple-like objects that have fields accessible by attribute lookup as well as being indexable and iterable. Instances of the subclass also have a helpful docstring (with typename and field_names) and a helpful [`__repr__()`](https://docs.python.org/3/reference/datamodel.html#object.__repr__) method which lists the tuple contents in a `name=value` format. 



```
>>> # Basic example
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(11, y=22)     # instantiate with positional or keyword arguments
>>> p[0] + p[1]             # indexable like the plain tuple (11, 22)
33
>>> x, y = p                # unpack like a regular tuple
>>> x, y
(11, 22)
>>> p.x + p.y               # fields also accessible by name
33
>>> p                       # readable __repr__ with a name=value style
Point(x=11, y=22)
```



## TASKS

### Use the [Faker ](https://faker.readthedocs.io/)library to get 10000 random profiles. Using namedtuple, calculate the largest blood type, mean-current_location, oldest_person_age, and average age 

### Solution

```
def generate_fake_lists(count = 10000)
    """
    Generates fake profiles and Returns 2 lists:
        list: List of NamedTuple
        list: List of dicts
    """
```

This is the base function that calls the Faker().profile. For convenience we return both a list of namedtuples and list of dicts. Sample of Faker.profile is as below:

```
{'job': 'IT technical support officer',
 'company': 'Mckinney, Gray and Smith',
 'ssn': '209-22-2764',
 'residence': '75478 Smith Estates Suite 245\nPort Andrew, GA 74768',
 'current_location': (Decimal('15.6842805'), Decimal('-103.190856')),
 'blood_group': 'AB-',
 'website': ['http://www.haynes-lindsey.org/',
  'https://walker-norris.com/',
  'https://www.jones.com/'],
 'username': 'chelseaorozco',
 'name': 'Bethany West',
 'sex': 'F',
 'address': '99714 Mclean Neck Apt. 758\nConnerbury, AK 36335',
 'mail': 'onelson@gmail.com',
 'birthdate': datetime.date(1977, 8, 17)}
```

```
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
```

The above function implements the actual logic of retrieving individual elements and getting following parameters:

1. Most common blood group
2. Average age of the samples. 
3. Old person in the sample.
4. Average Latitude
5. Average longitude

(Note: Faker profile provides a dateofbirth field in datetime format, so age must be calculated by taking delta with current)

### Do the same thing above using a dictionary. Prove that namedtuple is faster

### Solution

```
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
```

Second parameter of above function describes the type of list objects passed.

```
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
```

Single wrapper function that can invoke `calculate_vitals` based on whether elements are list or namedtuples. 

### Create fake data (you can use Faker for company names) for imaginary stock exchange for top 100 companies (name, symbol, open, high, close). Assign a random weight to all the companies. Calculate and show what value the stock market started at, what was the highest value during the day, and where did it end. Make sure your open, high, close are not totally random. You can only use namedtuple. 

### Solution:

```
def generate_company_details(count = 100)
    """
    Returns two lists i.e name of company and stocker ticker of each company
    """
```

First we generate two lists containing random company names and their 4-letter Ticker Symbol. Since the values tend to repeat we generate a larger set and remove duplicates.

```
def generate_market_prices(upper_cutoff=0.6, lower_cutoff=0.6):
    """
    Generates Open, high, low and close prices from a random uniform distribution (1, 10000)
    The upper_cutoff and lower_cutoff are used as max and min bounds based on the open value.
    Basic constraints to be met are:
    1. Open <= High
    2. High >= Low
    """
```

This function generates the real quotes. Basic constraints such as upper/lower cutoff for high/low values and sanity of Open, High, Low and close values are managed.

```
def generate_stock_data(company_name_list, unique_ticker, weights=None)
    """
    Creates a pseudo-stock market status based on the company, list, ticker and weights
    Returns:
        list: generated pseudo stock market data
        float: Open value based on weighted average of the indices
        float: High value based on weighted average of the indices
        float: Low value based on weighted average of the indices
        float: Close value based on weighted average of the indices   
    """
```

Main wrapper function to generate the movement of stock index based on the weights and prices calculated.

## User Details:
Submitted by: Rajesh Y(github: rajy4683)
Email ID: st.hazard@gmail.com
