from urllib2 import Request, urlopen
import re
import models
from titlecase import titlecase
import boss
from qlsite import findSite
import logging
from bs4 import BeautifulSoup
import logging
from google.appengine.api import urlfetch


def storeAndSearch(search):
    results = boss.getSearchResults(search)
    logging.info('get some results: %s' % results)
    type = search.type
    hits = []
    for result in results:
        site = findSite(result['url'],type)
        if site is None:
            continue
        logging.info('site is not none!!!!!')
        sr = models.SearchResult(url=result['url'],title=result['title'],searchTerm=search.term,site= site,type=search.type)
        sr.put()
        hits.append(sr)
    return hits




    


def getLyrics(hit):
    try:
        result = hit.url.replace('\\/','/')
        page = BeautifulSoup(urlfetch.fetch(url = result).content)
        sln = page.find("div", id = 'content_h')
        sln = ''.join([str(c) for c in sln.contents])
        return {'title':page.find('title').text,'content':sln}        
    except Exception, e:
        logging.error(e)
    
def getChords( hit ):
    
    def cleanChords(chords):
        return chords.replace( '\n', '<br />' ).replace( '\r', '<br />' )
    
    def cleanChordsTitle(title):
        removeLyrics = re.compile( 'chords for', re.IGNORECASE )
        title = removeLyrics.sub( '', title )
        removeLyrics = re.compile( 'chords', re.IGNORECASE )
        title = removeLyrics.sub( '', title )
        removeLyrics = re.compile( 'lyrics', re.IGNORECASE )
        title = removeLyrics.sub( '', title )
        removeLyrics = re.compile( 'tabs', re.IGNORECASE )
        title = removeLyrics.sub( '', title )
        removeLyrics = re.compile( ',', re.IGNORECASE )
        title = removeLyrics.sub( '', title )
        tag = re.compile( '@.*ultimate.*$', re.IGNORECASE )
        title = tag.sub( '', title )
        title = str( titlecase( title.replace( '<title>', '' ).replace( '</title>', '' ).lower() ) )
        return title
    hit_url = hit.url
    divtype = hit.site.div
    url_txt = urlopen( Request( hit_url ) ).read()
    # soup = BeautifulSoup( url_txt )
    soup = None
    if 'ultimate' in hit.site.name:
        lyricsSet = soup.findAll( 'div', {'id':divtype} )
        regex = r'(<div[\s\w=\n\r\t\_"]*>).*(</div>)'
    elif 'azchords' in hit.site.name:
        lyricsSet = soup.findAll( 'pre' )
        regex =  r'(<pre>).*(</pre>)'
        
    lyrics = str( lyricsSet[0] )
    tags = re.findall( regex, lyrics, re.DOTALL )
    lyrics = lyrics.replace( tags[0][0], '' ).replace( tags[0][1], '' )

    stupidLink = re.compile( '\[.*http.*\]', re.IGNORECASE )
    lyrics = stupidLink.sub( '', lyrics )
    upperChorus = re.compile( 'chorus', re.IGNORECASE )
    lyrics = cleanChords(upperChorus.sub( 'CHORUS', lyrics ))
    title = cleanChordsTitle(str( soup.findAll( 'title' )[0] ))    
    return {'content':lyrics,'title':title,'hit':hit}

def getWinner(hit):
    if hit.type == 'lyrics':
        return getLyrics(hit)
    return getChords(hit)
    hit.site.increment()

def scrapeSongID(songid):
    return {'result': getWinner(models.SearchResult.get(songid)), 'hits': []}
    
        
        

def androidSearch(search):
    

        
    def getWinnerFromHits(hits):
        while len(hits) > 0:
            try:
                hit = hits[0]
                winner = getWinner(hit)
                hits.remove(hit)
                return winner
            except:
                hits.remove(hit)
    hits = storeAndSearch(search)
    winner = getWinnerFromHits(hits)
    return {'result':winner,'hits':map(lambda x: x.toDict(), hits)}
