# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PractoSpiderPipeline(object):
    def process_item(self, item, spider):
        item['specializations'] = [i for i in item['specializations'] if i !=' ']
        item['total_votes'] = [i for i in item['total_votes'] if i not in (' ','(',')')]
        if len(item['clinic_name'])>1:
            item['clinic_name'] = item['clinic_name'][0]
        
        if len(item['address'])>1:
            item['address'] = item['address'][0]
        
        if len(item['clinic_ratings'])>1:
            item['clinic_ratings'] = item['clinic_ratings'][0]
        
        if len(item['experience'])>1:
            item['experience'] = item['experience'][1]
        
        if len(item['fees'])>1:
            item['fees'] = item['fees'][1]
        
        print(item)
        return item
