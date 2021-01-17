import requests
import bs4
import re

n_regex = re.compile(r"\n")


def get_translation(word):
    website = "https://de.pons.com/%C3%BCbersetzung/deutsch-englisch/" + word
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    res = requests.get(website, headers=headers)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    source_element = soup.find_all("div", attrs={"class": "source"})
    target_element = soup.find_all("div", attrs={"class": "target"})

    source = []
    target = []

    for i in range(len(source_element)):
        source_element[i] = n_regex.sub("", str(source_element[i].text))
        source.append(source_element[i])

    for i in range(len(target_element)):
        target_element[i] = n_regex.sub("", str(target_element[i].text))
        target.append(target_element[i])

    return source, target


def get_simple_translation(word):
    return get_translation(word)[1][1]
