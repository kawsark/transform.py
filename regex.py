import os

# Define a dict containing Regular Expressions for different crednetial types
regex_dict = {
    "azure":['([a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)','client_secret["\s:]+([\w/\+]+)'],
    "aws":['access_key["\s:]+([\w]+)','secret_key["\s:]+([\w/\+]+)'],
    "gcp":[""]
}

transformation_dict = {
    "azure":["azure","azure-client-secret"],
    "aws":["aws","aws"],
    "gcp":[""]
}

# For these transformations, split the value into two
split_values = ["aws","azure-client-secret"]

def get_regex(mode):
    return regex_dict[mode]

def get_transformations(mode):
    return transformation_dict[mode]