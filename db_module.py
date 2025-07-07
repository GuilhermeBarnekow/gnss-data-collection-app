import sqlite3
import threading
import time

class Database:
    def __init__(self, db_path='gps_data.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self.create_tables()
        self.cache = []
        self.cache_limit = 100  # Number of records before flushing to DB
        self.flush_interval = 5  # seconds
        self.last_flush_time = time.time()
        self._start_flush_thread()

    def create_tables(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gps_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    latitude REAL,
                    longitude REAL,
                    hectares_covered REAL
                )
            ''')
            self.conn.commit()

    def add_record(self, latitude, longitude, hectares_covered):
        with self.lock:
            self.cache.append((latitude, longitude, hectares_covered))
            current_time = time.time()
            if len(self.cache) >= self.cache_limit or (current_time - self.last_flush_time) >= self.flush_interval:
                self.flush_cache()

    def flush_cache(self):
        if not self.cache:
            return
        with self.lock:
            cursor = self.conn.cursor()
            cursor.executemany('''
                INSERT INTO gps_data (latitude, longitude, hectares_covered)
                VALUES (?, ?, ?)
            ''', self.cache)
            self.conn.commit()
            self.cache.clear()
            self.last_flush_time = time.time()

    def _start_flush_thread(self):
        def flush_periodically():
            while True:
                time.sleep(self.flush_interval)
                self.flush_cache()
        thread = threading.Thread(target=flush_periodically, daemon=True)
        thread.start()

    def close(self):
        self.flush_cache()
        self.conn.close()
