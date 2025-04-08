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

## Documentation

See the [docs](/docs) directory for Juypter notebooks with complete examples of using the API.

## Basic Usage

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

### Upload anything

```python
from felt_python import upload_file, list_layers

upload = upload_file(
    map_id=map_id,
    file_name="path/to/file.csv",
    layer_name="My new layer",
)
layer_id = upload["layer_id"]
```

## Support
We are always eager to hear from you. Reach out to support@felt.com for all your Felt support needs.
