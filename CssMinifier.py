#!/usr/bin/python
# encoding: utf-8

'''
Copyright (c) 2009 Monika Pudlovskyte, Denis Sokolov.

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

class CssMinifier(Minifier):
	'''Minifies CSS

	Use as any other Minifier:
		CssMinifier('body { ...').minify().get()
	'''

	def minify(self, content = None):
		'''Applies all the other minification methods.'''
		super(CssMinifier, self).minify(content)
		self.removeComments()
		self.removeWhitespace()
		return self

	def removeComments(self):
		self.content = re.sub(r'(?s)/\*.*?\*/', '', self.content)
		return self

	def removeWhitespace(self):
		self.content = re.sub(r'\s+', ' ', self.content)
		self.content = re.sub(r' ?([{}>+:;,]) ?', r'\1', self.content)
		self.content = self.content.replace(';}','}')
		self.content = re.sub(r'}[^{}]*{}', '}', self.content)
		self.content = re.sub(r' ?! ?', '!', self.content)
		return self