#!/user/bin/env python

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import re, collections

corpus = 'simple.txt'

def words(text): return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file(corpus).read()))

def counts(text):
    return [(w, NWORDS[w]) for w in words(text)]

def render(counts):
    html = '<FONT COLOR="1B2940">'
    for word, count in counts:
        if count == 1:
            html += '<FONT COLOR="6CA4FF">'+word+'</FONT>'
        elif count < 30:
            html += '<FONT COLOR="6194E5">'+word+'</FONT>'
        else:
            html += word
        html += ' '
    html += '</FONT>'
    return html

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""<!DOCTYPE html>
        <html>
        <head>
            <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">
        </head>
    """)
    self.response.out.write('<body><div class="container">')

    # A description
    self.response.out.write("""
        <h1><a href='http://simpleenglishchecker.appspot.com/'>Simple English</h1></a>
        <p class='lead'>
            Identify words that are <FONT COLOR="6CA4FF">rare</FONT> or <FONT
            COLOR="6194E5">uncommon</FONT>.
            <br/>
            <small>
            <a href='http://benjaminhaley.blogspot.com/2012/09/simple-english.html'>read
            more</a> or <a
            href='https://github.com/benjaminhaley/simpleenglish'>get the
            code</a> -
            benjamin.haley@gmail.com
            </small>
        </p>
    """)

    # Social Media
    self.response.out.write("")


    # Content
    self.response.out.write("""
        <form action="" method="post">
            <div>
                <textarea name="content" rows="10" class="span12"
                placeholder="Your text here...">%s</textarea>
            </div>
            <div><input class='btn btn-primary' type="submit" value="Highlight Uncommon Words"></div>
        </form>
    """ % self.request.get('content'))
    self.response.out.write(
            '<div class="hero-unit">'+
            render(counts(self.request.get('content'))) +
            '</div>'
    )
    self.response.out.write('</div/></body></html>')

  def post(self):
      self.get()

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
