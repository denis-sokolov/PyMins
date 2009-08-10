#!/usr/bin/python

class Minifier:
	'''Minifies different kinds of text.
	
	Usual usage:
		Minifier('text to minify').minify().get()
	
	You can use the same object for different strings to avoid creating
	multiple objects:
		min = Minifier()
		min.minify('text').get()
		min.minify('other text').get()
	
	In most implementations you should be able to apply only selected
	minifications:
		HtmlMinifier('<p></p>').removeComments().removeWhitespace().get()
	'''
	def __init__(self, content = ''):
		self.content = content
	
	def get(self):
		return self.content
	
	def minify(self, content = None):
		if (not content is None):
			self.content = content
		return self