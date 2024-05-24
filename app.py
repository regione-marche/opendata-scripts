from urllib.parse import urlparse
import os
import requests

base_url = 'https://dati.regione.marche.it/api/3/action/'
base_folder = 'resources'

def get_filename_from_url(url):
    # Parse the URL to get the path
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Extract the filename from the path
    filename = os.path.basename(path)

    return filename

def download_file_from_url(url, filename):
    # Download file in a folder
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the local file in write-binary mode
        with open(filename, 'wb') as f:
            # Write the response content to the local file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"File downloaded successfully as {filename}")
    else:
        print(f"---- ERROR DOWNLOADING: {response.status_code}")

def download_file_from_resource(package_id, resource_id):
    # Call API GET resource_show
    resourceshow_url = f'{base_url}resource_show?id={resource_id}'
    resourceshow_response = requests.get(resourceshow_url)

    # Check if is 200
    if resourceshow_response.status_code == 200:
        resourceshow = resourceshow_response.json()

        # Check if is successful
        if resourceshow.get('success'):
            resource = resourceshow.get('result', {})

            if isinstance(resource, dict):
                # Print the url of the package
                url = resource.get('url', 'N/A')

                if url is None or url == '':
                    print(f'---- ERROR BROKEN LINK')
                else:
                    filename = get_filename_from_url(url)
                    print(f"filename: {filename}")
                    print(f"url: {url}")

                    # Create the folder if it doesn't exist
                    folder = f'{base_folder}/{package_id}'
                    os.makedirs(folder, exist_ok=True)

                    # Define the filename
                    local_filename = f'{folder}/{resource_id}_{filename}'

                    # Download file from url
                    download_file_from_url(url, local_filename)
            else:
                print("Invalid result format: expected a dictionary")
        else:
            print("API request was not successful. 'success' field is False.")
    else:
        print(f"Failed to retrieve data. HTTP Status code: {resourceshow_response.status_code}")

def download_resources_from_package(package_id):
    # Call API GET package_show
    packageshow_url = f'{base_url}package_show?id={package_id}'
    packageshow_response = requests.get(packageshow_url)

    # Check if is 200
    if packageshow_response.status_code == 200:
        packageshow = packageshow_response.json()

        # Check if is successful
        if packageshow.get('success'):
            package = packageshow.get('result', {})

            if isinstance(package, dict):
                # Print the title of the package
                title = package.get('title', 'N/A')
                print(f"\npackage_id: {package_id}")
                print(f"title: {title}")
                
                # Get package resources
                resources = package.get('resources', [])

                for resource in resources:
                    # Print resource data
                    resource_id = resource.get('id', 'N/A')
                    format = resource.get('format', 'N/A')
                    print(f"resource_id: {resource_id}")
                    print(f"format: {format}")
                    download_file_from_resource(package_id, resource_id)
            else:
                print("Invalid result format: expected a dictionary")
        else:
            print("API request was not successful. 'success' field is False.")
    else:
        print(f"Failed to retrieve data. HTTP Status code: {packageshow_response.status_code}")

def download_resources_from_ckan():
    # Call API GET package_list
    packagelist_url = f'{base_url}package_list'
    packagelist_response = requests.get(packagelist_url)

    # Check if is 200
    if packagelist_response.status_code == 200:
        packagelist = packagelist_response.json()
        
        # Check if is successful
        if packagelist.get('success'):
            packages = packagelist.get('result', [])
            
            # Iterate though each packages
            for package_id in packages:
                download_resources_from_package(package_id)
        else:
            print("API request was not successful. 'success' field is False.")
    else:
        print(f"Failed to retrieve data. HTTP Status code: {packagelist_response.status_code}")

# Create the base folder for resources
os.makedirs(base_folder, exist_ok=True)

# Test single download
#download_resources_from_package('rete-ferroviaria-regionale')

# Download them all
download_resources_from_ckan()
