import re
def clean(line):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\u2700-\u27BF"  # Dingbats
                               u"\U0001F30D-\U0001F567"  # Other additional symbols
                               u"\u24C2-\U0001F251"  # Enclosed characters
                               u"\U0001F600-\U0001F64F"  # Additional emoticons
                               u"\U0001F300-\U0001F5FF"  # Other Characters
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    clean_line=line
    clean_line = emoji_pattern.sub(r'', clean_line)  # no emoji
    #print clean_line
    # Replace the https with [URL]
    clean_line1 = re.sub('(\n)', ' ', clean_line)
    clean_line1=re.sub('(https:\/\/t\.co.*?( |\t|\n|\r|\f|\v|$))','',clean_line1)
    #printable = set(string.printable)
    #clean_line2=filter(lambda x: x in printable, clean_line1)
    clean_line2=clean_line1
    # length=len(clean_line2)
    return clean_line2