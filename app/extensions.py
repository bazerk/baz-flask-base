import oauth2 as oauth
import urlparse
import urllib


class Twitter():

    request_token_url = "http://twitter.com/oauth/request_token"
    authenticate_url = 'http://twitter.com/oauth/authenticate'
    access_token_url = 'http://twitter.com/oauth/access_token'

    def set_callback(self, callback):
        self.callback = callback

    def set_keys(self, consumer_key, consumer_secret, token_key=None, token_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_key = token_key
        self.token_secret = token_secret

    def get_client(self, token=None):
        consumer = oauth.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        return oauth.Client(consumer, token)

    def request_token(self):
        client = self.get_client()

        payload = {'oauth_callback': self.callback}
        url = '%s?%s' % (Twitter.request_token_url, urllib.urlencode(payload))
        resp, content = client.request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from twitter %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))
        return ("%s?oauth_token=%s" % (Twitter.authenticate_url, request_token['oauth_token']), request_token)

    def get_access_token(self, oauth_token, oauth_verifier, request_token):
        token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = self.get_client(token)

        resp, content = client.request(Twitter.access_token_url, "POST")
        if resp['status'] != '200':
            raise Exception("Invalid response from twitter %s." % resp['status'])

        return dict(urlparse.parse_qsl(content))


from flaskext.bcrypt import Bcrypt
bcrypt = Bcrypt()

Session = None
twitter = Twitter()
