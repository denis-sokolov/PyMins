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

from Minifier import Minifier
import re

class SgmlMinifier(Minifier):
	def minify(self, content = None):
		Minifier.minify(self, content)
		self.removeWhitespace().removeComments()
		return self

	def removeComments(self):
		self.content = self.content.replace('<!---->','')
		self.content = re.sub(r'\<!--[^[].*?-->', '', self.content)
		return self

	def removeWhitespace(self):
		self.content = re.sub(r'\s+', ' ', self.content)
		self.content = self.content.replace('< ', '<').replace('</ ', '</')
		self.content = self.content.replace(' >','>').replace(' />', '/>')
		return self


	#	'' ==
	#	''' == SYNTAX ERROR
	#	'\'' == '
	#	'\\ foo' == \ foo
	#	r'\\ foo' == \\ foo
	#	r' \'  ' ==  \'
	#	r'\'' == \'
	#	r'\' == SYNTAX ERROR