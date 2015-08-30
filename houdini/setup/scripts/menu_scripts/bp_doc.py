import webbrowser
import sys

# Open in new tab
new = 2

# URL dictionary
url = { 'wiki' : 'https://www.filmakademie.de/wiki/x/MpzQ',
		'shotlist': '',
		'assetlist': 'https://docs.google.com/spreadsheets/d/17Eeo2JhRvx4Xtb2xR_Of_8HgqUjsxGm_UBNo9NqaWi8',
		'fxlist': 'https://docs.google.com/spreadsheets/d/1mOZhVGn7Afemrlo2OL3uWkZfNB3X8e_5kFoD1QpXcn4/edit#gid=1956037604'
}

arg = sys.argv[1]

if(len(url)>0):
	webbrowser.open(url[arg], new=new)
else:
	print('URL not specified')