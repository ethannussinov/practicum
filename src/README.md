# clean.py

## steps taken to clean raw data files
1. Use regex to cut everything between `*** START OF THE PROJECT GUTENBERG EBOOK` and `*** END OF THE PROJECT GUTENBERG EBOOK`, remove residual licensing notes and chapter numbers.
2. Normalize whitespace and punctuation
3. Enforce encoding UTF-8