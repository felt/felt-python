(WIP) The official Python client for the Felt API
===========================================

**felt-python** is a Python client for the Felt API. It provides convenient wrappers for
common operations like creating, deleting and updating maps and data layers.

This client is especially useful at simplifying certain operations like uploading and
refreshing files and (Geo)DataFrames or updating layer styles and element properties.

## Installation

```bash
pip install felt-python
```

## Usage

### Authentication

To authenticate with the Felt API, you need to provide your API token. You can either 
pass it explicitly to function calls or set it in the `FELT_API_TOKEN` environment variable.

```python
import os

os.environ["FELT_API_TOKEN"] = "YOUR_API_TOKEN"
```

### Creating a map

```python
from felt_python import create_map

response = create_map(
    title="My new map",
    lat=40,
    lon=-3,
    public_access="private",
)
map_id = resp["id"]
```

### Uploading a file

```python
from felt_python import upload_file, list_layers

upload = upload_file(
    map_id=map_id,
    file_path="path/to/file.csv",
    layer_name="My new layer",
)
layer_id = upload["layer_id"]
```

### Uploading a Pandas DataFrame
```python
import pandas as pd
from felt_python import upload_dataframe

df = pd.read_csv("path/to/file.csv")
upload_dataframe(
    map_id=map_id,
    dataframe=df,
    layer_name="Felt <3 Pandas",
)
```

### Uploading a GeoPandas GeoDataFrame
```python
import geopandas as gpd
from felt_python import upload_geodataframe

gdf = gpd.read_file("path/to/file.shp")
upload_geodataframe(
    map_id=map_id,
    dataframe=gdf,
    layer_name="Felt <3 GeoPandas",
)
```

### Refreshing a layer
```python
from felt_python import refresh_file_layer

refresh_file_layer(
    map_id=map_id,
    layer_id=layer_id,
    file_path="path/to/new_file.csv",
)
```

### Styling a layer
```python
from felt_python import get_layer_style, update_layer_style

current_style = get_layer_style(
    map_id=map_id,
    layer_id=layer_id,
)
new_style = current_style.copy()
new_style["color"] = "#FF0000"
new_style["size"] = 20
update_layer_style(
    map_id=map_id,
    layer_id=layer_id,
    style=new_style,
)
```
