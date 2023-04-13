# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
'''

from ansible.module_utils.basic import AnsibleModule

from happydomain.admin import Admin

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['absent', 'present']),
            username=dict(type='str', aliases=['name', 'email', 'happydomain_username']),
            password=dict(type='str', aliases=['passwd', 'happydomain_password'], no_log=True),
            allowcommercials=dict(type='bool', default=False),
            email_verified=dict(type='bool', default=True),
            socket=dict(type='path', default='/var/lib/happydomain/happydomain.sock'),
        )
    )

    p = module.params
    changed = False
    found = False

    a = Admin(socket=p['socket'])

    users = a.authuser_list()

    for u in users:
        if u.Email == p['username']:
            found = True

            if p['state'] == 'absent':
                u.Delete()
                changed = True

            else:
                changed = u.ResetPassword(p['password'])

                changedProp = False
                if u.AllowCommercials != p['allowcommercials']:
                    u.AllowCommercials = p['allowcommercials']
                    changedProp = True

                if u.EmailVerification is None and p['email_verified']:
                    now = datetime.now()
                    now = now.replace(microsecond=0)
                    u.EmailVerification = now.isoformat()
                    changedProp = True

                if changedProp:
                    u.Update()
                    changed = True
            break

    if not found and p['state'] != 'absent':
        a.authuser_create(p['username'], p['password'], p['allowcommercials'], p['email_verified'])
        changed = True

    module.exit_json(
        changed=changed,
        msg="user " + p['username'] + ((" created" if not found else " altered") if p['state'] != 'absent' else " deleted"),
    )


if __name__ == "__main__":
    main()
