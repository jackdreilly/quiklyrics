from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from json import dumps
import os
import lyricsscrape
from models import Title, Site
import urllib2
import httplib
from BeautifulSoup import BeautifulStoneSoup as bs
import logging
from titlecase import titlecase
from random import randint
import __init__ as zeep
import time
from qlsearch import QLSearch
from lyricsscrape import androidSearch, scrapeSongID

SECRET_ACCESS_KEY = '8c52658c67d395ae2a7f40ccbe76f4353b648c09'
API_KEY = '920dc163-c83c-4d50-9e09-c24b2b6b568d'

s = Site(name ='lyricsfreak', type='lyrics',tag = 'a', div='a', siteName='lyricsfreak')
s.put()
# s.commit()


class getLyricsHandler( webapp.RequestHandler ):
    def get( self ):
        try:
            city = self.request.get( 'city' )
            state = self.request.get( 'state' )
            country = self.request.get( 'country' )
            songID = self.request.get('songid')
            type_ = self.request.get('contenttype')
            term = self.request.get('songTitle')
            if not type_:
                type_ = 'lyrics'
            if songID:
                try:
                    resultPack = scrapeSongID(songID)
                except:
                    self.response.out.write(dumps({'post':'No Hits', 'title':''}))
                    return
            else:
                resultPack = androidSearch(QLSearch(term,type_))
            if resultPack['result'] is None:
                lyrics = 'No Hits'
            else:
                lyrics = resultPack['result']['content']
                title = resultPack['result']['title']
            if lyrics == 'No Hits':
                self.response.out.write(dumps({'post':'No Hits', 'title':''}))
                return
            Title( title = title, city = city, state = state, country = country, contenttype = type_ ).put()
            self.response.out.write( dumps( {'post':lyrics, 'title':title,'hits':resultPack['hits']} ) )
        except httplib.IncompleteRead as e:
            # print 'hi'
            # print e
            # print type(e)
            # print '\n######\n'
            self.response.out.write(dumps({'post':'Server Error', 'title':''}))
            
class AndroidLyricsHandler(webapp.RequestHandler):
    def get(self):
        
        type = self.request.get('contenttype')
        term = self.request.get('searchTerm')
        
        resultPack = androidSearch(QLSearch(term,type))
        self.response.out.write(dumps(resultPack))
        


class googleSuggestHandler( webapp.RequestHandler ):
    def get( self ):
        query = self.request.get( 'query' )
        contenttype = self.request.get( 'contenttype' )
        url = 'http://google.com/complete/search?output=toolbar&q=' + query.replace( ' ', '+' )
        txt = urllib2.urlopen( url ).read()
        self.response.headers.add_header('Content-type', 'text/plain')
        resultList = [sug['data'] for sug in bs( txt ).findAll( 'suggestion' )]
        
        self.response.out.write( dumps( {'results':resultList} ) )

class MainPage( webapp.RequestHandler ):
    def get( self ):
        shuffler = randint( 0, 9 )
        recentTitles = [titlecase( ttl.title.lower() ) for ttl in Title.all().order( '-date' ).fetch( 100 )[shuffler::20]]
        self.response.out.write( template.render( os.path.join( os.path.dirname( __file__ ), 'templates', 'index.htm' ), {'recentTitles':recentTitles}, True ) )




application = webapp.WSGIApplication( [( '/suggest.*', googleSuggestHandler ),
                                       ( '/getlyrics.*', getLyricsHandler ),
                                       ( '/.*', MainPage ),
                                       ], debug = True )


def main():
    run_wsgi_app( application )



if __name__ == "__main__":
    main()
