# views.py
from flask import abort, jsonify, render_template, request, redirect, url_for, make_response, send_file
import uuid

from app import app
from werkzeug.utils import secure_filename
import os
import glob
import json
import requests
import pandas as pd
from plotnine import *
import requests
import requests_cache
requests_cache.install_cache('/output/demo_cache')

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '{"status" : "up"}'

@app.route('/plot/simplebox', methods=['GET'])
def simplebox():
    task = request.values.get("task")
    metadata_column = request.values.get("metadata_column")
    variable_value = int(request.values.get("variable_value"))

    url = "https://proteomics3.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&file=feature_statistics/data_long.csv".format(task)
    r = requests.get(url)
    r.raise_for_status()
    local_filename = os.path.join("/output", task + ".tsv")
    with open(local_filename, "w") as output_file:
        output_file.write(r.text)
    long_data_df = pd.read_csv(local_filename)

    # Filtering the data
    if "metadata_conditions" in request.values:
        metadata_conditions = request.values["metadata_conditions"].split(";")
        long_data_df = long_data_df[long_data_df[metadata_column].isin(metadata_conditions)]

    long_data_df = long_data_df[long_data_df["variable"] == variable_value]
    p = (
        ggplot(long_data_df)
        + geom_boxplot(aes(x="factor({})".format(metadata_column), y="value", fill=metadata_column))
    )

    if "metadata_facet" in request.values:
        p = p + facet_wrap(facets=request.values["metadata_facet"])

    output_filename = "temp.png"
    p.save(output_filename)

    return send_file(output_filename)