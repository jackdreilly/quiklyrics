'''
Created on Feb 17, 2011

@author: jackdreilly
'''


from qlsite import qlsites
import re
import logging

lyricsSites = map(lambda x: x.siteName, filter(lambda y: y.type =='lyrics',qlsites))
chordSites = map(lambda x: x.siteName, filter(lambda y: y.type =='chords',qlsites))
from urllib import quote_plus
import simplejson
from google.appengine.api import urlfetch


def getSongResults(song,lst,st,extra=""):
    url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAqMXbCyjx0Qa9yt-xledCUC_1IDgr5FIw&cx=001283733761018543620:ujg1bejtz_y&q="lyrics "' + quote_plus(song)
    url = unicode(url.replace("+", "%20").replace(" ", "%20"))
    logging.info(url)
    contents = urlfetch.fetch(url = url).content
    logging.info("contents: " + str(contents))
    results = [{'url': x['link'], 'title': x['title']} for x in simplejson.loads(str(contents))['items']]
    logging.info('n results: ' + str(len(results)))
    return results

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