from urllib.parse import urlparse
import os
import requests

base_url = 'https://dati.regione.marche.it/api/3/action/'
base_folder = 'resources'


def check_package(package_id):
    # Call API GET package_show
    url = f'{base_url}package_show?id={package_id}'
    response = requests.get(url)

    # Check if is 200
    if response.status_code == 200:
        packageshow = response.json()

        # Check if is successful
        if packageshow.get('success'):
            package = packageshow.get('result', {})

            if isinstance(package, dict):
                # Get the title of the package
                title = package.get('title', 'N/A')

                # Get package resources
                resources = package.get('resources', [])

                for resource in resources:
                    # Get resource data
                    resource_id = resource.get('id', 'N/A')
                    format = resource.get('format', 'N/A')

                    # Check if the resource is CSV
                    if (format == 'CSV'):
                        # Print resource row (CSV style)
                        print(f'{package_id},{title},{resource_id},{format}')
            else:
                print('Invalid result format: expected a dictionary')
        else:
            print('API request was not successful. "success" field is False.')
    else:
        print(f'---- GET package_show ERROR: {response.status_code}')


def get_csv_packages():
    # Call API GET package_list
    url = f'{base_url}package_list'
    response = requests.get(url)

    # Check if is 200
    if response.status_code == 200:
        packagelist = response.json()

        # Check if is successful
        if packagelist.get('success'):
            packages = packagelist.get('result', [])

            # Print the results header (CSV style)
            print('package_id,title,resource_id,format')

            # Iterate though each packages
            for package_id in packages:
                check_package(package_id)
        else:
            print('API request was not successful. "success" field is False.')
    else:
        print(f'---- GET package_show ERROR: {response.status_code}')


# Create the base folder for resources
os.makedirs(base_folder, exist_ok=True)

# Get CSV packages
get_csv_packages()
