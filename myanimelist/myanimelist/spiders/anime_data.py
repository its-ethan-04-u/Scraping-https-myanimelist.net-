import scrapy


class AnimeDataSpider(scrapy.Spider):
    name = "anime_data"
    #allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/topanime.php"]
    
    #def start_requests(self):
       # yield scrapy.Request(url='https://myanimelist.net/topanime.php',callback=self.parse)

    def parse(self, response):
        #print("Message : ",response.body)
        for anime in response.css("tr.ranking-list"):
            detail_url = anime.css("td.title a::attr(href)").get()
            if detail_url:
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_anime_detail,
                    meta={'rank':anime.css("td.rank span::text").get().strip() if anime.css("td.rank span::text").get() else None }
                )

        next_page = response.css('a.link.blue-box:contains("Next")::attr(href)').get()
        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url,callback=self.parse)
        else:
            # Alternative way: calculate next offset
            current_limit = int(response.url.split('limit=')[-1]) if 'limit=' in response.url else 0
            next_limit = current_limit + 50
            next_url = f"https://myanimelist.net/topanime.php?limit={next_limit}"
            # Check if next page actually exists by looking for anime entries
            if response.css("tr.ranking-list"):
                yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_anime_detail(self,response):
        item = {}

        item['url'] = response.url
        item['mal_id'] = response.url.split('/')[-2] if response.url.split('/')[-2].isdigit() else None
        item['rank'] = response.meta.get('rank','')
        
        # Basic Info
        item['title'] = response.css('h1.title-name strong::text').get(default='').strip()
        item['title_english'] = response.xpath("//span[contains(text(),'English:')]/following-sibling::text()").get(default='').strip()
        item['title_japanese'] = response.xpath("//span[contains(text(),'Japanese:')]/following-sibling::text()").get(default='').strip()

        # Left-column info (use a helper dict)
        info = {}

        for row in response.css('div.spaceit_pad'):
            key = row.css('span::text').get()
            if key and ':' in key:
                key = key.strip(': ')
                value = ''.join(row.xpath('text() | a/text()').getall()).strip()
                info[key.lower()] = value


        item['type'] = info.get('type','')
        item['episodes'] = info.get('episodes','')
        item['status'] = info.get('status','')
        item['aired'] = info.get('aired','')
        item['premiered'] = info.get('premiered','')
        item['source'] = info.get('source','')
        item['duration'] = info.get('duration','')
        item['rating'] = info.get('rating','')

        # Genres, Themes, Demographics

        item['genres'] = [g.strip() for g in response.css('span:contains("Genre") ~ a::text, span:contains("Genres") ~ a::text').getall()]
        item['genres'] = ', '.join(i for i in item['genres']).strip() if item['genres'] else ''
        item['themes'] = [t.strip() for t in response.css('span:contains("Theme") ~ a::text, span:contains("Themes") ~ a::text').getall()]
        item['themes'] = ', '.join(i for i in item['themes']).strip() if item['themes'] else ''
        item['demographics'] = [d.strip() for d in response.css('span:contains("Demographic") ~ a::text, span:contains("Demographics") ~ a::text').getall()]
        item['demographics'] = ', '.join(i for i in item['demographics']).strip() if item['demographics'] else ''

        # Studios, Producers, Licensors

        item['studios'] = [s.strip() for s in response.css('span:contains("Studio") ~ a::text, span:contains("Studios") ~ a::text').getall()]
        item['studios'] = ', '.join(i for i in item['studios']).strip() if item['studios'] else ''
        item['producers'] = [p.strip() for p in response.css('span:contains("Producer") ~ a::text, span:contains("Producers") ~ a::text').getall()]
        item['producers'] = ', '.join(i for i in item['producers']).strip() if item['producers'] else ''
        item['licensors'] = [l.strip() for l in response.css('span:contains("Licensor") ~ a::text, span:contains("Licensors") ~ a::text').getall()]
        item['licensors'] = ', '.join(i for i in item['licensors']).strip() if item['licensors'] else ''

        # Statistics (right sidebar)

        item['score'] = response.css('span.score-label::text').get(default='').strip()
        item['scored_by'] = response.xpath("//span[@itemprop='ratingCount']/following-sibling::text()").get(default='').replace(' users)','').strip()  
        item['rank'] = response.css('span.numbers.ranked strong::text').get(default='').replace('#','').strip()
        item['popularity'] = response.css('span.numbers.popularity strong::text').get(default='').replace('#','').strip()
        item['members'] = response.css('span.numbers.members strong::text').get(default='').strip()
        item['favorites'] = response.xpath("//span[contains(text(),'Favorites:')]/following-sibling::text()").get(default='').strip()

        # Synopsis & Background
        item['synopsis'] = response.css('p[itemprop="description"]::text, p[itemprop="description"] span::text').getall()
        item['synopsis'] = ' '.join(item['synopsis']).strip()

        yield item
