import requests
api_key = 'c0eeb35de313126bb9b4c78690dd0632'
response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getServices')
services = response.json()
# print(services)

response_prices = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getPrices&country=22')
prices = response_prices.json()

# print(prices)
filtered_services_list = []
service_prices = []
common_services = set(services.keys()) & set(prices['22'].keys())

for index, service in enumerate(common_services):
    filtered_services_list.append({
        'index': index,
        # 'service': service,
        'service': services[service],
        'price': list(prices['22'][service].keys())[0],
        # 'service_ID': list(prices['22'][service].values())[0]
        'service_ID': service
    })

for service in filtered_services_list:
    serviceme= service['service']+'  '+service['price']+'₹'
    # print(serviceme)
    print(f"{service['index']}. Service: {service['service']}, Price: {service['price']}, Service_ID: {service['service_ID']}")










































































































import requests
api_key = 'c0eeb35de313126bb9b4c78690dd0632'
response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getServices')
services = response.json()

response_prices = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getPrices&country=22')
prices = response_prices.json()

filtered_services_list = []
service_prices = []
common_services = set(services.keys()) & set(prices['22'].keys())

for index, service in enumerate(common_services, start=1):
    filtered_services_list.append({
        'index': index,
        'service': service,
        'name': services[service],
        'price': list(prices['22'][service].keys())[0],
        # 'service_ID': list(prices['22'][service].values())[0]
        'service_ID': service
    })

for service in filtered_services_list:
    print(f"{service['index']}. Service: {service['service']}, Name: {service['name']}, Price: {service['price']}, ID: {service['service_ID']}")
