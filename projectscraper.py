import os
import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json

# Load .env file
load_dotenv()

# Get the username and password
username = os.getenv('UNI_USERNAME')
password = os.getenv('UNI_PASSWORD')

def get_web_page(url):
    print(f'Fetching page: {url}')
    response = requests.get(url, auth=(username, password), timeout=5)
    return BeautifulSoup(response.text, 'html.parser')

def get_project_links(soup):
    # Find the ordered list by id
    ol = soup.find('ol', attrs={'id': 'projs'})

    # Create an empty list to hold the project data
    project_data = []

    # If the ordered list exists
    if ol:
        print('Ordered list found')
        # Loop over each list item in the ordered list
        for li in ol.find_all('li'):
            # Get the anchor tag within the list item
            a = li.find('a')
            # If an anchor tag exists
            if a:
                # Get the link and text
                link = 'https://campus.cs.le.ac.uk/teaching/proposals/' + a['href']
                text = a.text
                project_data.append({'link': link, 'title': text})
    else:
        print('Ordered list with id "projs" not found')
        print(soup)

    return project_data

def get_project_info(url):
    time.sleep(2)  # Delay for 2 seconds
    soup = get_web_page(url)

    project_info = {}

    h3_tags = soup.find_all('h3')

    for tag in h3_tags:
        # Get the section title
        section_title = tag.text.strip()

        # Get the section text
        div = tag.find_next_sibling('div')
        if div:
            section_text = div.text.strip()

        # Add the section to the project info dictionary
        project_info[section_title] = section_text

    return project_info

def main():
    # Get the webpage
    url = "https://campus.cs.le.ac.uk/teaching/proposals/view_list.php?id=61"
    soup = get_web_page(url)

    # Get project data
    project_data = get_project_links(soup)

    # Loop through the links and get the project info
    for project in project_data:
        print(f'Fetching info for project: {project["title"]}')
        project_info = get_project_info(project["link"])
        project["info"] = project_info

    # Save the project data to a JSON file
    with open('projects.json', 'w') as f:
        print(f'Saving data to projects.json')
        json.dump(project_data, f, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
