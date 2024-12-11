## Airflow ETL Pipeline with Postgres and API Integration

This repository demonstrates the creation of an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline integrates with NASA’s Astronomy Picture of the Day (APOD) API to extract data, processes the data, and loads it into a PostgreSQL database. The project leverages Docker to ensure an isolated, reproducible environment for both Airflow and Postgres services.

## Key Components

## 1. Apache Airflow (Orchestration)

Apache Airflow orchestrates the entire ETL pipeline, providing features for defining, scheduling, and monitoring workflows. A Directed Acyclic Graph (DAG) in Airflow outlines the pipeline, ensuring reliable execution of tasks in sequential order.

## Key Features:

Task Dependencies: Automatically manages task execution order.

DAG Workflow: Includes tasks for data extraction, transformation, and loading.

## 2. PostgreSQL Database

The pipeline uses a PostgreSQL database to store the extracted and transformed data. Postgres runs as a Docker container for simplified management and data persistence through Docker volumes.

## Key Features:

Data Storage: Holds the structured data extracted from the API.

Airflow Integration: Interacts with Postgres using Airflow’s PostgresHook and PostgresOperator.

## 3. NASA APOD API

The external data source for this project is NASA’s Astronomy Picture of the Day (APOD) API. This API provides metadata such as the title, explanation, and URL of daily astronomy pictures.

## Key Features:

Data Source: Supplies JSON data about astronomy pictures.

Airflow Integration: The SimpleHttpOperator is used to fetch data from the API.

Objectives

## Extract Data:

Extracts astronomy-related data from the NASA APOD API on a scheduled basis (e.g., daily).

## Transform Data:

Processes the API response to filter relevant fields (e.g., title, explanation, URL, date).

Ensures the data is in the correct format for insertion into the database.

## Load Data into PostgreSQL:

Loads the transformed data into a PostgreSQL table.

Creates the target table automatically if it does not exist.

## Architecture and Workflow

The ETL pipeline is defined using an Airflow DAG with the following stages:

## Extract (E):

Uses the SimpleHttpOperator to perform HTTP GET requests to NASA’s APOD API.

The API response is in JSON format and includes fields such as the title, explanation, and URL of the image.

## Transform (T):

Processes the extracted JSON data using Airflow’s TaskFlow API and the @task decorator.

Extracts and formats relevant fields like title, explanation, url, and date.

## Load (L):

Loads the transformed data into a PostgreSQL table using PostgresHook.

A task in the DAG ensures that the target table exists, creating it if necessary.

## Setup and Installation

Prerequisites

Docker

Docker Compose

Steps

Clone this repository:

git clone <repository-url>
cd <repository-folder>

Start the Docker containers:

docker-compose up

Access the Airflow web interface:

Navigate to http://localhost:8080 in your browser.

Use the default credentials (provided in the docker-compose.yml file) to log in.

Trigger the DAG:

Locate the DAG in the Airflow web interface.

Manually trigger the DAG or wait for the scheduled run.

Directory Structure

.
├── dags/
│   └── nasa_apod_etl.py      # Airflow DAG defining the ETL workflow
├── sql/
│   └── create_table.sql      # SQL script for creating the Postgres table
├── docker-compose.yml        # Docker Compose configuration for Airflow and Postgres
├── requirements.txt          # Python dependencies for Airflow
└── README.md                 # Project documentation

## Future Enhancements

Add more transformations to enhance data quality and usability.

Implement automated alerting for ETL failures.

Expand the pipeline to integrate with additional APIs or data sources.

Add visualization tools (e.g., Tableau or Power BI) for analyzing the stored data.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Apache Airflow for workflow orchestration.

NASA APOD API for providing the data source.

PostgreSQL for data storage and management.
