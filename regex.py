import os

# Define a dict containing Regular Expressions for different crednetial types
regex_dict = {
    "azure":['([a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)'],
    "aws":['access_key["\s:]+([\w]+)','secret_key["\s:]+([\w/\+]+)'],
    "gcp":[""]
}

role_dict = {
    "azure":["azure-role"],
    "aws":["aws-role","aws-role"],
    "gcp":[""]
}

def get_regex(transformation):
    regex = os.getenv('REGEX',None)
    if not regex:
        return regex_dict[transformation]

def get_role_dict():
    return role_dict