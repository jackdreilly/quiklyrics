'''
Created on Feb 17, 2011

@author: jackdreilly
'''

# from urllib2 import urlopen
# from urllib import quote_plus
# from json import loads
from qlsite import qlsites
import re
import logging

# searchTemplate = 'http://boss.yahooapis.com/ysearch/web/v1/%s?appid=5mej32DV34FNE0cxlBmOKDfEN8EDHY6zdFxuF2wNILJkQva0H_TjsOFAAyVePYvBJsB_JUpyijLylOXk4lJpK8tJisuL1Gg-&style=raw&format=json&sites=%s'

lyricsSites = map(lambda x: x.siteName, filter(lambda y: y.type =='lyrics',qlsites))
chordSites = map(lambda x: x.siteName, filter(lambda y: y.type =='chords',qlsites))

# import requests
import urllib2
import httplib
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)
# import http
from urllib import quote_plus
# from oauthlib import oauth1
# from google.appengine.api import urlfetch
import simplejson
import requests
# key = 'dj0yJmk9VmNYWU1kNXgxbkxhJmQ9WVdrOWNuWkdZbFE0TXpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD02Mg--'
# secret = 'c8e26945311409681e14dbdbaaccfb0d79ba64c9'



def getLyricsForSong(song):
    # url = u'http://yboss.yahooapis.com/ysearch/limitedweb?q=' + unicode(quote_plus('"lyrics" ' + song)) + u'&format=json&count=10&sites=lyricsfreak.com'
    url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAqMXbCyjx0Qa9yt-xledCUC_1IDgr5FIw&cx=001283733761018543620:ujg1bejtz_y&q="lyrics "' + quote_plus(song)
    url = unicode(url.replace("+", "%20"))
    # url = u'http://yboss.yahooapis.com/ysearch/limitedweb?q=lyrics%20like%20a%20rolling%20sstone&format=json&count=10&sites=lyricsfreak.com'#&fields=title,url'
    # print url
    # client = oauth1.Client(key, client_secret = secret)
    # a,b,c = client.sign(url)
    # opener = urllib2.build_opener()
    # opener.addheaders = b.items()
    # try:
    #     print 'trying page'
    #     # page = urlfetch.fetch(url = url, headers = b).content
    #     page = opener.open(url).read()
    # except httplib.IncompleteRead, e:
    #     # print dir(e)
    #     # print e.message
    #     # print e.strerror
    #     # print 'reached this exception'
    #     # print e
    #     # print type(e)
    #     page = e.partial
    # # except urlfetch.DownloadError, e:
    # #     print dir(e)
    # #     print e.args
    # #     print e.message
    # #     raise Exception()
    page = requests.get(url).content
    # print 'trying to save', json.loads(page)['bossresponse']['limitedweb']['results']
    # return [{'url': x['url'], 'title': x['title']} for x in json.loads(page)['bossresponse']['limitedweb']['results']]
    results = [{'url': x['link'], 'title': x['title']} for x in simplejson.loads(page)['items']]
    logging.info('n results: ' + str(len(results)))
    return results
    # result = json.loads(page)['bossresponse']['limitedweb']['results'][0]['url'].replace('\\/','/')
    # page = bs(requests.get(result).content)
    # sln = page.find("div", id = 'content_h')
    # sln = ''.join([str(c) for c in sln.contents])
    # return sln

# def main():
#     print getLyricsForSong('wish you would step')

# if __name__ == '__main__':
#     main()

def getSongResults(song,lst,st,extra=""):
    return getLyricsForSong(song)
    # url = searchTemplate % (quote_plus(('"%s" ' % st) + song + extra ), ','.join(lst))
    # print url
    # try:
    #     results = map(lambda x: {'url':x['url'],'title':x['title']}, loads(urlopen(url).read())['ysearchresponse']['resultset_web'])
    # except:
    #     results = []
        
    # return results

def getLyrics(song):
    return getSongResults(song,lyricsSites,'lyrics')

def getChords(song):
    return getSongResults(song,chordSites,'chords')

def getSearchResults(search):
    song = search.term
    type = search.type
    if type == 'lyrics':
        return getLyrics(song)
    return getChords(song)