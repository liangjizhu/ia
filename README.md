# ia

## Project Description

This project is focused on fuzzy logic and risk assessment. It includes several Python scripts and data files that work together to evaluate the risk level of various applications based on input variables such as age, income level, assets, amount, job stability, and credit history.

## Setup Instructions

To set up the project, you need to have Python installed on your system. Additionally, you need to install the following dependencies:

- numpy
- scikit-fuzzy
- matplotlib

You can install these dependencies using pip:

```bash
pip install numpy scikit-fuzzy matplotlib
```

## Running the `main.py` Script

To run the `main.py` script, simply execute the following command in your terminal:

```bash
python main.py
```

This will process the input data files and generate a `Results.txt` file containing the risk assessment results for each application.

## Input Data Files

The project uses the following input data files:

- `InputVarSets.txt`: Contains the definitions of the fuzzy sets for the input variables.
- `Applications.txt`: Contains the data for the applications to be evaluated.
- `Risks.txt`: Contains the definitions of the fuzzy sets for the risk levels.
- `Rules.txt`: Contains the rules for evaluating the risk levels based on the input variables.

## Interpreting the Results

The `main.py` script generates a `Results.txt` file containing the risk assessment results for each application. Each line in the `Results.txt` file corresponds to an application and contains the application ID and the calculated risk level. The risk level is a numerical value that represents the degree of risk associated with the application. Higher values indicate higher risk levels.
