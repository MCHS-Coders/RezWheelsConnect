import sqlite3
import uuid
import os
import datetime

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


class P2PManager:
    def __init__(self):
        """Initialize the P2P system and create necessary tables."""
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Creates tables for users and messages if they do not exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uuid TEXT PRIMARY KEY,
                address TEXT NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_uuid TEXT NOT NULL,
                receiver_uuid TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_uuid) REFERENCES users (uuid),
                FOREIGN KEY (receiver_uuid) REFERENCES users (uuid)
            )
        """)

        self.conn.commit()

    def generate_uuid(self):
        """Generates a unique UUID for a new user."""
        return str(uuid.uuid4())

    def register_user(self, address):
        """
        Registers a new user with a generated UUID.
        :param address: The user's address (e.g., IP:Port)
        :return: The generated UUID
        """
        user_uuid = self.generate_uuid()
        self.cursor.execute("INSERT INTO users (uuid, address) VALUES (?, ?)", (user_uuid, address))
        self.conn.commit()
        return user_uuid

    def get_user_address(self, user_uuid):
        """
        Retrieves a user's address by UUID.
        :param user_uuid: The UUID of the user
        :return: The user's address or None if not found
        """
        self.cursor.execute("SELECT address FROM users WHERE uuid = ?", (user_uuid,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def list_users(self):
        """
        Lists all registered users.
        :return: A dictionary of {uuid: address}
        """
        self.cursor.execute("SELECT * FROM users")
        users = {row[0]: row[1] for row in self.cursor.fetchall()}
        return users

    def send_message(self, sender_uuid, receiver_uuid, message):
        """
        Stores a message in the database.
        :param sender_uuid: UUID of the sender
        :param receiver_uuid: UUID of the receiver
        :param message: Message text
        :return: Confirmation
        """
        self.cursor.execute("""
            INSERT INTO messages (sender_uuid, receiver_uuid, message) 
            VALUES (?, ?, ?)
        """, (sender_uuid, receiver_uuid, message))
        
        self.conn.commit()
        return {"status": "Message sent successfully"}

    def get_messages(self, user_uuid):
        """
        Retrieves all messages where the given UUID is the sender or receiver.
        :param user_uuid: UUID of the user
        :return: List of messages
        """
        self.cursor.execute("""
            SELECT sender_uuid, receiver_uuid, message, timestamp 
            FROM messages 
            WHERE sender_uuid = ? OR receiver_uuid = ?
            ORDER BY timestamp DESC
        """, (user_uuid, user_uuid))

        messages = [
            {
                "sender": row[0],
                "receiver": row[1],
                "message": row[2],
                "timestamp": row[3]
            }
            for row in self.cursor.fetchall()
        ]
        return messages


# Create an instance of P2PManager to use in __main__.py
p2p_manager = P2PManager()

if __name__ == "__main__":
    # Example usage
    print("Registering users...")
    uuid1 = p2p_manager.register_user("192.168.1.100:4000")
    uuid2 = p2p_manager.register_user("192.168.1.101:4000")
    print(f"User1 UUID: {uuid1}")
    print(f"User2 UUID: {uuid2}")

    print("\nSending a message...")
    p2p_manager.send_message(uuid1, uuid2, "Hello, this is a test message!")

    print("\nRetrieving messages for User2...")
    print(p2p_manager.get_messages(uuid2))
