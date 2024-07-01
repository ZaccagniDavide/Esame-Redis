import redis
import hashlib
from datetime import datetime

# Connessione al database Redis
r = redis.StrictRedis(
    host='redis-14639.c8.us-east-1-3.ec2.redns.redis-cloud.com',
    port=14639,
    db=0,
    decode_responses=True,
    password='3Xy7jwkrKb1WpzoDsRNR0jNQqLcQeeQa'
)

def register(username, password):
    if r.hexists('users', username):
        return 'Username already exists'
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    r.hset('users', username, hashed_password)
    return 'User registered successfully'

def login(username, password):
    stored_password = r.hget('users', username)
    if stored_password and stored_password == hashlib.sha256(password.encode()).hexdigest():
        return 'Login successful'
    return 'Invalid username or password'

def search_users(query):
    users = [user for user in r.hkeys('users') if query in user]
    return users

def add_contact(username, contact):
    if not r.hexists('users', contact):
        return 'Contact does not exist'
    r.sadd(f'contacts:{username}', contact)
    return 'Contact added successfully'

def set_dnd(username, dnd):
    r.hset('dnd', username, dnd)
    return 'DND status updated'

def send_message(sender, recipient, message):
    if r.hget('dnd', recipient) == 'true':
        return 'Cannot deliver message, user is in DND mode'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    r.rpush(f'chat:{sender}:{recipient}', f'>{message}\t[{timestamp}]')
    r.rpush(f'chat:{recipient}:{sender}', f'<{message}\t[{timestamp}]')
    return 'Message sent successfully'

def get_messages(user1, user2):
    return r.lrange(f'chat:{user1}:{user2}', 0, -1)

# Definizione utenti
user1 = 'utente1'
user2 = 'utente2'

# Utilizzo delle funzioni
print(register(user1, 'password123'))
print(register(user2, 'password456'))

print(login(user1, 'password123'))
print(add_contact(user1, user2))

print(send_message(user1, user2, 'Ciao, come stai?'))
print(send_message(user2, user1, 'Tutto bene, grazie!'))

messages = get_messages(user1, user2)

# Output
print(f"Chat con {user2}")
for message in messages:
    print(message)

'''def delete_message(user1, user2, message):
    chat_key_1 = f'chat:{user1}:{user2}'
    chat_key_2 = f'chat:{user2}:{user1}'
    
    if r.lrem(chat_key_1, 1, message):
        r.lrem(chat_key_2, 1, message)
        return 'Message deleted successfully'
    return 'Message not found'

def delete_chat(user1, user2):
    r.delete(f'chat:{user1}:{user2}')
    r.delete(f'chat:{user2}:{user1}')
    return 'Chat deleted successfully'

'''






