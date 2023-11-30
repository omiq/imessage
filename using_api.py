from imessage_reader import fetch_data

DB_PATH = "/Users/chrisg/library/messages/chat.db"

# Create a FetchData instance
fd = fetch_data.FetchData(DB_PATH)
messages  = fd.get_messages()
print(messages[0])

