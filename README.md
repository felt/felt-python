# The official Python client for the Felt API

[![PyPI][pypi_badge]][pypi_link]
[![Binder][binder_badge]][binder_jupyterlab_url]
[![open_in_colab][colab_badge]][colab_notebook_link]

[pypi_badge]: https://badge.fury.io/py/felt-python.svg
[pypi_link]: https://pypi.org/project/felt-python/
[binder_badge]: https://mybinder.org/badge_logo.svg
[binder_jupyterlab_url]: https://mybinder.org/v2/gh/felt/felt-python/HEAD
[colab_badge]: https://colab.research.google.com/assets/colab-badge.svg
[colab_notebook_link]: https://colab.research.google.com/github/felt/felt-python/blob/main

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
Use [the Felt dashboard](https://felt.com/maps/latest/integrations) to create a new token.

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
map_id = response["id"]
```

### Uploading a file

```python
from felt_python import upload_file, list_layers

upload = upload_file(
    map_id=map_id,
    file_name="path/to/file.csv",
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
    geodataframe=gdf,
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
from felt_python import get_layer_details, update_layer_style

current_style = get_layer_details(
    map_id=map_id,
    layer_id=layer_id,
)["style"]
new_style = current_style.copy()
new_style["color"] = "#FF0000"
new_style["size"] = 20
update_layer_style(
    map_id=map_id,
    layer_id=layer_id,
    style=new_style,
)
```

## Support
We are always eager to hear from you. Reach out to support@felt.com for all your Felt support needs.
