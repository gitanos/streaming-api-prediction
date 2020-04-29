# Streaming Api for Prediction

Template project to ingest streaming data and deliver predictions through an API.

## Setup

Create a directory (if not there already) named './patient_data/' within the project.
Add files age.csv, admission.csv, signal.csv to that repo in order to run the tool.

## Installation

First, make sure you have docker-compose installed on your machine
Then, build all containers with:

```
docker-compose build
```


### Running

Run it with:

```
docker-compose up
```

### Finding your way around... 

The project is built on a microservice-based architecture. 
Each Docker container has a specific function. 
You can find a scheme of the project below. 

The project includes the following elements:

- Stream (hospital)
- Import of stream (buffer)
- Tool 
- Database
- Model API

The buffer module is responsible for calling the stream and consuming it. 
Each message is submitted to a Redis queue. This is picked up by the Tool that 
stores the retrieved data into a Mysql database and evaluates whether a patient
is still in ICU. If that's the case, then the tool makes an API request to 
the model API and get a prediction on the state of the patient. 


### Output

In the terminal where you run the previous command you will start seeing logs from the project.

Here you can find the messages retrieved from the stream and submitted to Redis. 
Then, data is stored in a Database. You could always `exec` into the mysql container
to check that data is stored correctly. 

The API containing the model is only called if a patient is currently in ICU. 
As these data are at the bottom of the .csv file, it might take a while before you 
get a prediction per patient. I would recommend that in the initial .csv files
 you keep only data without a `discharge_date` so you can immediately see the
 results of the prediction. 

## Structure
```bash
.
├── buffer
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
├── hospital
│   ├── Dockerfile
│   ├── preprocessing.py
│   ├── requirements.txt
│   └── streamer_aiohttp.py
├── modelapi
│   ├── api_errors.py
│   ├── app.ini
│   ├── Dockerfile
│   ├── endpoints.py
│   ├── requirements.txt
│   ├── server.py
│   └── wsgi.py
├── nginx
│   ├── app.conf
│   └── Dockerfile
├── patient_data
│   ├── admission.csv
│   ├── age.csv
│   ├── all_data.csv    ** gets created
│   └── signal.csv
├── README.md
└── tool
    ├── database
    │   ├── Dockerfile
    │   └── init.sql
    ├── data_handler.py
    ├── db_connector.py
    ├── Dockerfile
    ├── requirements.txt
    ├── run.py
    └── worker.py
```

### Problems?

Get it touch with me and I will try to help you out. 
