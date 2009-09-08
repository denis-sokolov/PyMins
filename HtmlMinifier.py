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
from SgmlMinifier import SgmlMinifier
import re

class HtmlMinifier(SgmlMinifier):
	'''Minifies HTML

	Use as any other Minifier:
		HtmlMinifier('<html>...').minify().get()
	'''
	inlineTags = 'a|abbr|acronym|dfn|em|strong|code|samp|kbd|var|b|i|big|small|strike|s|tt|u|font|span|br|bdo|cite|del|ins|q|script|sub|sup|img|button|input|label'

	def minify(self, content = None):
		'''Applies all the other minification methods.'''
		Minifier.minify(self, content)
		self.removeWhitespace().removeComments()
		self.content = self.AttributeCleaner(self.content).minify().get()
		return self


	def removeTags(self):
		'''Removes not needed HTML tags'''
		for tag in ['body','/colgroup','/dd','/dt','head','html','/li',
			'/option','/p','tbody','/td','/tfoot','/th','/thead','/tr']:
			if tag[0] == '/':
				self.content = self.content.replace('<%s>' % tag,'')
			else:
				length = len(self.content)
				self.content = self.content.replace('<%s>' % tag,'')
				if len(self.content) < length:
					self.content = self.content.replace('</%s>' % tag,'')
		return self

	def removeWhitespace(self):
		'''Changes all whitespace to a single space character.

		In addition, removes spaces between block level tags:
			<html> <head> <title> becomes
			<html><head><title>, but
			<p>Foo <img> <span> stays the same.'''
		SgmlMinifier.removeWhitespace(self)
		self.content = re.sub(r'> \<(?P<closingSlash>/?)(?!(%s)[^a-zA-Z])' % self.inlineTags,
					r'><\g<closingSlash>', self.content)
		# This is for reference on how the hell that just worked.
		#self.content = re.sub(r'''(?x)
		#			>   # The first tag ends here.
		#			\   # THe space between the tags.
		#			\<  # The second tag starts here.
		#			(?P<closingSlash>/?)  # We store the slash symbol if the second tag is closing
		#			(?! # Negative lookahead
		#				(%s) # ...for any of self.inlineTags
		#				[^a-zA-Z] # Make sure the second (inline) tag name has ended (A vs. AREA case)
		#			)
		#			''' % self.inlineTags,
		#			r'><\g<closingSlash>', self.content)
		return self

	class AttributeCleaner(Minifier):
		'''Cleans attributes in HTML.'''
		quotes = '"|\''
		attributeValueWithoutQuotes = '[a-zA-Z0-9-]+'
		singularAttributes = ['compact','checked','declare','defer','disabled','ismap','nohref','noshade','noresize','nowrap','multiple','readonly','selected']

		def minify(self, content = None):
			Minifier.minify(self, content)
			self.iterateAttributes()
			return self

		def iterateAttributes(self):
			'''Walk through the tags, then attributes, and rebuild them again.'''
			replace = []
			for tag in re.finditer('<(?P<tagName>[a-zA-Z]+)(?P<contents> [^>]+)>', self.content):
				attrStr = tag.groupdict()['contents']
				attributes = []
				for regexp in [
					r'(?P<name>[a-zA-Z-]+)=(%s)(?P<value>.*?)\2'	% self.quotes, # Quoted
					r'(?P<name>[a-zA-Z-]+)=(?P<value>%s)' % self.attributeValueWithoutQuotes, # Unquoted
					r'(?P<name>[a-zA-Z-]+)(?P<value>)(?!=)' # Singular
					]:
					toRemove = []
					for attr in re.finditer(regexp, attrStr):
						attrDict = attr.groupdict()
						attributes.append((attrDict['name'], attrDict['value']))
						toRemove.append((attr.start(), attr.end()))
					attrStr = self.__removePartsFromString(attrStr, toRemove)
				replace.append((tag.start(), tag.end(),
					self.__buildTag(tag.groupdict()['tagName'], attributes)))
			self.content = self.__replacePartsInString(self.content, replace)
			return self

		def __buildTag(self, tagName, attributes):
			'''Creates an HTML tag with a given name and attributes.

			Attributes must be a list of tuples (attributeName, attributeValue).'''
			atrs = []
			for name, value in attributes:
				if name in self.singularAttributes:
					atrs.append(' %s' % name)
				elif value == '':
					pass
				elif re.match("^%s$" % self.attributeValueWithoutQuotes, value):
					atrs.append(' %s=%s' % (name, value))
				else:
					atrs.append(' %s="%s"' % (name, value))
			return '<%s%s>' % (tagName, ''.join(atrs))

		def __replacePartsInString(self, string, parts):
			'''Replace certain parts in a string.

			Parts must be a list of tuples (startPosition, endPosition, withWhatToReplace)'''
			delta = 0
			for start, end, replace in parts:
				start -= delta
				end -= delta
				string = string[:start] + replace + string[end:]
				delta += end - start - len(replace)
			return string

		def __removePartsFromString(self, string, parts):
			'''Remove certain parts from a string.

			Parts must be a list of tuples (startPosition, endPosition)'''
			return self.__replacePartsInString(string,
				[(start, end, '') for start, end in parts])
