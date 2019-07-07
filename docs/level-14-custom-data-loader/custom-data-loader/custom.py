import csv

from moban import constants
from lml.plugin import PluginInfo


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["custom"])
def open_custom(file_name):
    with open(file_name, "r") as data_csv:
        csvreader = csv.reader(data_csv)
        rows = []
        for row in csvreader:
            rows.append(row)

        data = dict(zip(rows[0], rows[1]))
        return data
