import json

with open("./env.json") as f:
    config = json.load(f)

statuses = dict(enumerate([
    "STATUS_COMPLIANT",
    "STATUS_NOT_COMPLIANT",
    "STATUS_NOT_APPLICABLE",
    "STATUS_ERROR",
    "STATUS_EXCEPTION"], 1))
