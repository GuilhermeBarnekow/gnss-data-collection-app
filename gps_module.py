import serial
import threading
import time
import random

class GNSSModule:
    def __init__(self, port=None, baudrate=115200, simulation=False):
        self.simulation = simulation
        if not self.simulation:
            # Use default port if not specified
            if port is None:
                # Common serial ports for Raspberry Pi
                possible_ports = ['/dev/serial0', '/dev/ttyAMA0', '/dev/ttyS0']
                for p in possible_ports:
                    try:
                        self.ser = serial.Serial(p, baudrate, timeout=1)
                        print(f"Connected to GNSS module on port {p}")
                        break
                    except serial.SerialException:
                        continue
                else:
                    raise serial.SerialException("Could not open any serial port for GNSS module.")
            else:
                self.ser = serial.Serial(port, baudrate, timeout=1)
        else:
            self.sim_data_index = 0
            self.sim_data = self._generate_sim_data()
            self.lock = threading.Lock()
            self.running = True
            self.thread = threading.Thread(target=self._simulate_data_thread, daemon=True)
            self.thread.start()

    def _generate_sim_data(self):
        # Generate simulated GPS data points (latitude, longitude)
        base_lat = -23.5505  # Example base location (São Paulo)
        base_lon = -46.6333
        data = []
        for i in range(1000):
            lat = base_lat + (random.random() - 0.5) * 0.01
            lon = base_lon + (random.random() - 0.5) * 0.01
            data.append((lat, lon))
        return data

    def _simulate_data_thread(self):
        while self.running:
            time.sleep(1)
            with self.lock:
                self.sim_data_index = (self.sim_data_index + 1) % len(self.sim_data)

    def read_data(self):
        if self.simulation:
            with self.lock:
                lat, lon = self.sim_data[self.sim_data_index]
            # Return simulated NMEA-like string or tuple
            return f"$GPGGA,{lat},{lon}"
        else:
            if self.ser.in_waiting:
                line = self.ser.readline().decode('ascii', errors='replace').strip()
                # Here you can parse NMEA sentences or other GNSS data
                return line
            return None

    def stop(self):
        if self.simulation:
            self.running = False
            self.thread.join()
