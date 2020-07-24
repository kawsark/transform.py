import os
import sys
import subprocess
import re
import logging
import json
import argparse
import regex

# Create logger: https://docs.python.org/3/howto/logging.html#configuring-logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
formatter = logging.Formatter('%(levelname)s: %(message)s')
ch.setFormatter(formatter)

# hit counter
hits = 0

# transformation
decode = False
transformation = "azure"
role = "azure-role"

# Prefix
prefix = os.getenv('PREFIX','')

# Encode command
encode_cmd = os.getenv('ENCODE_CMD',"vault write -format=json transform/encode/{0} value={1} transformation={2}")

# Decode command
decode_cmd = os.getenv('DECODE_CMD',"vault write -format=json transform/decode/{0} value={1} transformation={2}")

def main():
    global logger
    global decode
    global transformation
    global role
    
    # Process arguments
    parser = argparse.ArgumentParser(description='Encode or Decode using HashiCorp vault transform secrets engine.')
    parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
    parser.add_argument("-d", "--decode", help="Decodes previously tansformed input", action="store_true")

    # Process transformations
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-az", "--azure", help="Apply transformation for Azure", action="store_true")
    group.add_argument("-aws", "--aws", help="Apply transformation for AWS", action="store_true")
    group.add_argument("-gcp", "--gcp", help="Apply transformation for GCP", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.decode:
        decode = True
        logger.debug("Enabled decode")
        if args.aws:
            print("Sorry AWS decode is not supported yet.")

    # Set transformation
    if args.aws:
        transformation = "aws"
    elif args.gcp:
        transformation = "gcp"
        print("Sorry gcp is not supported yet.")
    else:
        transformation = "azure"
    
    role = transformation + "-role"
    regex_list = regex.get_regex(transformation)

    logger.debug("Using Role: %s and Transformation: %s" % (role,transformation))
    logger.debug("Using Regex: %s" % (regex_list))

    global hits
    input_str = sys.stdin.read()

    for r in regex_list:
        if not decode:
            input_str = re.sub(r,encode_str,input_str,flags=re.DOTALL) # Encode
        else:
            global prefix
            input_str = input_str.replace(prefix,'') # Remove prefix
            input_str = re.sub(r,decode_str,input_str,flags=re.DOTALL) # Decode
    
    logger.debug("Transformed %d times" % hits)        
    print(input_str)

def encode_str(m):
    global logger
    global hits
    global prefix
    global transformation
    global role
    hits += 1

    target = m[1]

    # Create masked value in case vault throws an error
    l = ['#' for i in range(len(target))]
    masked = ''.join(l)

    values = [target]
    results = []

    # Need to split a long string into two parts
    if transformation == "aws" and (len(target) > 25):
        d = int(len(target) / 2)
        values = [target[:d],target[d:]]

    error = False
    for value in values:
        cmd = encode_cmd.format(role,value,transformation)
        logger.debug(encode_cmd.format(role,'{masked}',transformation))

        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            j = json.loads(stdout)
            if "data" in j and "encoded_value" in j["data"]:
                results.append(j["data"]["encoded_value"])
            else:
                error = True
                logger.error('Unexpected output from vault %s' % j)            
        else:
            error = True
            logger.error('Received errors from command %s: %s' % (cmd, stderr))

    if error:
        logger.warning('Defaulting to masking')
        result = masked
    else:
        result = ''.join(results)
        if transformation == "aws":
            x = m[0]
            i = int(len(x)-len(result))
            result = ''.join([x[:i],prefix,result])
        else:
            result = '{}{}'.format(prefix,result)

    return result

def decode_str(m):
    global logger
    global hits
    global transformation
    global role
    hits += 1

    # m.group(0) should contain the value to be decoded
    value = m.group(0)

    cmd = decode_cmd.format(role,value,transformation)
    logger.debug(decode_cmd.format(role,value,transformation))
    
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    error = False;
    
    if process.returncode == 0:
        j = json.loads(stdout)
        if "data" in j and "decoded_value" in j["data"]:
            v = j["data"]["decoded_value"]
        else:
            error = True
            logger.error('Unexpected output from vault %s' % j)            
    else:
        error = True
        logger.error('Received errors from command %s: %s' % (cmd, stderr))

            
    if error:
        logger.warning('Could not decode, returning original string')
        v = value

    return v


if __name__ == '__main__':
    main()
