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
            domain=dict(type='str', aliases=['name']),
            zone=dict(type='str'),
            type=dict(type='str'),
            subdomain=dict(type='str'),
            service=dict(type='dict'),
            erase_others=dict(type='bool'),
            apply_changes=dict(type='bool'),
        )
    )

    p = module.params
    result = {
        "changed": False
    }

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
            for z in d.zone_history:
                if z == p['zone']:
                    zone = d.get_zone(z)

                    if p['subdomain'].removesuffix(d.domain) in zone.services:
                        for s in zone.services[p['subdomain'].removesuffix(d.domain)]:
                            if s._svctype == p['type']:
                                differ = False

                                for k in s.service:
                                    if k not in p['service'] or s.service[k] != p['service'][k]:
                                        differ = True
                                        break

                                if p['erase_others']:
                                    if differ:
                                        s.delete()
                                        result['changed'] = True
                                elif not differ:
                                    if p['state'] == 'absent':
                                        s.delete()
                                        result['changed'] = True
                                    else:
                                        module.exit_json(**result)
                                        return

                    if p['state'] != 'absent':
                        zone.add_zone_service(
                            p['subdomain'].removesuffix(d.domain),
                            p['type'],
                            p['service'],
                        )
                        result['changed'] = True


                    if p['apply_changes']:
                        zone.apply_changes()
                        result['published'] = True
                        result['changed'] = True

                    break
            else:
                module.fail_json(msg="No zone found with id " + p['zone'])
                return
            break
    else:
        module.fail_json(msg="No domain found with name " + p['domain'])
        return

    module.exit_json(**result)


if __name__ == "__main__":
    main()
