Ansible Role: happydomain
=========

Ansible Role to deploy happyDomain on Linux hosts.

Requirements
------------

* Ansible >= 2.9
* Docker installed on the remote host
* Cron ready

Role Variables
--------------

All variables which can be overridden are stored in [./defaults/main.yaml](./defaults/main.yaml) file as well as in table below.

| Variable | Default | Description |
| :------ | :------ | :--------- |
| `instance_name` | `happyDomain` | name of this instance |
| `happydomain_version` | `latest` | version of happyDomain to use |
| `happydomain_data_dir` | `/var/lib/happydomain` | Local directory used to store happyDomain data |
| `happydomain_inner_data_dir` | `/data` | Directory used inside the container |
| `happydomain_admin_bind` | `./happydomain.sock` | Bind port/socket for administration interface |
| `happydomain_baseurl` | `` | URL prepended to each URL |
| `happydomain_bind` | `:8081` | Bind port/socket |
| `happydomain_custom_body_html` | `` | Add custom HTML right before `</body>` |
| `happydomain_custom_head_html` | `` | Add custom HTML right before `</head>` |
| `happydomain_default_nameserver` | `127.0.0.1:53` | Adress to the default name server (used for resolutions) |
| `happydomain_external_auth` | `` | Base URL to use for login and registration (use embedded forms if left empty) |
| `happydomain_external_url` | `http://localhost:8081` | Begining of the URL, before the base, that should be used eg. in mails |
| `happydomain_jwt_secret_key` | `` | Secret key used to verify JWT authentication tokens (a random secret is used if undefined) |
| `happydomain_storage_leveldb_path` | `./happydomain.db` | Path to the LevelDB Database |
| `happydomain_mail_from` | `happyDomain <happydomain@localhost>` | Define the sender name and address for all e-mail sent |
| `happydomain_mail_smtp_host` | `` | Use the given SMTP server as default way to send emails |
| `happydomain_mail_smtp_port` | `465` | Define the port to use to send e-mail through SMTP method |
| `happydomain_mail_smtp_username` | `` | If the SMTP server requires authentication, fill with the username to authenticate with |
| `happydomain_mail_smtp_password` | `` | Password associated with the given username for SMTP authentication |
| `happydomain_mail_smtp_tls_no_verify` | `` | Do not verify certificate validity on SMTP connection |
| `happydomain_no_auth` | `false` | Disable user access control, use default account |
| `happydomain_ovh_application_key` | `` | Application Key for using the OVH API |
| `happydomain_ovh_application_secret` | `` | Application Secret for using the OVH API |
| `happydomain_storage_engine` | `leveldb` | Select the storage engine to use |


Example Playbook
----------------

```yaml
---
- hosts: happydomain-host
  roles:
    - name: happydns.happydomain.happydomain
	  happydomain_version: linux-amd64
	  happydomain_no_auth: "true"
	  happydomain_mail_from: "Demo User <demo@localhost>"
	  happydomain_mail_smtp_host: smtp.example.com
```

License
-------

CECILL-2.1
