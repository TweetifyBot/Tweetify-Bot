import pyrebase
firebaseConfig = {
    "apiKey": "Enter you firebase apiKey",
    "authDomain": "Enter you firebase authDomain",
    "databaseURL": "Enter you firebase databaseURL",
    "storageBucket": "Enter you firebase storageBucket"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
username_server_list = {}

def get_chat_id_from_the_data_base():
    db_data_chat_id = db.child("Chat ID").get().val()

    for chat_id in db_data_chat_id:
        username_server_list[chat_id] = []
        db_data_username = db.child("Chat ID").child(chat_id).get().val()

        for username in db_data_username:
            username_server_list[chat_id].append(username)

    return username_server_list

def update_username_to_the_data_base(chat_id, data):
    db.child("Chat ID").child(chat_id).set(data)
