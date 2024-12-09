"""
Disclaimer: This software is provided "as is", without warranty of any kind, express or implied, 
including but not limited to the warranties of merchantability, fitness for a particular purpose, 
and noninfringement. In no event shall the authors or copyright holders be liable for any claim, 
damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, 
out of, or in connection with the software or the use or other dealings in the software.

Use this software at your own risk. The authors do not take any responsibility for any harm that 
may come from the use of this software. Ensure that the sensor connections and configurations 
are appropriate for your specific use case.
"""

import sys
import pandas as pd
from datetime import datetime
import pyqtgraph as pg
from gdx import gdx
from PySide6.QtCore import QTimer
import time
import os
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
)

# Initialize the sensor
gdx = gdx.gdx()
gdx.open(connection="ble", device_to_open="GDX-RB 0K2035X5")
gdx.select_sensors([1, 2])


class SensorApp(QMainWindow):
    AUTO_EXPORT_INTERVAL_MINUTES = 20
    READ_INTERVAL_SECONDS = 0.1

    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()  # Timer for periodic data updates
        self.timer.timeout.connect(
            self.update_data
        )  # Connect timer to data update method
        self.start_time = None  # Variable to store the start time of recording

        # Create ndarray to store time, force, breath rate data, and timestamp
        self.data_array = np.empty((0, 4))  # Initialize an empty ndarray

    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle("Sensor Data Logger")

        # Create central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create plot widget for displaying data
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Create start recording button
        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.start_button)

        # Create stop recording button
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.layout.addWidget(self.stop_button)

        # Add legend to the plot
        self.plot_widget.addLegend()
        self.force_plot = self.plot_widget.plot(pen="b", name="Force (N)")
        self.breath_plot = self.plot_widget.plot(pen="r", name="Respiration Rate (bpm)")

    def start_recording(self):
        """Start recording sensor data."""
        gdx.start(
            self.READ_INTERVAL_SECONDS * 1000
        )  # Start the sensor with specified period
        self.start_time = time.time()  # Record the start time
        self.timer.start()  # Start the timer
        self.data_array = np.empty((0, 4))  # Reset the ndarray

        # Clear the plots
        self.force_plot.clear()
        self.breath_plot.clear()

    def stop_recording(self):
        """Stop recording sensor data."""
        self.timer.stop()  # Stop the timer
        gdx.stop()  # Stop the sensor
        self.save_data_to_csv()  # Save recorded data to CSV file

    def update_data(self):
        """Update sensor data."""
        measurements = gdx.read()  # Read data from the sensor
        if measurements is None:
            return  # If no data is read, return early

        current_time = time.time() - self.start_time  # Calculate elapsed time
        timestamp = round(time.time(), 4)  # Get current timestamp

        # Append new data to the ndarray
        new_data = np.array([[current_time, measurements[0], measurements[1], timestamp]])
        self.data_array = np.vstack([self.data_array, new_data])

        # Filter out NaN values for plotting
        filtered_time_data = self.data_array[~np.isnan(self.data_array[:, 2]), 0]
        filtered_breath_data = self.data_array[~np.isnan(self.data_array[:, 2]), 2]

        # Update the plots with the new data
        self.force_plot.setData(self.data_array[:, 0], self.data_array[:, 1])
        self.breath_plot.setData(filtered_time_data, filtered_breath_data)

        # Auto save data to CSV
        if (
            len(self.data_array)
            >= self.AUTO_EXPORT_INTERVAL_MINUTES * 60 / self.READ_INTERVAL_SECONDS
        ):
            self.save_data_to_csv()

    def save_data_to_csv(self):
        """Save the recorded data to a CSV file."""
        df = pd.DataFrame(
            self.data_array, columns=["Time", "Force_N", "Respiration_Rate_bpm", "Timestamp"]
        )
        os.makedirs("Data", exist_ok=True)  # Create Data directory if it doesn't exist
        filename = os.path.join(
            "Data", datetime.now().strftime("%Y%m%d_%H%M%S") + "_gt.csv"
        )
        df.to_csv(filename, index=False)  # Save the DataFrame to a CSV file
        self.data_array = np.empty((0, 4))  # Clear the data array after saving

    def closeEvent(self, event):
        """Handle the window close event to ensure the sensor is properly closed."""
        self.timer.stop()  # Stop the timer
        gdx.stop()  # Stop the sensor
        gdx.close()  # Close the sensor connection
        super().closeEvent(event)  # Call the parent class's closeEvent method


def main():
    """Main function to start the application."""
    app = QApplication(sys.argv)
    ex = SensorApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
