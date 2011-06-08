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


class RedirPage(webapp.RequestHandler):
	def get(self):
		path = self.request.path
		path_k = db.Key.from_path('Redirection', path)
		result = db.get(path_k)
		if not result:
			self.response.set_status(404)
			return
		result.update()
		result.put()
		self.redirect(result.url, permanent=False)


def main():
    application = webapp.WSGIApplication([('/.*', RedirPage)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
