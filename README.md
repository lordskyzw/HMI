# HUMAN MACHINE INTERFACE

This is a Python application that predicts the DP (Differential Pressure) value based on the values of Flow and Ferric. The application utilizes a trained neural network model and provides a graphical representation of the DP values over time.

## Requirements

- Python 3.x
- pandas
- scikit-learn
- TensorFlow
- matplotlib
- tkinter

## Installation

1. Clone the repository to your local machine:
git clone https://github.com/lordskyzw/hmi.git


2. Navigate to the project directory:
cd hmi


3. Install the required dependencies:
pip install -r requirements.txt


## Usage


1. Train the neural network model:

- Run all the cells in the `modelbuilding` notebooks to train the model using the dataset.
- Adjust the model parameters (e.g., number of epochs, batch size) as needed.

2. Run the prediction application:

- Execute the script 'hmi.py' to launch the DP prediction application.
