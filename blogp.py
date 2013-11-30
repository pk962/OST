#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
from google.appengine.api import users
from google.appengine.ext import db
import datetime
import webapp2

class Post(db.Model):

  title = db.StringProperty(required=True)
  tag= db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)
  modified_date = db.DateTimeProperty()
  content=db.TextProperty()
  author=db.UserProperty()

class Blog(db.Model):
  name=db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)

class blog_create(webapp2.RequestHandler):
    def post(self):
      user = users.get_current_user()
      if user:
            self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>] ' % (
            user.email(), users.create_logout_url(self.request.uri)))
            self.response.out.write('<br><br>')
            self.response.out.write('<form action="/article" method="post">') 
            self.response.out.write("""
                    <div>Blog_name<input type="text" name="name"><br><br><br></div>
                    <div>Post_title<input type="text" name="title"><br><br><br></div>
                    <div>Content</div>
                    <div><textarea name="content" rows="3" cols="60"></textarea></div>
                    <div>Tag<input type="text" name="tag"><br><br><br></div>
                    <div><input type="submit" value="Submit Blog"></div>
                  
                
              """)
            self.response.out.write('</form>')
      

class blog_display(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>Author:%s wrote:<pre>' %(users.get_current_user()))
        self.response.out.write(cgi.escape(self.request.get('name'))+"<br>")
        self.response.out.write(cgi.escape(self.request.get('content'))+"<br>")
        self.response.out.write(cgi.escape(self.request.get('title'))+"<br>")
        self.response.out.write(cgi.escape(self.request.get('tag'))+"<br>")
        title=self.request.get('title')
        content=self.request.get('content')
        name=self.request.get('name')
        author=users.User()
        tag=self.request.get('tag')
        pos=Post(title=title,tag=tag,content=content,author=author)
        blo=Blog(name=name)
        pos.put()
        blo.put()
        self.response.out.write('</pre></body></html>')

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write('Hello <em>%s</em>! Create a blog[<a href="%s">sign out</a>] ' % (
            user.email(), users.create_logout_url(self.request.uri)))
            self.response.out.write('<br><br>')
            self.response.out.write('<form action="/create" method="post">')
            self.response.out.write("""                                                       
                    <div><input type="submit" value="Create_blog"></div>
               
                             """)
            self.response.out.write('</form>')  
        else:
            self.redirect(users.create_login_url(self.request.uri))





application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create', blog_create),
    ('/article', blog_display)
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()