#!/usr/bin/python
# encoding: utf-8

'''
Copyright (c) 2009 Monika Pudlovskyte.

This file is part of PyMins.

PyMins is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyMins is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyMins.  If not, see <http://www.gnu.org/licenses/>.
'''

import unittest

from HtmlMinifier import HtmlMinifier

# For validity checks
import tempfile
import poster.encode
from poster.streaminghttp import register_openers
import urllib2

class Error(Exception):
	pass

class Tags(unittest.TestCase):
	def testSimpleCase(self):
		result = HtmlMinifier('<html><body>Foo!</body></html>').removeTags().get()
		self.assertEqual('Foo!', result)

	def testPositiveCase(self):
		result = HtmlMinifier('<html><body class="quux">Foo!</body></html>').removeTags().get()
		self.assertEqual('<body class="quux">Foo!</body>', result)

class Whitespace(unittest.TestCase):
	def testImageCase(self):
		result = HtmlMinifier('<p>My cat: <img src=""> <img src="">.</p>').removeWhitespace().get()
		self.assertEqual('<p>My cat: <img src=""> <img src="">.</p>', result)

	def testSpacesBetweenTagsCase(self):
		result = HtmlMinifier('<html>   <p>Foo</p> </html>').removeWhitespace().get()
		self.assertEqual('<html><p>Foo</p></html>', result)

class AttributeQuotes(unittest.TestCase):
	def testSimple(self):
		result = HtmlMinifier.AttributeCleaner('<foo bar="quux">').minify().get()
		self.assertEqual('<foo bar=quux>', result)

	def testValueWithSpaces(self):
		result = HtmlMinifier.AttributeCleaner('<foo bar="quux baz">').minify().get()
		self.assertEqual('<foo bar="quux baz">', result)

class AttributeEmpty(unittest.TestCase):
	def testSimple(self):
		result = HtmlMinifier.AttributeCleaner('<foo bar="">').minify().get()
		self.assertEqual('<foo>', result)

	def testSingularQuotes(self):
		result = HtmlMinifier.AttributeCleaner("<foo bar=''>").minify().get()
		self.assertEqual('<foo>', result)

	def testMultiple(self):
		result = HtmlMinifier.AttributeCleaner("<foo alt='' title=''>").minify().get()
		self.assertEqual("<foo>", result)

	def testComplicatedAttribute(self):
		result = HtmlMinifier.AttributeCleaner("<foo onclick='try bar=\"\"'").minify().get()
		self.assertEqual("<foo onclick='try bar=\"\"'", result)

class AttributeSingular(unittest.TestCase):
	def testSimple(self):
		result = HtmlMinifier.AttributeCleaner("<foo selected='selected'>").minify().get()
		self.assertEqual('<foo selected>', result)

	def testMultiple(self):
		result = HtmlMinifier.AttributeCleaner("<foo defer='defer' noresize=noresize>").minify().get()
		self.assertEqual("<foo defer noresize>", result)

class AttributeComplicated(unittest.TestCase):
	def testOne(self):
		result = HtmlMinifier.AttributeCleaner('''<html>
			<head>
				<title>Foo bar</title>
			</head>
			<body id="main">
				<p class="foo" boras=batas defer="defer" noresize>
					Let's gather to the next party!"")
					<img src="" style="onresize='bar'">
				</p>
			</body>
		</html>''').minify().get()
		self.assertEqual('''<html>
			<head>
				<title>Foo bar</title>
			</head>
			<body id=main>
				<p class=foo defer boras=batas noresize>
					Let's gather to the next party!"")
					<img style="onresize='bar'">
				</p>
			</body>
		</html>''', result)

class Validity(unittest.TestCase):
	validatorServer = 'validator.w3.org'
	validatorUrl = '/check'

	def testHomepage(self):
		html = open('TestData/ValidateHomepage.in', 'r').read()
		html = HtmlMinifier(html).minify().get()
		valid = self.validate(html)
		if not valid:
			open('TestData/ValidateHomepage.min', 'w').write(html)
		self.assertTrue(valid)

	def validate(self, html):
		register_openers()
		datagen, headers = poster.encode.multipart_encode([
			poster.encode.MultipartParam('output', 'soap12'),
			poster.encode.MultipartParam('fragment', html)
		])
		request = urllib2.Request(
			'http://%s%s' % (self.validatorServer, self.validatorUrl),
			datagen, headers)
		try:
			answer = urllib2.urlopen(request).read()
		except urllib2.HTTPError, e:
			if e.code == 404:
				raise Error('The validator URL is invalid.')
			else:
				raise Error('''Problem connecting the validation server.
					Code %d, message "%s"''' % (e.code, e.msg))

		return answer.find('<m:validity>true</m:validity>') > -1

if __name__ == "__main__":
    unittest.main()