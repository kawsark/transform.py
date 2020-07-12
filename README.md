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

- Use transform.py to transform `az` outputs
```
$ git clone https://github.com/kawsark/transform.py.git && cd transform.py
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

### Usage - decoding example
Pending
