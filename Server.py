# Listen for handshake request. Accept no more than 3 clients.

# Assign client name in format, Client01, Client02, etc

''' Cache info about accepted clients of current session, (store only in memory): 
    - Time and date connection was accepted
    - Time and date connection was finished
'''

# Listen for any tcp messages with a string. Once recived echo same string back to client
# with 'ACK' appended at the end. 

# Listen for an 'exit' message. Upon recieval, terminate connection with that specific client.

# Listen for a 'list' message. Upon recieval, give a list of files, and wait for response.
# Upon response send the clients desired file. If name invalid ask again.
