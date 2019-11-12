# Osm2Pg

Simple tool for importing OSM data into postGIS

## Requirements

```sudo apt-get install build-essential cmake libboost-dev libexpat1-dev zlib1g-dev libbz2-dev libgeos-c1v5 python3-dev postgresql-server-dev-10```

## Usage

```python3 -m venv venv```
```source venv/bin/activate```
```pip install -r requirements.txt```

```export CONN_STR="dbname=<DB_NAME> user=<USER> password=<PASSWORD> host=<HOST>"```

```python import.py /path/to/osm_file.pbf```
