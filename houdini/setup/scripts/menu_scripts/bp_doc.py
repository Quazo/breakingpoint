import webbrowser
import sys

# Open in new tab
new = 2

# URL dictionary
url = { 'wiki' : 'https://www.filmakademie.de/wiki/x/MpzQ',
		'shotlist': '',
		'assetlist': 'https://docs.google.com/spreadsheets/d/17Eeo2JhRvx4Xtb2xR_Of_8HgqUjsxGm_UBNo9NqaWi8'
}

arg = sys.argv[1]

if(len(url)>0):
	webbrowser.open(url[arg], new=new)
else:
	print('URL not specified')