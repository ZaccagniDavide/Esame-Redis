import redis
import hashlib
from datetime import datetime, timedelta
import threading

# Connessione al database Redis
r = redis.StrictRedis(
    host='redis-14639.c8.us-east-1-3.ec2.redns.redis-cloud.com',
    port=14639,
    db=0,
    decode_responses=True,
    password='3Xy7jwkrKb1WpzoDsRNR0jNQqLcQeeQa'
)

# Funzione per registrare un nuovo utente
def register(username, password):
    if r.hexists('users', username):
        return 'Username already exists'
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    r.hset('users', username, hashed_password)
    return 'User registered successfully'

# Funzione per effettuare il login di un utente
def login(username, password):
    stored_password = r.hget('users', username)
    if stored_password and stored_password == hashlib.sha256(password.encode()).hexdigest():
        return 'Login successful'
    return 'Invalid username or password'

# Funzione per cercare utenti in base a una query
def search_users(query):
    users = [user for user in r.hkeys('users') if query in user]
    return users

# Funzione per aggiungere un contatto alla lista dei contatti di un utente
def add_contact(username, contact):
    if not r.hexists('users', contact):
        return 'Contact does not exist'
    r.sadd(f'contacts:{username}', contact)
    return 'Contact added successfully'

# Funzione per impostare lo stato "Do Not Disturb" (DND) di un utente
def set_dnd(username, dnd):
    r.hset('dnd', username, dnd)
    return 'DND status updated'

# Funzione per inviare un messaggio da un utente a un altro
def send_message(sender, recipient, message, timed_chat=False):
    if r.hget('dnd', recipient) == 'true':
        return 'Cannot deliver message, user is in DND mode'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_entry = f'>{message}\t[{timestamp}]'
    
    # Invia il messaggio alla cronologia chat di entrambi gli utenti
    r.rpush(f'chat:{sender}:{recipient}', message_entry)
    r.rpush(f'chat:{recipient}:{sender}', f'<{message}\t[{timestamp}]')
    
    # Pubblica una notifica sul canale del destinatario
    r.publish(f'notifications:{recipient}', message_entry)
    
    # scadenza
    if timed_chat:
        r.expire(f'chat:{sender}:{recipient}', 60)
        r.expire(f'chat:{recipient}:{sender}', 60)
    
    return 'Message sent successfully'

# Funzione per ottenere i messaggi tra due utenti
def get_messages(user1, user2):
    return r.lrange(f'chat:{user1}:{user2}', 0, -1)

# Funzione per eliminare un messaggio specifico dalla chat tra due utenti
def delete_message(user1, user2, message):
    chat_key_1 = f'chat:{user1}:{user2}'
    chat_key_2 = f'chat:{user2}:{user1}'
    
    if r.lrem(chat_key_1, 1, message):
        r.lrem(chat_key_2, 1, message)
        return 'Message deleted successfully'
    return 'Message not found'

# Funzione per eliminare l'intera chat tra due utenti
def delete_chat(user1, user2):
    r.delete(f'chat:{user1}:{user2}')
    r.delete(f'chat:{user2}:{user1}')
    return 'Chat deleted successfully'

# Funzione per ascoltare le notifiche (eseguire questa funzione in un thread separato o in un processo separato)
def listen_for_notifications(username):
    pubsub = r.pubsub()
    pubsub.subscribe(f'notifications:{username}')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"New message for {username}: {message['data']}")

# Esempio di utilizzo
user1 = 'utente1'
user2 = 'utente2'

print(register(user1, 'password123'))
print(register(user2, 'password456'))

print(login(user1, 'password123'))
print(add_contact(user1, user2))

# Avvia un thread per ascoltare le notifiche per user2
notification_thread = threading.Thread(target=listen_for_notifications, args=(user2,))
notification_thread.start()

print(send_message(user1, user2, 'Ciao, come stai?'))
print(send_message(user2, user1, 'Tutto bene, grazie!'))

messages = get_messages(user1, user2)
print(f"Chat con {user2}")
for message in messages:
    print(message)

# Invia un messaggio temporizzato
print(send_message(user1, user2, 'Questo è un messaggio temporizzato', timed_chat=True))
