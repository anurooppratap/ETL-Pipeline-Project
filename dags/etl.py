from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json


### Define the DAG
with DAG( # This is a context manager that creates and initializes a DAG object. All tasks defined within this block are automatically associated with the DAG.
    dag_id = 'nasa_apod_postgres', # This sets the unique identifier for the DAG, which is how Airflow recognizes it.
    start_date = days_ago(1), # sets the start date to one day before the current date.
    schedule_interval = '@daily',
    catchup = False # Determines if Airflow should backfill (run missed DAG runs) for all intervals between the start_date and the current date. False disables backfilling, meaning only the latest scheduled DAG run will execute.
) as dag:

    ### Step 1: Create the table in Postgres if it does not exist
    ### This code snippet defines a Python function create_table() using the TaskFlow API in Apache Airflow. The function is part of a DAG task and is responsible for creating a table in a PostgreSQL database if it does not already exist.
    @task
    def create_table():
        ### initialize the PostgresHook
        postgres_hook = PostgresHook(postgres_conn_id = "my_postgres_connection")

        ### SQL Query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        ### Execute the table creation query
        postgres_hook.run(create_table_query)


    ### Step 2: Extract the NASA API Data - Creating EXTRACT Pipeline
    ### The below code snippet defines a task in Apache Airflow using the SimpleHttpOperator. This operator makes an HTTP request (like a GET request) to an external API (in this case, NASA's Astronomy Picture of the Day API), and the task will be part of a Directed Acyclic Graph (DAG).
    ### SimpleHttpOperator is an Airflow operator that allows you to make HTTP requests to an external API
    extract_apod = SimpleHttpOperator(
        task_id = 'extract_apod', # This is a unique identifier for the task within the DAG
        http_conn_id = 'nasa_api', # http_conn_id refers to the connection set up in the Airflow connections UI that contains the necessary information to make the API request
        endpoint = 'planetary/apod', # The endpoint specifies the path that will be appended to the base URL defined in the nasa_api connection. This indicates that the task will call the Astronomy Picture of the Day (APOD) API endpoint: https://api.nasa.gov/planetary/apod
        method = 'GET', # GET is used to retrieve data from the API (in this case, APOD data)
        data = {"api_key": "{{conn.nasa_api.extra_dejson.api_key}}"},
        # data specifies the payload (body) of the request
        # Here, the payload is a dictionary with the key "api_key", and the value is dynamically retrieved using Airflow’s Jinja templating:
            # {{conn.nasa_api.extra_dejson.api_key}} will pull the API key from the connection's extra field (in JSON format) for the nasa_api connection
            # This API key is needed to authenticate the request to NASA's API
        response_filter = lambda response:response.json(), 
        # response_filter is an optional parameter that allows you to process or modify the API response before it's returned to the next task
        # The response from the API is processed using the response_filter, which parses the response as JSON and returns it as a Python dictionary
    ) 


    ### Step 3: Transform the data - Pick info that we will save
    @task
    def transform_apod_data(response):
        apod_data = {
            'title': response.get('tile', ""),
            'explanation': response.get('explanation',""),
            'url': response.get('url',""),
            'date': response.get('date',""),
            'media_type': response.get('media_type',"")
        }
        return apod_data

    ### Step 4: Loading the data into PostgresSQL
    @task
    def load_data_to_postgres(apod_data):
        ### Initialize the PostgresHook
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')

        ### Define the SQL Insert Query
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """

        ### Execute the SQL Query
        postgres_hook.run(insert_query, parameters = (
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))



    ### Step 5: Verify the data by viewing it through DBViewer



    ### Step 6: Define the task dependencies
    ### Extract
    create_table() >> extract_apod ## Ensure table is created before extraction
    api_response = extract_apod.output
    ### Transform
    transformed_data = transform_apod_data(api_response)
    ### Load
    load_data_to_postgres(transformed_data) 