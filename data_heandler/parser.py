from dataclasses import dataclass

import bs4
import requests


@dataclass
class ServicesStat:
    name: str
    url: str = None
    description: str = None


class CompanyParser:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {
            'User-Aget': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164'
                ' Safari/537.36'),
            'Accept-Language': 'en',
        }

    def get_page(self, page: int = None, url: str = None):
        params = {}
        if page and page > 1:
            params['start'] = page
        if not url:
            url = 'https://www.justwebagency.com'
        r = self.session.get(url, params=params)
        return r.text

    def parse_block(self, page, url: str = None):
        text = self.get_page(page=page, url=url)
        return bs4.BeautifulSoup(text, 'lxml')

    def get_pagination_limit(self):
        page_list = range(0, 300, 10)
        for page in page_list:
            if self.get_block(page):
                break

    def get_block(self, page):
        soup = self.parse_block(page)
        services_list = soup.select('.sub-menu > li > a')
        services = {}
        for item in services_list:
            block = ServicesStat(
                item.get_text(), item.get('href'))
            if block.url:
                soup = soup = self.parse_block(page=page, url=block.url)
                service_discription = [item.get_text().strip().replace("\n", '') for item in soup.select('#main .entry-content .vc_row.wpb_row.vc_row-fluid')]
                block.description = service_discription
            services[block.name] = block
        return services


class Command:
    help = 'Companies parsing'

    def handle(self, *args, **options):
        p = CompanyParser()
        p.get_pagination_limit()


if __name__ == '__main__':
    a = Command()
    a.handle()
