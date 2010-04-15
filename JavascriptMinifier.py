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
from JSpacker import JavaScriptPacker

class JavascriptMinifier(Minifier):
	'''Minifies CSS

	Use as any other Minifier:
		JavascriptMinifier('$(document).load(...').minify().get()
	'''

	def minify(self, content = None, force = False):
		'''Applies all the other minification methods.'''
		super(JavascriptMinifier, self).minify(content)
		packed = JavaScriptPacker().pack(self.content, compaction=False, encoding=62, fastDecode=False)
		if len(packed)*1.1 < len(self.content) or force:
			self.content = packed
		return self