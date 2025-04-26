**Data Anonymizer Tool**

**Introduction**
The Data Anonymizer Tool is a Python-based application that provides data anonymization functionalities for sensitive information in CSV files. This tool utilizes different privacy-enhancing techniques to protect sensitive data while maintaining the utility of the original dataset. It supports the following anonymization methods:

Differential Privacy,
Generalization,
Suppression,
Synthetic Data Generation

The application features a user-friendly GUI developed using CustomTkinter for easy interaction with the data.

**Features**

Differential Privacy: Adds noise to numerical columns to preserve privacy.
Generalization: Masks part of the string data with asterisks for anonymization.
Suppression: Replaces rare values in a column with ***.
Synthetic Data Generation: Generates fake data for sensitive string columns using the Faker library.

**GUI:**

Easy-to-use interface to upload data, select anonymization techniques, and save the results.

**Requirements**
To run the project, you will need Python installed along with the required libraries:

pandas,numpy,customtkinter,tkinter,faker


You can install the necessary libraries using the following command:

py -m pip install -r requirements.txt

git clone https://github.com/INeuron9/Data-Anonymizer-Tool.git



Run the main script to launch the application:

Upload a CSV file with sensitive data.

Select an anonymization technique.

Enter parameters like epsilon (privacy level) and k (anonymity level).

View both original and anonymized datasets.

Save the anonymized data to a new CSV file.

Usage
1. Uploading a CSV File
Click on the "📂 Upload CSV" button to upload your dataset (in CSV format).

2. Anonymizing Data
Set the epsilon (privacy level) and k (anonymity threshold) values.

Choose the desired anonymization method from the dropdown:

Generalization: Masks part of string data.

Suppression: Replaces rare values with ***.

Synthetic: Generates fake data for string columns.

Click on "🔒 Anonymize Data" to apply the selected method.

3. Saving Anonymized Data
Click on "💾 Save Anonymized CSV" to save the processed data to a new CSV file.

4. Data Display
The application will display both the original and anonymized data side by side for easy comparison.

A summary section will show the number of records and transformations performed.

Example
Original Data:

Name	Age	Email
John Doe	29	john@example.com
Jane Smith	34	jane@example.com
Sam Brown	45	sam@example.com
Anonymized Data:

Name	Age	Email
John D***	29.14	j***@example.com
Jane S***	34.52	j***@example.com
Sam B***	45.88	s***@example.com
Future Improvements
Additional anonymization techniques for other types of data.

Advanced error handling and validation for user inputs.

Further optimizations for the GUI responsiveness.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
If you have any questions or suggestions, feel free to open an issue on the GitHub repository or contact me directly.

