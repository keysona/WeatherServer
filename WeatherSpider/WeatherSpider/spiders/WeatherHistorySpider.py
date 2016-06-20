import re
import scrapy


class WeatherHistorySpider(scrapy.Spider):

    name = 'weather-history'
    start_urls = [
        'http://lishi.tianqi.com/'
        ]
    date_pattern = r'(\d*).html'

    def parse(self, response):
        # COUNT = 10
        # count = 0
        for a in response.css('.bcity li > a'):
            url = a.css("::attr('href')").extract()[0]
            text = a.css("::text").extract()[0]
            if url != '#':
                self.logger.error('start %s %s' % (text, url))
                yield scrapy.Request(url, self.parse_country,
                                     meta={
                                        'country': text
                                        })
                # count += 1
                # if count == COUNT:
                    # return

    def parse_country(self, response):
        for url in response.css(".tqtongji1 li > a::attr('href')").extract():
            date = re.findall(self.date_pattern, url)[0]
            response.meta.update(date=date)
            yield scrapy.Request(url, self.parse_history_weather,
                                 meta={
                                        'country': response.meta['country'],
                                        'date': date
                                    })

    def parse_history_weather(self, response):
        weathers = []
        for ul in response.css(".tqtongji2 ul")[1:]:
            li_all = ul.css("li")
            li_first = li_all[0]
            weather = dict()
            if li_first.css("a"):
                weather['date'] = self.extract_text(li_first)
            else:
                weather['date'] = self.extract_text(li_first)
            weather['temp_max'] = self.extract_text(li_all[1])
            weather['temp_min'] = self.extract_text(li_all[2])
            weather['weather'] = self.extract_text(li_all[3])
            weather['wind_direction'] = self.extract_text(li_all[4])
            weather['wind_speed'] = self.extract_text(li_all[5])
            weathers.append(weather)
        yield {
            'country': response.meta['country'],
            'weathers': weathers
            }

    def extract_text(self, node):
        text = node.css("::text").extract()
        if text:
            return text[0]
        return ''
