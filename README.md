# Esame-Redis
1. Connessione al database Redis: la connessione al database Redis viene effettuata utilizzando redis.StrictRedis. È necessario specificare host, port, db, decode_responses e password.

2. Funzione per registrare un nuovo utente
   def register(username, password)
   - Parametri: username (string), password (string)
   - Output: Restituisce un messaggio di successo o errore.
   - Descrizione: Registra un nuovo utente inserendo la password e salvandola nel database Redis.

3. Funzione per effettuare il login di un utente
   def login(username, password)
   - Parametri: username (string), password (string)
   - Output: Restituisce un messaggio di successo o errore.
   - Descrizione: Verifica le credenziali dell'utente confrontando la password hashata con quella memorizzata.

4. Funzione per cercare utenti in base a una query
   def search_users(query)
   - Parametri: query (string)
   - Output: Restituisce una lista di utenti che corrispondono alla query.
   - Descrizione: Cerca utenti il cui nome contiene la query specificata.
