
Built by https://www.blackbox.ai

---

# GNSS Data Collection Application

## Project Overview
This project is a Python application designed to interact with GNSS (Global Navigation Satellite System) devices. It reads satellite data, processes it, and stores the results in a database. The application provides a graphical interface built with Kivy, allowing users to visualize GPS data in real-time, manage settings, and track geographical changes.

## Installation
To install the necessary dependencies for this project, you need Python and pip (Python package manager) installed on your system. Follow the steps below:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) If you want to run the application with GNSS hardware, ensure you have a compatible GNSS module and that the correct serial port is set.

## Usage
To run the application, simply execute the following command in your terminal:
```bash
python main.py
```
The application will launch a Kivy interface, where you can view GPS coordinates and other related data. You can interact with the grid and observe the connection status of the GNSS device.

## Features
- **Real-time GPS Monitoring**: Displays current latitude and longitude data.
- **Data Storage**: Automatically stores GPS data in an SQLite database.
- **Dynamic Interface**: Interactive grid-based UI that changes based on collected data.
- **Simulation Mode**: (Optional) Use simulated GNSS data for testing without hardware.
- **Multithreading**: Efficient data reading and database interactions using separate threads.

## Dependencies
The project uses the following Python packages:
- `kivy`: The graphical library for building the user interface.
- `sqlite3`: For database interactions (included with Python).
- `serial`: For serial communication with the GNSS module.

Refer to `requirements.txt` for the complete list of dependencies.

## Project Structure
The project's files are organized as follows:

```
/gnss-data-collection-app
│
├── main.py              # Entry point of the application, GUI setup and logic controller.
├── gps_module.py        # Handles communication with GNSS device (real or simulated).
├── db_module.py         # Manages database operations for storing GPS data.
├── ui.kv                # Kivy file defining the layout and style of the application interface.
├── requirements.txt      # Required Python libraries for the project.
└── next-env.d.ts        # Type definitions for Next.js (not directly related but part of the project context).
```

## Notes
- Before using with actual GNSS hardware, ensure the correct serial port configurations are set in `gps_module.py`.
- The application may require additional permissions on some operating systems to access serial devices.

For any issues or contributions, please feel free to open an issue or pull request within the project repository.

---
This README provides a brief yet comprehensive guide to using the GNSS Data Collection Application. For further details, you may refer to the documentation provided in `DOCUMENTATION_PT_BR.md`.