'''
Created on Oct 22, 2010

@author: jackreilly
'''
from google.appengine.ext import db
from simplejson import dumps

class Site( db.Model ):
    name = db.StringProperty(required=True)
    count = db.IntegerProperty()
    type = db.StringProperty(required=True)
    tag = db.StringProperty(required=True)
    div = db.StringProperty(required=False)
    siteName = db.StringProperty(required=True)
    
    def increment(self):
        self.count+=1
        self.put()

class Title( db.Model ):
    title = db.StringProperty( required = True )
    state = db.StringProperty( required = False )
    city = db.StringProperty( required = False )
    country = db.StringProperty( required = False )
    date = db.DateTimeProperty( auto_now_add = True )
    contenttype = db.StringProperty( required = False )
    
class SearchResult(db.Model):
    url = db.URLProperty(required = False)
    title = db.StringProperty(required = False)
    searchTerm = db.StringProperty(required = False)
    date = db.DateTimeProperty(auto_now_add=True)
    type = db.StringProperty(required=True)
    site = db.ReferenceProperty(Site)
    
    def toJSON(self):
        return dumps(self.toDict())
    
    def toDict(self):
        return {'title':self.title,'id':str(self.key())}

