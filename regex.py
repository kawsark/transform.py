# Define a dict containing Regular Expressions for different credential types

# Step 1. For each mode, create one or more Regex for transform.py.
# - Each Regex will correspond to a specific field that needs to be encoded.
regex_dict = {
    "azure": [r'([a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)', r'client_secret["\s:]+([\w/\+]+)'],
    "aws": [r'access_key["\s:]+([\w]+)', r'secret_key["\s:]+([\w/\+]+)'],
    "gcp": [""]
}

# Step 2. specify one or more transformation names that will be used to encode each field.
# - The order of the transformations must correspond to the order of the fields in regex_dict.
transformation_dict = {
    "azure": ["azure", "azure-client-secret"],
    "aws": ["aws", "aws"],
    "gcp": [""]
}

# Step 3. For long fields, indicate the transformations that need to be split into two
split_values_list = ["aws", "azure-client-secret"]
