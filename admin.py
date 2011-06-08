#!/usr/bin/env python
#
# Copyright 2011 Daniel Halperin <daniel@halper.in>
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
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from datetime import datetime
import cgi

class Redirection(db.Model):
	url = db.LinkProperty()
	added = db.DateTimeProperty(auto_now_add=True)
	last = db.DateTimeProperty()
	hitcount = db.IntegerProperty(default=0)

	def update(self):
		self.hitcount += 1
		self.last = datetime.now()


class AddPage(webapp.RequestHandler):
	def post(self):
		name = self.request.get('name')
		url = self.request.get('url')
		if len(name) == 0:
			self.response.out.write('Bad name '+cgi.escape(name))
			return
		if name[0] != '/':
			name = '/' + name
		if name.find('/admin') == 0:
			self.response.out.write('Bad name '+cgi.escape(name))
			return
		r =  Redirection(key_name=name)
		try:
			r.url = url
		except db.BadValueError:
			self.response.out.write('Bad URL '+cgi.escape(url))
			return
		r.put()
		self.redirect('/admin/', permanent=False)

	def get(self):
		self.post()


class DelPage(webapp.RequestHandler):
	def post(self):
		name = self.request.get('name')
		name_k = db.Key.from_path('Redirection', name)
		result = db.get(name_k)
		if not result:
			self.response.out.write('name not found '+cgi.escape(name))
			return
		result.delete()
		self.redirect('/admin/', permanent=False)

	def get(self):
		self.post()


class AdminPage(webapp.RequestHandler):
	def get(self):
		links = db.GqlQuery("SELECT * "
				    "FROM Redirection "
				    "ORDER BY added")

		if links.count(1) == 0:
			self.response.out.write("No links<BR>\n")

		for link in links:
			delurl = "/admin/del?name=%s" %(link.key().name())
			msg = "%s -> <a href='%s'>%s</a> : count=%d : added=%s : last=%s" %(link.key().name(), link.url, link.url, link.hitcount, str(link.added), str(link.last))
			self.response.out.write( "<a href='" + delurl + "'>X</a> " + msg + '<br>\n')

		self.response.out.write('<br>\n')
		self.response.out.write("""
		<form action="/admin/add" method="post">
			<div>name: <input name="name"> url: <input name="url" value="http://"> <input type="submit"></div>
		</form>
		""")

def main():
    application = webapp.WSGIApplication([('/admin/*', AdminPage), ('/admin/add', AddPage), ('/admin/del', DelPage)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
