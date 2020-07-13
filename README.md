# transform.py
A wrapper for the HashiCorp Vault transform secrets engine

This repository is a wrapper around the [Vault Transform Secrets Engine](https://www.vaultproject.io/docs/secrets/transform) to transform sensitive values such as credentials or account IDs when performing demos. Below is an example for Azure. All the values prefixed with `vault:fpe:` have been transformed using Vault Format Preserving Encryption ([blog post](https://medium.com/hashicorp-engineering/advanced-data-protection-with-hashicorp-vault-96839b6b22af)).
```
$ az account list | python3 transform.py -v -t
 {
    "cloudName": "AzureCloud",
    "homeTenantId": "vault:fpe:jkqyhelg-1j6p-b1aw-lqru-x04xd45f69q3",
    "id": "vault:fpe:7tjtckfw-81vt-qtmm-lv48-ibu7hh7serls",
    "isDefault": true,
    "managedByTenants": [
      {
        "tenantId": "vault:fpe:605nu3wm-xyzb-s8jy-rdby-g2dkmu0lwfob"
      },
      {
        "tenantId": "vault:fpe:ee28kq6g-hul9-42jj-4974-vbiwd8oyc56v"
      }
    ],
    "name": "Team Engineers",
    "state": "Enabled",
    "tenantId": "vault:fpe:jkqyhelg-1j6p-b1aw-lqru-x04xd45f69q3",
    "user": {
      "name": "user@company.com",
      "type": "user"
    }
  }
```

### Usage - encoding example
- Please download and unzip a Vault binary with minimum version 1.4 with the `+ent` suffix. These are available for download at [releases page](https://releases.hashicorp.com/vault/). Start the Vault server in dev mode on one terminal.
```
vault server -dev
```


- Setup the transform secrets engine. Note: this will transform sensitive IDs output from the `az` CLI tool and Vault's Azure dynamic secrets engine.
```
# Secret engine
vault secrets enable transform

# Create template
vault write transform/template/azure_template type=regex \
        pattern="([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)" \
        alphabet=builtin/alphanumericlower

# Create transformation
vault write transform/transformation/azure \
        type=fpe \
        template=azure_template \
        tweak_source=internal \
        allowed_roles='azure_role'

# Create role
vault write transform/role/azure_role transformations=azure
```

- Use transform.py to transform `az` outputs. 
```
$ git clone https://github.com/kawsark/transform.py.git && cd transform.py
$ az account list | python3 transform.py -t
 {
    "cloudName": "AzureCloud",
    "homeTenantId": "vault:fpe:jkqyhelg-1j6p-b1aw-lqru-x04xd45f69q3",
    "id": "vault:fpe:7tjtckfw-81vt-qtmm-lv48-ibu7hh7serls",
    "isDefault": true,
    "managedByTenants": [
      {
        "tenantId": "vault:fpe:605nu3wm-xyzb-s8jy-rdby-g2dkmu0lwfob"
      },
      {
        "tenantId": "vault:fpe:ee28kq6g-hul9-42jj-4974-vbiwd8oyc56v"
      }
    ],
    "name": "Team Engineers",
    "state": "Enabled",
    "tenantId": "vault:fpe:jkqyhelg-1j6p-b1aw-lqru-x04xd45f69q3",
    "user": {
      "name": "user@company.com",
      "type": "user"
    }
  }
... <remaining output omitted>
```

### Usage - decoding example
To decode a previously encoded outputs, please save the encoded output above into a file (E.g. az.txt). then run the same process with the `-d` parameter as shown below.
```
$ az account list | python3 transform.py -t > az.txt
$ cat az.txt | python3 transform.py -d
... <output omitted>
```

### Verbose mode
The `-v` parameter can be used to enable verbose mode and show the underlying vault commands, as well as indicate how many times an encoding or decoding operation took place:
```
$ az account list | python3 transform.py -v -t
DEBUG: Enabled transform
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: vault write -format=json transform/encode/local value={masked} transformation=azure
DEBUG: Encoded 18 times
...<remaining output omitted>

$ cat az.txt | python3 transform.py -d -v
DEBUG: Enabled decode
DEBUG: vault write -format=json transform/decode/local value=t1mwirk8-g9pv-tm6v-c9fz-vqar3c2ucvzn transformation=azure
DEBUG: vault write -format=json transform/decode/local value=14fh6g3q-jtso-ebd2-01oh-1a1xm9phb8jp transformation=azure
DEBUG: vault write -format=json transform/decode/local value=kyal0fgl-zbpl-avqj-yw98-gvtb494ntfb3 transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=7f1j1gop-ymav-c6i8-untu-vk2w8hvek6df transformation=azure
DEBUG: vault write -format=json transform/decode/local value=m7qemial-wm8r-jcy2-6xqc-vbvile14cpck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=pntypy5w-m6xi-g2a3-y7i7-lfdurgooworq transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=8a4kij3a-jvcx-vin6-pbm0-ho9gexwdv6qg transformation=azure
DEBUG: vault write -format=json transform/decode/local value=m7qemial-wm8r-jcy2-6xqc-vbvile14cpck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=sfy66yab-0zcm-5ro5-d779-ujmq3y27hdnj transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: vault write -format=json transform/decode/local value=go3wazrl-c7ql-13pd-5ech-hnydcy5ldemp transformation=azure
DEBUG: vault write -format=json transform/decode/local value=yu6m6hww-cvzi-vdfm-x73p-u2zhqjfkq3ck transformation=azure
DEBUG: Decoded 18 times
...<remaining output omitted>
```
