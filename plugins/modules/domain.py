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
            provider=dict(type='str'),
            domain=dict(type='str', aliases=['name']),
            import_zone=dict(type='bool', default=False),
        )
    )

    p = module.params
    result = {
        "changed": False
    }
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

    domains = a.domain_list()

    for d in domains:
        if d.domain == p['domain'] or d.domain == p['domain'] + ".":
            found = True

            if p['state'] == 'absent':
                d.delete()
                result['changed'] = True
                result['msg'] = "domain " + p['domain'] + " deleted"

            elif len(d.zone_history) == 0 and p['import_zone']:
                result['changed'] = True
                result['current_zone'] = d.current_zone.id
                result['msg'] += " and zone imported"
            else:
                result['current_zone'] = d.current_zone
            break

    if not found:
        providers = a.provider_list()
        provider_found = False
        for s in providers:
            if s._comment == p['provider']:
                provider_found = True

                dn = s.domain_add(p['domain'])
                result['msg'] = "domain " + p['domain'] + " added"

                if p['import_zone']:
                    result['current_zone'] = dn.current_zone.id
                    result['msg'] += " and zone imported"

        if not provider_found:
            module.fail_json(msg="No provider found with name " + p['provider'])
            return
        result['changed'] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
