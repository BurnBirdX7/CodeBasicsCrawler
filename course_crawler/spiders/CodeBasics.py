import scrapy
from course_crawler.items import CourseItem


class CourseSpider(scrapy.Spider):
    name = 'CodeBasics'
    allowed_domains = ['code-basics.com']
    start_urls = ['https://code-basics.com/ru/language_categories/programming',
                  'https://code-basics.com/ru/language_categories/layouting']

    def parse(self, response):
        main_block = response.xpath('//main')
        links = main_block.xpath('//div[contains(@class, "card-title")]/a')

        for link in links:
            name = link.xpath('text()').get()
            url = link.xpath('@href').get()

            yield scrapy.Request(response.urljoin(url), self.parse_course, meta={'name': name})

    def parse_course(self, response):
        item = CourseItem()

        container = response.xpath('//main/div/div/div[1]/div/div[1]')

        item['url'] = response.url

        title = response.meta['name']
        long_title: str = container.xpath('//h1/text()').get()
        item['title'] = title
        item['long_title'] = long_title

        item['description'] = container.xpath('//p/text()').get()

        item['cost'] = container.xpath('//*[contains(@class, "badge")]/text()').get()
        item['estimated_duration'] = container.xpath('*//span[1]/text()').get()

        plan_selector = response.xpath('/html/body/main/div/div/div[2]/div[not(contains(@class, "mt-5"))]')
        item['education_plan'] = plan_selector.xpath('div/ul/li/a/text()').getall()

        if not long_title.startswith(title) or long_title.endswith('начинающих'):
            item['entry_level'] = 'Базовый'
        else:
            item['entry_level'] = 'Средний'



        return item
