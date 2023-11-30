import os
import re
import sqlite3
import datetime

def extract_first_url(text):
    # Enhanced regular expression pattern for a full URL
    url_pattern = r'https?://(?:www\.)?[-\w]+(\.\w[-\w]*)+([/?#][^\s]*)?'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)  # Returns the matched URL
    else:
        return None



#chatdb_location = "/Users/" + os.getlogin() + "/library/messages/chat.db"
chatdb_location = "/Volumes/External/iMessage-Backup/chat.db"

# Connect to the database and execute a query to join message and handle tables
conn = sqlite3.connect(chatdb_location)
cursor = conn.cursor()
query = """
    SELECT message.ROWID, message.date, message.text, message.attributedBody, message.is_from_me, message.cache_roomnames
    FROM message
    WHERE message.is_from_me 
    ORDER BY message.date DESC
    
"""

#LIMIT 10

results = cursor.execute(query).fetchall()

# Initialize an empty list for messages
links = {}

# Loop through each result row and unpack variables
for result in results:
    rowid, date, text, attributed_body, is_from_me, cache_roomname = result

    url = ""

    # Convert date from Apple epoch time to standard format using datetime module if human_readable_date is True  
    date_string = '2001-01-01'
    mod_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    unix_timestamp = int(mod_date.timestamp())*1000000000
    new_date = int((date+unix_timestamp)/1000000000)
    date = datetime.datetime.fromtimestamp(new_date).strftime("%Y-%m-%d %H:%M:%S")

    if text:
        url = extract_first_url(text)
    else:

        # Decode and extract relevant information from attributed_body using string methods 
        attributed_body = attributed_body.decode('utf-8', errors='replace')
        if "NSNumber" in str(attributed_body):
            attributed_body = str(attributed_body).split("NSNumber")[0]
            if "NSString" in attributed_body:
                attributed_body = str(attributed_body).split("NSString")[1]
                if "NSDictionary" in attributed_body:
                    attributed_body = str(attributed_body).split("NSDictionary")[0]
                    attributed_body = attributed_body[6:-12]
                    body = attributed_body

        url = extract_first_url(body)

    if url:
        links[date] = url

conn.close()

for link in links:
    print(link, links[link])








