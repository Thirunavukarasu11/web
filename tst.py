1. How to find the first non-repeated character in a string?

def first_non_repeated_char(a):
    for char in a :
       if a.count(char) == 1:
        return char
    return None

string = "applieddatafinance"
result = first_non_repeated_char(string)
print("repeated char is :",result)

O/P: repeated char is l

2. Write a program to get distinct elements from an array by avaoiding duplicate elements.
Ex: String arr[]={“vignesh”,”vinoth”,”vinitha”,”ramesh”,”vignesh”,”vinoth”,”vinitha”}

arr = ["vignesh", "vinoth", "vinitha", "ramesh", "vignesh", "vinoth", "vinitha"]

def get_distinct_elements (arr):
    return list(set(arr))

distinct_elements = get_distinct_elements(arr)
print("distinct_elements :",distinct_elements)

O/P : distinct_elements : ['vignesh', 'ramesh', 'vinitha', 'vinoth']