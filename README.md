# LiMR Teleoperational Robot

Virtual teleoperational robot code for Manchester university 4th year project. Class of 2020, Team 2, LiMR: Blurring the lines between virtual and real worlds.

The aim of this project was to create a virtual environment that will be used by technicians to remotely inspect a HVDC substation.

Other associated repositories can be found under LiMRMainApplication and LiMRInfrastructure.

Python project to act as a virtual robot within a substation. The code can be easily transfered to be a physical robot. Interfaces with the cloud to retrieve and update coordinates. Also contains a machine learning aspect to detect faults on incoming data. All simulated substation data used for training can be found within Isolation_forest_OC_SVM
## To Run
The main robot application, including data uploading and machine learning can be run using:

```
cd src
python3 main.py
```

When running for the first time, it may be necessary to condense the learning data to improve application running times using:
```
python3 condense_data.py
```
The machine learing model can be trained using
```
python3 ml_train.py
```

The URL/Endpoints in some scripts need changing to reflect the correct cloud produced via LiMRInfrastructure.
