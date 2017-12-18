"""
Example usage:
$ python predict_custom_input.py "new jerry seinfeld show releases"
new jerry seinfeld show releases
['news']
['e']

"""

import naive_bayes
import sys


if __name__ == '__main__':
	mysql_obj_identifier = naive_bayes.mysql_connection('news_identifier')
	mysql_obj_classifier = naive_bayes.mysql_connection('news_classifier')
	input_text = sys.argv[1]
	input_text = naive_bayes.normalize_text(input_text)
	print input_text
	identifier_output = naive_bayes.test([input_text], mysql_obj_identifier)
	print identifier_output
	if identifier_output[0] == 'news':
		print naive_bayes.test([input_text], mysql_obj_classifier)
