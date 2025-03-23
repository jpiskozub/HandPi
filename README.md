# HandPi: Polish Sign Language Recognition System

## Project Overview
HandPi is a comprehensive system for Polish Sign Language (PSL) recognition that combines custom hardware with machine learning. The project uses a specialized glove equipped with pressure sensors and an Inertial Measurement Unit (IMU) to capture hand gestures, process the data, and interpret Polish Sign Language in real-time.

## System Architecture

### Hardware Components
- **Sensor Glove**: Custom-designed glove with:
  - 10 pressure/flex sensors (2 per finger) connected to ADS1115 ADCs
  - BNO055 IMU for orientation and movement tracking
  - Raspberry Pi as the main processing unit

### Software Components
- **Data Collection Module** (`handpi.py`):
  - Interfaces with hardware sensors through I2C
  - Records and timestamps gesture data
  - Provides self-diagnostics for sensor connections
  - Stores captured data in PostgreSQL database
  - Supports both debugging and examination modes

- **Machine Learning Module** (`handclas.py`):
  - Processes and normalizes collected sensor data
  - Implements a hybrid CNN-GRU neural network architecture
  - Classifies both static and dynamic gestures
  - Achieves high accuracy in recognizing all 36 Polish alphabet signs

## Features
- **Comprehensive Sign Support**: Recognizes all 36 Polish alphabet characters
- **Dual Gesture Types**: Distinguishes between static positions and dynamic movements
- **Multi-modal Sensing**: Combines pressure data with spatial orientation
- **Self-diagnostic Capabilities**: Automatically detects sensor shortcircuits
- **Database Integration**: Stores gesture data with patient metadata
- **MQTT Communication**: Enables remote monitoring and data transfer

## Technical Details

### Data Collection
The system captures:
- ADC readings from 10 pressure points (P1_1 through P5_2)
- Euler angles (orientation in 3D space)
- Linear acceleration (movement dynamics)
- Timestamps for temporal analysis

### Neural Network Architecture
The model uses:
- Convolutional layers for spatial feature extraction
- GRU layers for temporal sequence analysis
- Batch normalization for training stability
- L2 regularization to prevent overfitting

### Dataset
- Samples are organized into 75-point sequences
- Each sample contains 16 features (10 pressure + 6 orientation/acceleration)
- Data is labeled with the corresponding Polish alphabet character

## Usage
1. Run the data collection script (`handpi.py`) on the Raspberry Pi:
   - Option 1: Debug mode for real-time sensor monitoring
   - Option 2: Examination mode for collecting labeled gesture data

2. Train the neural network with collected data using `handclas.py`

3. Deploy the trained model for real-time sign language interpretation

## Installation Requirements
- Raspberry Pi with I2C enabled
- PostgreSQL database
- Python 3.6+
- TensorFlow 2.x
- Required Python packages: adafruit-circuitpython-ads1x15, adafruit-circuitpython-bno055, paho-mqtt, psycopg, pandas, numpy, scikit-learn

## Development Status
The project demonstrates successful recognition of Polish Sign Language characters with promising accuracy. Future work will focus on:
- Real-time translation capabilities
- Expanded vocabulary beyond individual characters
- Mobile application integration
- Personalization for different users
