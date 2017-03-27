import scrapy
from ..items import TeacherItem

class Teacher_spdier(scrapy.Spider):
    name='teachjob'
    start_urls = ['http://www.dxc020.com/Student.asp?page='+str(x) for x in range(1,2)]

    def parse(self,response):
        grade_list = response.xpath('//td[@width="12%"]/br[1]/preceding-sibling::node()[1]').extract()
        subject_list = response.xpath('//td[@width="12%"]/br[2]/preceding-sibling::node()[1]').extract()
        gender_list = response.xpath('//td[@width="36%"]/div/font/text()').extract()
        other_list = response.xpath('//td[@width="36%"]/div/descendant::node()[4]').extract()
        detail_list = response.xpath('//div[@class="ShowDetail"]/a/@href').extract()
        for i,j,z,x,d in zip(grade_list,subject_list,gender_list,other_list,detail_list):
            zf = TeacherItem()
            zf['grade'] = i
            zf['subject'] = j
            zf['gender'] = z
            zf['other'] = x[1:-3]
            request = scrapy.Request('http://www.dxc020.com/'+d, callback=self.parse_detail)
            request.meta['item'] = zf
            yield request

    def parse_detail(self, response):
        zf = response.meta['item']
        zf['time'] = response.xpath('//table[@class="data_detail"]/tbody/tr[8]/td[2]/text()').extract()[0]
        zf['reward'] = response.xpath('//table[@class="data_detail"]/tbody/tr[9]/td[2]/font/text()').extract()[0] + response.xpath('//table[@class="data_detail"]/tbody/tr[9]/td[2]/text()').extract()[0][0:5]
        yield zf
