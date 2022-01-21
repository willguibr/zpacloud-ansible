# (Unofficial) Zscaler Private Access (ZPA) Ansible Collection

![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=Ansible+Galaxy&prefix=v&url=https://galaxy.ansible.com/api/v2/collections/willguibr/zpacloud/&query=latest_version.version)

This collection contains modules and plugins to assist in automating the configuration and operational tasks on
Zscaler Private Access cloud, and API interactions with Ansible.

-   Free software: Apache 2.0 License
-   Documentation:
    <https://willguibr.github.io/zpacloud-ansible/>
-   Repo:
    <https://github.com/willguibr/zpacloud-ansible>
-   Example Playbooks:
    <https://github.com/willguibr/zpacloud-playbooks>

Tested Ansible Versions
-----------------------

This collection is tested with the most current Ansible 2.9 and 2.10 releases.  Ansible versions
before 2.9.10 are **not supported**.

Installation
------------

Install this collection using the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install willguibr.zpacloud
```

Usage
-----

Either refer to modules by their full FQCN or use the `collections`
specification in your playbooks:

```yaml
  collections:
    - willguibr.zpacloud

  tasks:
  - name: Get the system info
    panos_op:
      provider: '{{ provider }}'
      cmd: 'show system info'
    register: res

  - debug:
      msg: '{{ res.stdout }}'
```
