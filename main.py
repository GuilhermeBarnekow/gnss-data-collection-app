import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty
from kivy.lang import Builder
from gps_module import GNSSModule
from db_module import Database

Builder.load_file('ui.kv')

from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.base import EventLoop

class GPSWidget(Widget):
    grid_cols = NumericProperty(5)
    grid_rows = NumericProperty(5)
    quadrant_colors = ListProperty([])  # List of colors for each quadrant
    gnss_connected_color = ListProperty([1, 0, 0, 1])  # Red by default (disconnected)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation_mode = False
        self.gnss = GNSSModule(port=None, baudrate=115200, simulation=self.simulation_mode)
        self.db = Database()
        self.total_hectares = 0.0
        self.quadrant_colors = [(1, 1, 1, 1)] * (self.grid_cols * self.grid_rows)  # default white
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS
        self.create_grid()
        self.keyboard = None

    def update(self, dt):
        data = self.gnss.read_data()
        if data:
            # Update GNSS connection icon to green
            self.gnss_connected_color = [0, 1, 0, 1]
            # Update lat/lon labels
            try:
                parts = data.split(',')
                if len(parts) >= 3:
                    lat = float(parts[1])
                    lon = float(parts[2])
                    self.ids.lat_label.text = f"Lat: {lat:.6f}"
                    self.ids.lon_label.text = f"Lon: {lon:.6f}"
                    # Calculate hectares covered (dummy calculation for example)
                    self.total_hectares += 0.01
                    self.db.add_record(lat, lon, self.total_hectares)
                    self.update_grid_colors()
            except Exception as e:
                print(f"Error parsing GPS data: {e}")
        else:
            # No data, set GNSS icon to red
            self.gnss_connected_color = [1, 0, 0, 1]

    # ... rest of the class remains unchanged

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation_mode = False
        self.gnss = GNSSModule(port=None, baudrate=115200, simulation=self.simulation_mode)
        self.db = Database()
        self.total_hectares = 0.0
        self.quadrant_colors = [(1, 1, 1, 1)] * (self.grid_cols * self.grid_rows)  # default white
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS
        self.create_grid()
        self.keyboard = None

    def create_grid(self):
        grid = self.ids.grid
        grid.clear_widgets()
        for i in range(self.grid_cols * self.grid_rows):
            from kivy.uix.button import Button
            btn = Button(background_color=self.quadrant_colors[i])
            btn.bind(on_press=self.on_grid_cell_pressed)
            grid.add_widget(btn)

    def on_grid_cell_pressed(self, instance):
        index = self.ids.grid.children.index(instance)
        print(f"Grid cell {index} pressed")
        # Toggle green color for demonstration
        current_color = instance.background_color
        green = [0, 1, 0, 1]
        white = [1, 1, 1, 1]
        new_color = green if current_color == white else white
        instance.background_color = new_color

    def update(self, dt):
        data = self.gnss.read_data()
        if data:
            # Process data and update UI
            # For example, update quadrant colors based on GPS position
            # Parse latitude and longitude from data (assuming NMEA-like string)
            try:
                parts = data.split(',')
                if len(parts) >= 3:
                    lat = float(parts[1])
                    lon = float(parts[2])
                    # Calculate hectares covered (dummy calculation for example)
                    self.total_hectares += 0.01
                    self.db.add_record(lat, lon, self.total_hectares)
                    self.update_grid_colors()
            except Exception as e:
                print(f"Error parsing GPS data: {e}")

    def update_grid_colors(self):
        # Update quadrant colors based on total hectares and grid size
        green = [0, 1, 0, 1]
        white = [1, 1, 1, 1]
        # Simple logic: color quadrants green based on hectares covered
        num_green = int(self.total_hectares / (self.grid_cols * self.grid_rows) * 10)
        for i in range(self.grid_cols * self.grid_rows):
            color = green if i < num_green else white
            self.quadrant_colors[i] = color
        self.refresh_grid()

    def refresh_grid(self):
        grid = self.ids.grid
        for i, btn in enumerate(grid.children):
            btn.background_color = self.quadrant_colors[i]

    def set_route_a(self):
        print("Route A set")

    def set_route_b(self):
        print("Route B set")

    def show_keyboard(self, instance, value):
        if value:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            if self._keyboard.widget:
                # If it is a widget, this means that it is a virtual keyboard
                pass
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
        else:
            if hasattr(self, '_keyboard'):
                self._keyboard.unbind(on_key_down=self._on_keyboard_down)
                self._keyboard = None

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            self.on_text_entered(self.ids.input_field.text)
            return True
        return False

    def on_text_entered(self, text):
        print(f"Text entered: {text}")
        # Process the entered text here, e.g., update grid size or other parameters
        try:
            value = int(text)
            if value > 0:
                self.grid_cols = value
                self.grid_rows = value
                self.quadrant_colors = [(1, 1, 1, 1)] * (self.grid_cols * self.grid_rows)
                self.create_grid()
        except ValueError:
            print("Invalid input for grid size")
        self.ids.input_field.text = ''

    def toggle_mode(self):
        self.simulation_mode = not self.simulation_mode
        self.gnss.stop()
        self.gnss = GNSSModule(port=None, baudrate=115200, simulation=self.simulation_mode)
        mode = "Simulação" if self.simulation_mode else "Real"
        print(f"Modo alterado para: {mode}")

class GPSApp(App):
    def build(self):
        return GPSWidget()

if __name__ == '__main__':
    GPSApp().run()
