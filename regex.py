import os

# Define a dict containing Regular Expressions for different crednetial types
regex_dict = {
    "azure":['([a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)'],
    "aws":['access_key["\s:]+([\w]+)','secret_key["\s:]+([\w/\+]+)'],
    "gcp":[""]
}

def get_regex(transformation):
    regex = os.getenv('REGEX',None)
    if not regex:
        return regex_dict[transformation]
