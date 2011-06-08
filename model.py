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
from google.appengine.ext import db
from datetime import datetime

class Redirection(db.Model):
	url = db.LinkProperty()
	added = db.DateTimeProperty(auto_now_add=True)
	last = db.DateTimeProperty()
	hitcount = db.IntegerProperty(default=0)

	def update(self):
		self.hitcount += 1
		self.last = datetime.now()
