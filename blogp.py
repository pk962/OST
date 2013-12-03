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
  blog_name=db.StringProperty(required=True)
  tag= db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)
  modified_date = db.DateTimeProperty()
  content=db.TextProperty()
  

class Blog(db.Model):
  name=db.StringProperty(required=True)
  title = db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)
  author=db.UserProperty(required=True)

def Post_key(title=None):
    """Constructs a datastore key for a Post entity with title."""
    return db.Key.from_path('Post', title)

def Blog_key(name=None):
    """Constructs a datastore key for a Blog entity with name."""
    return db.Key.from_path('Blog', name)


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
        pos=Post(title=title,tag=tag,content=content,blog_name=name)
        blo=Blog(name=name,title=title,author=author)
        pos.put()
        blo.put()
        self.response.out.write('</pre></body></html>')


class display_all(webapp2.RequestHandler):
    def get(self,blog_name):
        #self.response.out.write('%s' %(cgi.escape(self.request.get('blog_name'))))
        #self.response.out.write(cgi.escape(self.request.get('blog_name')))
        x=self.request.get('blog_name')
        #self.response.out.write('%s' %x)
        posts= db.GqlQuery("SELECT * FROM Post WHERE blog_name = :1 ",x )
        for post in posts:
            self.response.out.write('<div>%s</div>'%(post.title))
            self.response.out.write('<div>%s</div>'%(post.content))


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:         
            self.response.out.write('Hello <em>%s</em>! Create a blog[<a href="%s">sign out</a>] ' % (
            user.email(), users.create_logout_url(self.request.uri)))
            self.response.out.write('<br><br>')
            all_blogs=db.GqlQuery("SELECT Distinct name FROM Blog")
            for blog in all_blogs:
              self.response.out.write('<div><a href="/display_all/?blog_name=%s">%s</a></div>' % (
              blog.name,blog.name))
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
    ('/article', blog_display),
    ('/display_all/(.*)',display_all)
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()