import http.client

# Define the connection parameters
url = '127.0.0.1:5000'
endpoint = '/api/phase1/'

# Establish a connection to the server
connection = http.client.HTTPConnection(url)

# Send a GET request
connection.request('GET', endpoint)

# Get the response
response = connection.getresponse()

# Print the response status and read the response data
if response.status == 200:
    data = response.read().decode('utf-8')  # Decoding response data assuming it's UTF-8
    print(data)
else:
    print('Failed to fetch data:', response.status)

# Close the connection
connection.close()
