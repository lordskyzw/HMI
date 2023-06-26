# DP Prediction Application

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
cd dp-prediction


3. Install the required dependencies:
pip install -r requirements.txt


## Usage

1. Prepare the dataset:

- Create an Excel file named 'pretreatment.xlsx' with a sheet named 'Sheet2'.
- Add the following columns to the sheet: 'Turbidity', 'Flow', 'Ferric', and 'DP'.
- Populate the dataset with the corresponding values for each column.

2. Train the neural network model:

- Run the script 'train_model.py' to train the model using the dataset.
- Adjust the model parameters (e.g., number of epochs, batch size) as needed.

3. Run the prediction application:

- Execute the script 'dp_prediction.py' to launch the DP prediction application.
