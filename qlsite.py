'''
Created on Feb 23, 2011

@author: jackdreilly
'''
from models import Site

qlsites = Site.all().fetch(100)

    
def findSite(url,type):
	return [site for site in qlsites if site.name in url and site.type == type][0]