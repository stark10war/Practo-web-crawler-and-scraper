# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:13:04 2019

@author: Shashank.Tanwar
"""


import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np
from ..items import PractoSpiderItem


class practo_spider(scrapy.Spider):
    
    name = 'practo'
    page_number = 2
    start_urls = ['https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22General%20Physician%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=Delhi&page=1']
    items = PractoSpiderItem()

    def parse(self, response):
        
        total_results = response.css('div[class="u-cushion u-white-fill u-normal-text o-card o-card--separated c-list-card"]')
        for result in total_results:
            doctor_page_link = result.css('div.c-card-info a::attr(href)').get()
            print(doctor_page_link)
            yield response.follow(url = doctor_page_link, callback = self.parse_doctor)
        
        next_page = response.css('ul[class="c-paginator"] li a[data-qa-id="pagination_next"]::attr(href)').get()
        next_page_link = 'https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22General%20Physician%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=Delhi&page='+ str(practo_spider.page_number)
        
        if practo_spider.page_number<3:
            practo_spider.page_number = practo_spider.page_number+1
            print('First page scrapped successfully, moving to next page....')
            print(next_page_link)
   #         next_page_link = start_urls[0]+ '&page=' + str(1+len(next_page))
            yield response.follow(url = next_page_link, callback = self.parse)
        

    def parse_doctor(self,response):
    
        self.items['doctor'] = response.css('h1[data-qa-id="doctor-name"]::text').extract()
        self.items['qualification'] = response.css('div.c-profile--qualification p[data-qa-id="doctor-qualifications"]::text').extract()
        self.items['experience'] = response.css('div.c-profile__details > h2.u-d-inlineblock::text').extract()
        self.items['fees'] = response.css('span[data-qa-id="consultation_fee"]::text').extract()
        self.items['upvote_percentage'] = response.css('div.c-profile--verification p[data-qa-id="doctor-patient-experience-score"] span[class="u-green-text u-bold u-large-font"]::text').extract()
        self.items['total_votes'] = response.css('span[class="u-smallest-font u-grey_3-text"] ::text').extract()
        self.items['clinic_name'] = response.css('div[class="pure-g c-profile--clinic--details"] h2 a::text').extract()
        self.items['address'] = response.css('p.c-profile--clinic__address::text').extract()
        self.items['clinic_ratings'] = response.css('div[class="common__star-rating tooltip-hover"] span.common__star-rating__value::text').extract()
        self.items['specializations'] = response.css('div#specializations div.p-entity--list ::text').extract()
        self.items['services'] = response.css('div#services div.p-entity--list ::text').extract()
        self.items['registrations'] = response.css('div#registrations div.p-entity--list ::text').extract()
        no_of_feedbacks = response.css('li[data-qa-id="feedback-tab"] > span::text').extract()[0]
        print(no_of_feedbacks)
        if len(no_of_feedbacks) > 0 :
            no_of_feedbacks = int(''.join(i for i in no_of_feedbacks if i not in ('(',')')))
        
        else:
            no_of_feedbacks = 0
            self.items['feedbacks_all'] = 'No feedback available'
            yield self.items
        
        if no_of_feedbacks >4:
            feedback_page = response.css('a[data-qa-id="show-all-feedback"]::attr(href)').get()
            yield response.follow(url = feedback_page, callback = self.parse_feedbacks)
        
        else:
            total_feedbacks = response.css('div.feedback--list-container div[data-qa-id="feedback_item"]')
            all_feedbacks = []
            for feedback in total_feedbacks:
                polarity = feedback.css('div[class="u-cushion--small-bottom u-large-font"] span::text').extract()
                tags = feedback.css('p[class="feedback__content u-cushion--small-bottom u-large-font"] ::text').extract()
                message = feedback.css('p[data-qa-id="review-text"] ::text').extract()
                feedbacks_list = [polarity, tags, message]
                single_feedback = []
                for values in feedbacks_list:
                    if type(values)==list:
                        values = ' , '.join(values)                   
                    single_feedback.append(values)
                full_feedback  = " >>> ".join(single_feedback)               
                all_feedbacks.append(full_feedback)
            self.items['total_feedbacks'] = len(all_feedbacks)
            final_all_feedback_text = ' $$$New_feedback$$$ '.join(all_feedbacks)
            self.items['feedbacks_all'] = final_all_feedback_text
    ll        yield self.items
                

        
    def parse_feedbacks(self,response):
        
        total_feedbacks = response.css('div.feedback--list-container div[data-qa-id="feedback_item"]')
        all_feedbacks = []
        for feedback in total_feedbacks:
            polarity = feedback.css('div[class="u-cushion--small-bottom u-large-font"] span::text').extract()
            tags = feedback.css('p[class="feedback__content u-cushion--small-bottom u-large-font"] ::text').extract()
            message = feedback.css('p[data-qa-id="review-text"] ::text').extract()
            feedbacks_list = [polarity, tags, message]
            single_feedback = []
            for values in feedbacks_list:
                if type(values)==list:
                    values = ' , '.join(values)                   
                single_feedback.append(values)
            full_feedback  = " >>> ".join(single_feedback)               
            all_feedbacks.append(full_feedback)
        self.items['total_feedbacks'] = len(all_feedbacks)
        final_all_feedback_text = ' $$$New_feedback$$$ '.join(all_feedbacks)
        self.items['feedbacks_all'] = final_all_feedback_text
        yield self.items
        #yield response.follow(url = feedback_page, callback = self.parse_feedbacks)
        
            
        #def parse_feedbacks(self,response):
         #   yield items
        
        
#process = CrawlerProcess()
#process.crawl(quotes_spider)
#process.start()





