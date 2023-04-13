# Ansible Collection for happyDomain

The collection (`happydns.happydomain`) contains modules to assist in [happyDomain](https://happydomain.org/) deployment and management.


## Ansible version compatibility

The collection is tested and supported with: `ansible >= 2.9`


## Installing the collection

Before using the happyDomain collection, you need to install it using the below command:

```
ansible-galaxy collection install happydns.happydomain
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: happydns.happydomain
```


## Using this collection

### Deploy happyDomain

To setup happyDomain as a local service (support Docker, openrc and systemd), use the role `happydns.happydomain.happydomain`:

```yaml
  roles:
    - name: happydns.happydomain.happydomain
	  use_container: no # yes if you want to use Docker instead
```

### Create a user account on your happyDomain instance

```yaml
  tasks:
    - happydns.happydomain.user:
	  username: frederic@happydomain.org
	  password: "mySuperS3cur3P4$$w0rd"
```

This will create and enabled the user (no need to validate the email).


### Register a NS provider

Eg. for an AXFR/DDNS provider:

```yaml
  tasks:
    - happydns.happydomain.provider:
	  name: test
	  type: DDNSServer
	  data:
	    server: 192.168.0.42
		keyname: ddns
	    algorithm: hmac-sha256
		keyblob: yourBASE64Secret==
	  happydomain_username: frederic@happydomain.org
	  happydomain_password: "mySuperS3cur3P4$$w0rd"
```


### Handle a new domain name in happyDomain

```yaml
  tasks:
    - happydns.happydomain.domain:
	  provider: test
	  domain: happydomain.tf
	  happydomain_username: frederic@happydomain.org
	  happydomain_password: "mySuperS3cur3P4$$w0rd"
```

### Create a new record for a domain

First, you need a zoneid:

```yaml
  tasks:
    - happydns.happydomain.domain:
	  provider: test
	  domain: happydomain.tf
	  happydomain_username: frederic@happydomain.org
	  happydomain_password: "mySuperS3cur3P4$$w0rd"
	register: my_zone
```

Note the `register`ed variable.

Then, use the `happydns.happydomain.service` module:

```yaml
  tasks:
    - happydns.happydomain.service:
	  happydomain_username: frederic@happydomain.org
	  happydomain_password: "mySuperS3cur3P4$$w0rd"
	  domain: happydomain.tf
	  zone: "{{ my_zone.current_zone }}"
	  subdomain: "test"
	  type: abstract.Server
	  service:
        A: 127.0.0.1
		AAAA: "::1"
	  apply_changes: yes
```

This will add two records under `test.happydomain.tf`: A and AAAA (part of `abstract.Server`).


### Remove a given record

You'll also need a zoneid, see previous section. Then:

```yaml
  tasks:
    - happydns.happydomain.service:
	  happydomain_username: frederic@happydomain.org
	  happydomain_password: "mySuperS3cur3P4$$w0rd"
	  domain: happydomain.tf
	  zone: "{{ my_zone.current_zone }}"
	  subdomain: "test"
	  type: scvs.TXT
	  service:
        content: "This is a test record"
	  state: absent
	  apply_changes: yes
```

This will remove all records matching:

```
test IN TXT "This is a test record"
```


## Code of Conduct

This collection follows the Ansible project's [Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html). Please read and familiarize yourself with this doc.


## License

CECILL-2.1
