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
  
5. Funzione per aggiungere un contatto alla lista dei contatti di un utente
   def add_contact(username, contact)
   - Parametri: username (string), contact (string)
   - Output: Restituisce un messaggio di successo o errore.
   - Descrizione: Aggiunge un contatto alla lista dei contatti dell'utente se il contatto esiste.

6. Funzione per impostare lo stato "Do Not Disturb" (DND) di un utente
   def set_dnd(username, dnd)
   - Parametri: username (string), dnd (string, 'true' o 'false')
   - Output: Restituisce un messaggio di successo.
   - Descrizione: Imposta lo stato DND per un utente, salvando il valore nel database Redis.

7. Funzione per inviare un messaggio da un utente a un altro
   def send_message(sender, recipient, message, timed_chat=False)
   - Parametri: sender (string), recipient (string), message (string), timed_chat (boolean, opzionale)
   - Output: Restituisce un messaggio di successo o errore.
   - Descrizione: Invia un messaggio da un utente a un altro, gestendo anche le chat temporizzate se timed_chat è impostato su True.

8. Funzione per ottenere i messaggi tra due utenti
   def get_messages(user1, user2)
   - Parametri: user1 (string), user2 (string)
   - Output: Restituisce una lista di messaggi.
   - Descrizione: Recupera la cronologia dei messaggi tra due utenti.
  
9. Funzione per eliminare un messaggio specifico dalla chat tra due utenti
   def delete_message(user1, user2, message)
   - Parametri: user1 (string), user2 (string), message (string)
   - Output: Restituisce un messaggio di successo o errore.
   - Descrizione: Elimina un messaggio specifico dalla cronologia chat tra due utenti.

10. Funzione per eliminare l'intera chat tra due utenti
    def delete_chat(user1, user2)
    - Parametri: user1 (string), user2 (string)
    - Output: Restituisce un messaggio di successo.
    - Descrizione: Elimina l'intera cronologia chat tra due utenti.

11. Funzione per ascoltare le notifiche 
    def listen_for_notifications(username)
    - Parametri: username (string)
    - Output: Nessuno, stampa le notifiche ricevute.
    - Descrizione: Ascolta le notifiche di nuovi messaggi per un utente specifico e stampa i messaggi ricevuti.
