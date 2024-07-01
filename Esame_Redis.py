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
