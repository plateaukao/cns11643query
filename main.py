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
import logging
import cgi
import webapp2
import query_word

MAIN_PAGE_HTML = """\
<html>
  <head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
  <script src="/js/main.js" type="text/javascript" ></script>
  </head>
  <body>
  <table width="100%">
  <tr align="center"> <td>書法 + </td> </tr>
  <tr align="center"><td>
    <div id="searchContainer">
        <form action="/query" method="post">
            <input id="field" name="content" type="text" />
            <input id="submit" name="submit" type="submit" value="Search" />
        </form>
    </div>
    </td> </tr>
    </table>
  </body>
</html>
"""
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class QueryHandler(webapp2.RequestHandler):
    def post(self):
        arg = cgi.escape(self.request.get('content'))
        logging.debug("request:%s",arg)
        html = query_word.generateHTML(arg)
        self.response.write(arg)
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/query', QueryHandler)
], debug=True)
