from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from scrapy.signalmanager import dispatcher

class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item")
    )

    def __init__(self, *args, **kwargs):
        super(CrawlingSpider, self).__init__(*args, **kwargs)
        self.books = []
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse_item(self, response):
        title = response.css(".product_pod h3 a::attr(title)").get()
        price = response.css(".price_color::text").get()

       
        price = float(price.replace('£', ''))

        book_data = {
            'title': title,
            'price': price,
        }

        self.books.append(book_data)

        yield book_data

    def spider_closed(self, spider):
        if len(self.books) >= 2:
            
            sorted_books = sorted(self.books, key=lambda x: x['price'])

            
            book1 = sorted_books[0]
            book2 = sorted_books[1]

            print(f"Comparação de preços entre '{book1['title']}' e '{book2['title']}':")
            if book1['price'] < book2['price']:
                print(f"'{book1['title']}' é mais barato que '{book2['title']}'")
            elif book1['price'] > book2['price']:
                print(f"'{book2['title']}' é mais barato que '{book1['title']}'")
            else:
                print(f"'{book1['title']}' e '{book2['title']}' têm o mesmo preço")