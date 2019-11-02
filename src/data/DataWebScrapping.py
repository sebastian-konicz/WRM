import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pathlib import Path

# SCRAPPING DATA FROM THE NET
def scrapping(dir):

    # Downloading rental data from the page
    pageRental = requests.get("https://www.wroclaw.pl/open-data/dataset/wrmprzejazdy_data/resource_history/65b5015e-070e-41da-8852-802a86442ac5")
    htmlRental = BeautifulSoup(pageRental.content, 'html.parser')
    linksRental = htmlRental.find_all("a", class_="heading")

    filenames = []
    for link in linksRental:
        href = link.get('href')
        index = href.index("Historia")
        filename = href[index:]
        filenames.append(filename)
        filepath = dir + r'\data\raw\{}'.format(filename)
        if Path(filepath).exists() == False:
            urlretrieve(href, filepath)
            print("Data updated: " + filename)
        else:
            pass

    #Downloading dockingstation data form the page
    pageStations = requests.get('https://www.wroclaw.pl/open-data/dataset/nextbikesoap_data')
    htmlStations = BeautifulSoup(pageStations.content, 'html.parser')
    linksStations = htmlStations.find("a", class_="resource-url-analytics")

    hrefStations = linksStations.get('href')
    urlretrieve(hrefStations, str(dir) + r'\data\raw\DockingStations.csv')
    print("Docking station data have been updated")

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    scrapping(project_dir)