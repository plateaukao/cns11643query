#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import webapp2
import query_word

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/query" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Search"></div>
    </form>
  </body>
</html>
"""
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class QueryHandler(webapp2.RequestHandler):
    def post(self):
        arg = cgi.escape(self.request.get('content'))
        html = query_word.generateHTML(arg)
        self.response.write(arg)
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/query', QueryHandler)
], debug=True)
