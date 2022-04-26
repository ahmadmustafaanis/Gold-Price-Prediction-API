# Forecasting API


## Project Structure
### Data Folder
- Dataset file
### Models
- Saved Trained Models
### src
- Jupyter Notebooks for Vis and Training
### api
- Flask API

## Running the project
- Install Docker and run the following commands
```bash
$ git clone github.com/ahmadmustafaanis/forecastingapi
$ cd ForecastingAPI
$ sudo docker build -f Dockerfile -t gold_price_api:api .
$ sudo docker run -p 5000:5000 -d gold_price_api:api
```