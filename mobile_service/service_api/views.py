from rest_framework.decorators import api_view
from rest_framework.response import Response
import simplejson as json
import requests
import csv


# get the final result set of all valid operator records
def get_result_set(operator_records):
    result_set = []
    for operator_record in operator_records:
        result_set.append(get_operator_info(operator_record))
    return result_set


# get a list of operator records that have a matching value for LambertX
def operator_record_list(lambertX, operator_list):
    filter_operator_list = operator_list
    operator_records = []
    while True:
        index = binary_search(lambertX, filter_operator_list)
        if index or index == 0:
            temp_operator_data = []
            for i in range(6):
                temp_operator_data.append(filter_operator_list[index][i])
            operator_records.append(temp_operator_data)
            filter_operator_list.pop(index)
        else:
            break
    return operator_records



# get Lambert93 X coordinate from the query address
def get_address_lambertX(address_list):
    address = address_list[0]
    lambertX = address['properties']['x']
    return int(float(lambertX))


# get operator names from their codes
def get_operator_name(operator_code):
    if int(operator_code) == 20801:
        return 'Orange'
    elif int(operator_code) == 20810:
        return 'SFR'
    elif int(operator_code) == 20815:
        return 'Free'
    elif int(operator_code) == 20820:
        return 'Bouygues Telecom'


# get information about an operator
def get_operator_info(operator_record):
    operator_name = get_operator_name(operator_record[0])
    availability_2G = 'true' if operator_record[3] == '1' else 'false'
    availability_3G = 'true' if operator_record[4] == '1' else 'false'
    availability_4G = 'true' if operator_record[5] == '1' else 'false'
    return {'name': operator_name, '2G': availability_2G, '3G': availability_3G, '4G': availability_4G}


# read operators.csv and create a list of operators
def read_csv_file(filename):
    operator_list = []
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # skip the headers of the csv file
        next(csv_reader)
        for operator in csv_reader:
            operator_list.append(operator)
    return operator_list


# binary search to quickly search for matching operator in operator list
def binary_search(lambert_x, operator_list):
    list_size = len(operator_list)
    low_index = 0
    high_index = list_size - 1
    while low_index <= high_index:
        mid_index = int((high_index + low_index) / 2)
        if int(operator_list[mid_index][1]) < lambert_x:
            low_index = mid_index + 1
        elif int(operator_list[mid_index][1]) > lambert_x:
            high_index = mid_index - 1
        else:
            return mid_index



# API endpoint for retrieving address details
api_search = 'https://api-adresse.data.gouv.fr/search/?limit=20'


@api_view(['GET'])
def network_view(request):
    # get list of operators from csv file (performed only once when we first load the server)
    OPERATOR_LIST = read_csv_file('../operators.csv')

    # get query parameter 'q' containing address from url
    query_address = request.query_params['q']

    # fetch address with query parameter & limit=1 to get the best address (addresses are already sorted with max score values)
    params = {'q': query_address, 'limit': 1}
    get_address_detail = requests.get(api_search, params=params)

    # convert data in json format to python native object
    query_address_result = json.loads(get_address_detail.text)

    # filter for only data about the address
    address_result_set = query_address_result['features']

    if len(address_result_set) == 0:
        return Response({"message": f"Sorry, No Operator Info was found for the address '{query_address}'"})
    else:
        lambertX = get_address_lambertX(address_result_set)
        print(lambertX)
        operator_records = operator_record_list(lambertX, OPERATOR_LIST)
        result = get_result_set(operator_records)
        if len(result) == 0:
            return Response({'message': f"Sorry, no info was found for the address '{query_address}'"})
        return Response({'count': len(result), 'search_param': query_address, 'data': result})
