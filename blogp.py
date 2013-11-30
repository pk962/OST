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

class Articles(db.Model):

  title = db.StringProperty(required=True)
  category= db.StringProperty(required=True,
                           choices=set(["technology", "science", "food","books"]))
  create_date = db.DateTimeProperty(auto_now_add=True)
  content=db.TextProperty()
  author=db.UserProperty()

class Blog(db.Model):
  name=db.StringProperty(required=True)
  author=db.UserProperty()

class blog_create(webapp2.RequestHandler):
    def get(self):
      user = users.get_current_user()
      if user:
            self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>] ' % (
            user.email(), users.create_logout_url(self.request.uri)))
            self.response.out.write('<br><br>')
            all_cats=db.GqlQuery("SELECT * FROM Articles")
            self.response.out.write('<form action="/article" method="post">')
            for cats in all_cats:
                self.response.out.write('<div> %s</div>'%(cats.category))

            self.response.out.write("""
                    <div>Category<select name="category">
                    <option value="science">science</option>
                    <option value="technology">technology</option>
                    <option value="food">food</option>
                    <option value="books">books</option>
                    </select> </div> 
                    <div>Blog_Title<input type="text" name="title"><br><br><br></div>
                    <div>Content</div>
                    <div><textarea name="content" rows="3" cols="60"></textarea></div>
                    <div><input type="submit" value="Submit Blog"></div>
                  
                
              """)
            self.response.out.write('</form>')
      else:
            self.redirect(users.create_login_url(self.request.uri))


class blog_display(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>Author:%s wrote:<pre>' %(users.get_current_user()))
        self.response.out.write(cgi.escape(self.request.get('title'))+"<br>")
        self.response.out.write(cgi.escape(self.request.get('content')))
        title=self.request.get('title')
        content=self.request.get('content')
        category=self.request.get('category')
        author=users.User()
        pos=Articles(title=title,category=category,content=content,author=author)
        pos.put()
        self.response.out.write('</pre></body></html>')



application = webapp2.WSGIApplication([
    ('/', blog_create),
    ('/article', blog_display)
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()