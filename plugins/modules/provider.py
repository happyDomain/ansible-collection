# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
'''

from ansible.module_utils.basic import AnsibleModule

from happydomain.api import HappyDomain

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['absent', 'present']),
            happydomain_username=dict(type='str', aliases=['email']),
            happydomain_password=dict(type='str', aliases=['passwd'], no_log=True),
            happydomain_token=dict(type='str'),
            happydomain_scheme=dict(type='str', default='http'),
            happydomain_host=dict(type='str', default='localhost'),
            happydomain_port=dict(type='int', default='8081'),
            happydomain_baseurl=dict(type='str', default=''),
            type=dict(type='str'),
            name=dict(type='str', aliases=['comment']),
            data=dict(type='dict'),
        )
    )

    p = module.params
    changed = False
    found = False

    a = HappyDomain(
        scheme=p['happydomain_scheme'],
        host=p['happydomain_host'],
        port=p['happydomain_port'],
        baseurl=p['happydomain_baseurl'],
        token=p['happydomain_token'],
    )

    if p['happydomain_password'] is not None:
        a.login(p['happydomain_username'], p['happydomain_password'])

    providers = a.provider_list()

    for s in providers:
        if s._srctype == p['type'] and s._comment == p['name']:
            s = a.provider_get(s._id)
            found = True

            if p['state'] == 'absent':
                s.delete()
                changed = True

            else:
                for k in p['data']:
                    if k not in s.args or p['data'][k] != s.args[k]:
                        s.args = p['data']
                        changed = True
                        break

                if changed:
                    s.update()
            break

    if not found and p['state'] != 'absent':
        a.provider_add(p['type'], p['name'], p['data'])
        changed = True

    module.exit_json(
        changed=changed,
        msg="provider " + p['name'] + ((" created" if not found else " altered") if p['state'] != 'absent' else " deleted"),
    )


if __name__ == "__main__":
    main()
