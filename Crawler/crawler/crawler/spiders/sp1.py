import scrapy

class Sp1Spider(scrapy.Spider):
    name = 'sp1'
    allowed_domains = ['leagueoflegends.com']
    start_urls = ['https://www.leagueoflegends.com/pt-br/champions']

    def start_requests(self):
        yield scrapy.Request('https://www.leagueoflegends.com/pt-br/champions/', self.parse)

    def parse(self, response):
        print("ACESSANDO URL:", response.url)
        result = response.css('.style__List-sc-13btjky-2.dLJiol')

        CHAMPION_SELECTOR = "a.style__Wrapper-n3ovyt-0.style__ResponsiveWrapper-n3ovyt-4::attr(href)"

        champions = result.css(CHAMPION_SELECTOR).getall()

        for a in range(0, len(champions)):
            championUrl = "https://www.leagueoflegends.com"+champions[a]
            yield scrapy.Request(championUrl, self.parse_boneco)
        

    def parse_boneco(self, response):
        print("ACESSANDO URL:", response.url)
        result = response.css('.style__AbilityInfoList-sc-1bu2ash-7').extract()
        
        NICK_SELECTOR = ".style__Title-sc-1h71ys8-3.fXBrkV span::text"
        SUB_NICK_SELECTOR = ".style__Intro-sc-1h71ys8-2.kcvbei span::text"
        NAME_SELECTOR = "h5.style__AbilityInfoItemName-sc-1bu2ash-10.gUFHLu::text"
        DESC_SELECTOR = "p.style__AbilityInfoItemDesc-sc-1bu2ash-11.iqHSEh::text"

        nick = response.css(NICK_SELECTOR).extract()
        sub = response.css(SUB_NICK_SELECTOR).extract()
        nomes = response.css(NAME_SELECTOR).extract()
        descriptions = response.css(DESC_SELECTOR).extract()
        
        for a in range(-1, len(nomes)):
            if(a == -1):
                yield {
                    'Nome': nick[0],
                    'Descricao': sub[0]
                }
            else:
                yield{
                    'Nome': nomes[a],
                    'Descricao': descriptions[a]
                }

            pass
