import json
import os
from datascrapper import DataScrapper

URL = "https://www.ivi.ru/movies/"
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
PATH = "data/"

def get_categories(soup):
    categories = soup.find(class_="headerDropdown__body").find_all(class_="dropdownLinksList__item")
    categories_dict = {}
    for category in categories:
        link = category.find("a")
        url = link["href"]
        name = link.text.strip()
        categories_dict[name] = url
        
        data = DataScrapper(url, HEADERS) 
        category_path = f"{PATH}categories/{name}.html"
        data.pull_from_file_or_url(category_path)
        if not os.path.isfile(category_path):
            data.save(category_path)

    return categories_dict

def get_all_films(ds, categories_dict):
    films_dict = {}
    i = 1
    for name, url in categories_dict.items():
        ds.url = url
        soup = ds.pull_from_file_or_url(f"{PATH}categories/{name}.html")
        films = soup.find_all(class_="gallery__item gallery__item_virtual")
        info_dict = {}
        for film in films:
            short_url = film.find("a")["href"]
            url = "https://www.ivi.ru" + short_url
            film_name = film.find(class_="nbl-slimPosterBlock__titleText").text.strip().replace("\"", "")
            properties = film.find(class_="nbl-poster__propertiesInfo").find(class_="nbl-poster__propertiesRow").text.strip().split(",")
            info_dict[film_name] = {
                "url": url,
                "year": properties[0],
                "country": properties[1],
                "genre": properties[2],
            }
        films_dict[name] = info_dict
        i += 1
        print(f"\33[92mCategory {name} have scanned\33[0m")
    return films_dict

if __name__ == "__main__":
    ds = DataScrapper(URL, HEADERS)

    # pull the data from created html file or get from url
    soup = ds.pull_from_file_or_url(f"{PATH}index.html")
    ds.save(f"{PATH}index.html")
    categories_dict = get_categories(soup)

    # save data as json 
    with open(f"{PATH}categories.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(categories_dict, indent=4, ensure_ascii=False))
    
    films_dict = get_all_films(ds, categories_dict)

    # save data as json 
    with open(f"{PATH}all_films.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(films_dict, indent=4, ensure_ascii=False))
    
