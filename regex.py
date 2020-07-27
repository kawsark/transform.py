import os

# Define a dict containing Regular Expressions for different crednetial types
# Step 1. For each mode, create one or more Regex for transform.py. 
# - Each Regex will correspond to a specific field that needs to be encoded.
regex_dict = {
    "azure":['([a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)','client_secret["\s:]+([\w/\+]+)'],
    "aws":['access_key["\s:]+([\w]+)','secret_key["\s:]+([\w/\+]+)'],
    "gcp":[""]
}

# Step 2. spcify one or more transformation names that will be used to encode each field.
# - The order of the transformations must correspond to the order of the fields in regex_dict.
transformation_dict = {
    "azure":["azure","azure-client-secret"],
    "aws":["aws","aws"],
    "gcp":[""]
}

# Step 3. For long fields, indicate the transformations that need to be split into two
split_values = ["aws","azure-client-secret"]


def get_regex(mode):
    return regex_dict[mode]

def get_transformations(mode):
    return transformation_dict[mode]

def get_split_values():
    return split_values