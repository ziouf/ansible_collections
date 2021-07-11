# Ansible Collection - ziouf.tpm

Manage entries in TeamPasswordManager application

---

## Getting started

1. Setup

You can provide the following information by environment variable or by playbook facts. 

|Env Var|Playbook Fact|Description|
|---|---|---|
|TPM_HOST|tpm_hostname|Hostname of you Team Password Manager instance|
|TPM_USER|tpm_username|For Basic authentication: Username|
|TPM_PASS|tpm_password|For Basic authentication: Password|
|TPM_PUBLIC_KEY|tpm_public_key|For HMAC authentication: API Public key|
|TPM_PRIVATE_KEY|tpm_private_key|For HMAC authentication: API Public key|

2. Create entry

```yaml
- hosts: all
  vars:
    tpm_hostname: teampasswordmanager.com
    tpm_public_key: <public_key>
    tpm_private_key: <private_key>
  tasks:
  - name: Register new credential
    ziouf.tpm.password:
      name: secret-name
      project_name: project-name
      tags: 
        - tag1
        - tag2
      access_info: http://hostname.com
      username: username
      email: username@hostname.com
      password: mySup3rp@$$w0rd
    register: created_secret

  - debug: var=created_secret.tpm
```


3. Retrieve entry

```yaml
# First matching result (tpm query language)
- debug: msg="{{ query('ziouf.tpm.password', 'username:admin tag:tag1,tag2') }}"
- debug: msg="{{ lookup('ziouf.tpm.password', 'username:admin tag:tag1,tag2', field='password') }}"
- debug: msg="{{ query('ziouf.tpm.password', 'username:admin tag:tag1,tag2', field='password') }}"

# All matching results (tpm query language)
- debug: msg="{{ query('ziouf.tpm.password', 'username:admin tag:tag1,tag2', all=True) }}"
- debug: msg="{{ lookup('ziouf.tpm.password', 'username:admin tag:tag1,tag2', all=True, field='password') }}"
- debug: msg="{{ query('ziouf.tpm.password', 'username:admin tag:tag1,tag2', all=True, field='password') }}"

# Get from password's id
- debug: msg="{{ query('ziouf.tpm.password', id=1234) }}"
- debug: msg="{{ lookup('ziouf.tpm.password', id=1234, field='password') }}"

# Generate a new password
- debug: msg="{{ lookup('ziouf.tpm.password', generate=True) }}"
```