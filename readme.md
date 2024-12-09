# Sensor Data Logger for Vernier Go Direct® Respiration Belt

## Overview

This application is designed to log sensor data from the Vernier Go Direct® Respiration Belt and save it to a CSV file. It supports automatic logging, saving data to a new CSV file every 20 minutes.

## Usage

1. Ensure your computer has all necessary dependencies installed (see below).
2. Turn on the Vernier Go Direct® Respiration Belt.
3. Run the `record_app.py` file and wait for the GUI to start.
4. Click the **Start Recording** button to start logging data and the **Stop Recording** button to stop logging and save data to a CSV file.
5. The application supports auto-recording, saving data every 20 minutes.

## Dependencies

Before running this application, ensure you have the following Python libraries installed:

- `pandas`
- `numpy`
- `pyqtgraph`
- `PySide6`
- `godirect` (for Vernier sensors)

You can install these dependencies using the following command:

```sh
pip install numpy pandas pyqtgraph PySide6 godirect
```

## Support

If you need support or additional code examples, please visit this repository:
[https://github.com/VernierST/godirect-examples](https://github.com/VernierST/godirect-examples)

This should provide clear guidance on how to use the application, its dependencies, and where to seek additional support or examples.
