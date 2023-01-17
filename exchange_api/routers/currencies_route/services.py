import requests
from bs4 import BeautifulSoup

class Scrapper:
    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = self.create_soup()

    def download_page(self) -> requests.Response:
        response = requests.get(url=self.url)
        return response

    def create_soup(self) -> BeautifulSoup:
        response = self.download_page()
        html = response.content
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def get_currencies(self) -> dict[str:str]:
        currency_table = self.soup.find_all(
            name='div',
            attrs={'class': "currency__CurrencySection-sc-1xymln9-3 kLTJuY"})

        soup_links = []
        currencies = {}

        for letter in currency_table:
            letter: BeautifulSoup
            links = letter.find_all('a')
            soup_links.extend(links)
            
        
        for link in soup_links:
            link: BeautifulSoup
            currency_code, currency_name = link.text.split(" - ")
            currencies[currency_name] = currency_code
            
        return currencies
