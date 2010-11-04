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
from SgmlMinifier import SgmlMinifier

class Comments(unittest.TestCase):

	def testConditionalComments(self):
		result = SgmlMinifier('foo <!--[ foo --> bar').removeComments().get()
		self.assertEqual('foo <!--[ foo --> bar', result)	

	def testDoubleComments(self):
		result = SgmlMinifier('foo <!-- foo --> bar <!-- spam --> niof').removeComments().get()
		self.assertEqual('foo  bar  niof', result)	

	def testEmptyComment(self):
		result = SgmlMinifier('foo <!----> bar').removeComments().get()
		self.assertEqual('foo  bar', result)
		
	def testEmptyComment2(self):
		result = SgmlMinifier('foo <!-- --> bar').removeComments().get()
		self.assertEqual('foo  bar', result)
		
	def testSimpleCase(self):
		result = SgmlMinifier('foo <!-- foo --> bar').removeComments().get()
		self.assertEqual('foo  bar', result)  	 	
		
class Whitespace(unittest.TestCase):
	def testSimpleCase(self):
		result = SgmlMinifier(
			'<html>\n   <title>\n       Foo\n   </title>\n</html>').removeWhitespace().get()
		self.assertEqual('<html> <title> Foo </title> </html>', result) 
		
	def testSimpleCase2(self):
		result = SgmlMinifier('<html>Foo      bar</html>').removeWhitespace().get()
		self.assertEqual('<html>Foo bar</html>', result)
		
	def testTag(self):
		result = SgmlMinifier('<body > <  / body >').removeWhitespace().get()
		self.assertEqual('<body> </body>', result)
		
	def testSelfClosingTag(self):
		result = SgmlMinifier('<  br / >').removeWhitespace().get()
		self.assertEqual('<br/>', result)

if __name__ == "__main__": 
    unittest.main()  