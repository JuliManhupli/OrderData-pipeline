# OrderData-pipeline

This project implements an order data processing pipeline using Apache Airflow. 
It generates order data, transfers it between databases, and converts currencies.

## Prerequisites

* Docker and Docker Compose installed on your machine.
* An account on [OpenExchangeRates](https://openexchangerates.org/) and an obtained API key.

## Steps

**1. Clone the Repository**

Open a terminal and navigate to your desired project directory. Then, clone the repository using the following command:

```bash
git clone https://github.com/JuliManhupli/OrderData-pipeline.git
cd OrderData-pipeline
```

**2.Create a virtual environment and install dependencies**

```bash
poetry install
```

**3. Setting Up the Environment File**

1. Navigate to the root directory of your project.
2. Create a new file named `.env`.
3. Inside the `.env` file, paste the necessary environment variables specific to your project. These variables will
   likely be in the `.env.ini` format.

**4. Building Docker Containers**

After setting up the `.env` file, run the following command to build the Docker containers defined in your
`docker-compose.yml` file:

```bash
docker-compose build
```

**5. Starting Docker Containers**

Once the build process completes, run the following command to start the Docker containers in detached mode (meaning the
terminal will not be blocked):

```bash
docker-compose up -d
```

**6. Open the Airflow UI:**

Navigate to the Airflow UI at `http://localhost:8080`.

**7. Enable DAGs**

In the Airflow UI, enable the `generate_orders` and `transfer_and_convert_orders` DAGs.


**8. Stopping Docker Containers**

To stop the Docker containers, run the following command:

```bash
docker-compose down
```
