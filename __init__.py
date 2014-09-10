# Copyright (c) 2008 Zeep Mobile (zeepmobile.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
  
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
   
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import base64
import os
import hmac
import hashlib
import time
try:
    from urllib import urlencode
    from urllib2 import URLError, Request, urlopen
except ImportError:
    # Presumably, they are running Py3k, which merged the modules
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
import sha

class ZeepError(Exception):
    pass


def connect(api_key=None, secret_key=None):
    if api_key is None:
        api_key = '920dc163-c83c-4d50-9e09-c24b2b6b568d'
        
    if secret_key is None:
        secret_key = '8c52658c67d395ae2a7f40ccbe76f4353b648c09'
        
    return Connection(api_key, secret_key)


class Auth:
    """Provides low level signature signing and validation routines. This class is provided
    for developers who wish to integrate Zeep with other web platforms and servers. Normally you
    would use the Connection instance returned by zeep.sms.connect() to interact with Zeep Mobile
    
    Api and secret keys can be obtained at zeepmoible.com.
    
    
    """
        
    @classmethod
    def sign_request(cls, request, api_key, secret_key):
        """Adds an authorization header to any object that has the same interface
        as urllib2.Request. Specifically this object must support add_header(), get_header(),
        has_header() and get_data() methods.
        
        >>> import urllib2
        >>> request = urllib2.Request('https://api.zeepmobile.com/messaging/2008-07-14/send_message')
        >>> request.add_data('Hi Mom')
        
        If you do not set the Date header in the request a Date header will be set for you.
        To keep our unit test consistant we set the Date header in this example.
        
        >>> request.add_header('Date', 'Tue, 26 Aug 2008 18:07:33 GMT')
        
        Once your request is built use Auth.sign_request to add the Authorization header.
        
        >>> Auth.sign_request(request, 'api-key', 'secret-key')
        
        >>> request.get_header('Authorization')
        'Zeep api-key:CY8NJNtmgnzgRj+VL08kr/7oPBo='
              
        """
  
        body = request.get_data()
        
        if not request.has_header('Date'):            
            request.add_header('Date', time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.gmtime()))
        http_date = request.get_header('Date')
        
        signature = cls.calculate_signature(body, api_key, secret_key, http_date)
        request.add_header('Authorization', 'Zeep %s:%s' % (api_key, signature))
        
    @classmethod
    def signature_valid(cls, request, api_key, secret_key):
        """Returns true if the request has a valid Zeep signature, otherwise false.
        
        Use this method to validate that a web request, specfically a mobile event, 
        originated from Zeep.
        
        Assume your webserver received the following request.
        
        >>> import urllib, urllib2
        >>> request = urllib2.Request('https://api.zeepmobile.com/messaging/2008-07-14/send_message')
        >>> request.add_data(urllib.urlencode({'user_id': 'joe@test.com', 
        ...            'event':'MO', 'message':'hi mom' }))
        >>> request.add_header('Date', time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.gmtime()))
        >>> Auth.sign_request(request, 'api-key','secret-key')
        
        You can validate that the method did in fact originate from Zeep like this
        
        >>> Auth.signature_valid(request, 'api-key', 'secret-key')
        True
        
        """
        
        signature = cls.calculate_signature(request.get_data(), api_key, 
                                        secret_key, request.get_header('Date'))
                                        
        authentication = 'Zeep %s:%s' % (api_key, signature)
              
        return request.get_header('Authorization') ==  authentication

    @classmethod    
    def calculate_signature(cls, body, api_key, secret_key, http_date=None):
      """Returns the base64 HMAC based on the body, api_key, secret_key and http_date.
       
      
      >>> Auth.calculate_signature('Hi Mom', 'api-key', 'secret-key', 
      ...     'Tue, 26 Aug 2008 18:07:33 GMT')
      'CY8NJNtmgnzgRj+VL08kr/7oPBo='
      
      Note  passing in date and time is optional. We do it above to generate a consistant
      value for our doctest. You can call the method without a time like below to generate
      the signature.
      
      >>> sig = Auth.calculate_signature('Hi Mom', 'api-key', 'secret-key')
     
      Which should return a 28 character long string.
      
      >>> len(sig)
      28
      
      """
      
      if http_date is None:
          http_date = time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.gmtime())
      
      # As of 3.0, everything is Unicode, and the hmac module only accepts bytes
      sig = hmac.new(secret_key.encode('ascii'), digestmod=hashlib.sha1)
      sig.update(api_key.encode('ascii'))
      sig.update(http_date.encode('ascii'))
      sig.update(body.encode('ascii'))
      
      return base64.encodestring(sig.digest()).strip().decode('utf-8')
            
    
class Connection:
    """Simplifies sending HTTP requsets to Zeep Mobile. 
    
    """
    
    base_url = 'https://api.zeepmobile.com/messaging'
    version = '2008-07-14'
     
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key 
                
    def send_message(self, user_id, body):
        request = self.make_request('send_message', user_id=user_id, body=body)
        self.dispatch(request)
    
    def blast_message(self, body):
        request = self.make_request('blast_message', body=body)
        self.dispatch(request)
        
    def dispatch(self, request):
        """Sends the given request and waits for the response. Raises an exception if the 
        HTTP status code is anything other than 200"""
        
        try:
            response = urlopen(request)
        except URLError:
            import sys
            (err_type, err_val, err_tb) = sys.exc_info()
            raise ZeepError('Zeep connection failed with code %s and reason: %s' %
                            (err_val.code, err_val.read()))

        response_body = response.read()
        if response_body.strip().decode('utf-8')  != 'OK':
            raise RuntimeError("Expected OK got %s" % response_body)        

    def make_request(self, action, **kw):
        """Returns a signed Request object.
        
        >>> conn = Connection('api-key', 'secret-key')
        >>> request = conn.make_request('send_message', arg1='blah', arg2='foo')
        
        >>> request.get_full_url()
        'https://api.zeepmobile.com/messaging/2008-07-14/send_message'
        
                
        >>> Auth.signature_valid(request, conn.api_key, conn.secret_key)
        True
        
        >>> request.get_method()
        'POST'
        
        >>> request.get_data()
        'arg1=blah&arg2=foo'
        
        """
        
        request = Request("%s/%s/%s" % (self.base_url, self.version, action))
        request.add_data(urlencode(kw))
        Auth.sign_request(request, self.api_key, self.secret_key)
        
        return request
        
        
