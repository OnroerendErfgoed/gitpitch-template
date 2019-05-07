---
@title[Code Presenting Templates]

@snap[north]
### Folderstructuur Ansible
@snapend

@snap[south]
```text
ansible
├── ansible.cfg
├── docs
│   └── source
├── group_vars
│   ├── all.yml
│   └── playground.yml
├── installatie
│   ├── OHO_actoren.yml
│   ├── ...
│   ├── OHO_dossierdata.yml
│   ├── ...
│   ├── OHO_verwerkingsdiensten.yml
│   ├── files
│   │   ├── AtoM
│   │   ├── ansible_versie.sh
│   │   ├── apc.php
│   │   ├── httpd.conf
│   │   ├── info.php
│   │   ├── nginx.conf
│   │   ├── status
│   │   └── vim-bestanden.tar.gz
│   ├── handlers
│   │   ├── OHO_restart_squid.yml
│   │   ├── restart_apache.yaml
│   │   ├── restart_memcached.yaml
│   │   └── restart_nginx.yaml
│   ├── tasks
│   │   ├── OHO_AtoM_packages.yml
│   │   ├── OHO_config_status.yml
│   │   ├── OHO_drupal_packages.yml
│   │   ├── OHO_ee_packages.yml
│   │   ├── OHO_fwp_config.yml
│   │   ├── OHO_fwp_packages.yml
│   │   ├── OHO_notificatie.yml
│   │   ├── OHO_reboot.yml
│   │   ├── OHO_rest_packages.yml
│   │   ├── OHO_user_basis.yml
│   │   ├── OHO_user_export.yml
│   │   └── ...
│   └── templates
│       ├── AtoM
│       ├── OHO_http_proxy.sh.j2
│       ├── OHO_pip.conf.j2
│       ├── OHO_squid.conf.j2
│       ├── nginx_vHost.j2
│       ├── pip_conf.j2
│       ├── ports_conf.j2
│       └── vHost.j2
├── monitoring
│   ├── OHO_iptables.yml
│   ├── OHO_verbindingen.yml
│   └── tasks
│       ├── OHO_fwp.yml
│       ├── OHO_mail.yml
│       ├── OHO_msb.yml
│       ├── OHO_postgres.yml
│       ├── OHO_vioe-pypi.yml
│       └── ...
├── oe_hosts.ini
└── roles
    ├── apache
    ├── basis
    ├── nginx
    ├── users
    ├── users_and_groups
    └── users_db
```
@[1-3, 6](Structuur van ansible)
@[4](Template van dossierdata)
@[6-19,25](Bestanden nodig door ansbile om dossierdata aan te maken)
@snapend

---
@title[Ansible-bestand - dossierdata]

@snap[north span 40]
### Ansible-bestand van dossierdata
@snapend

```yamlex
- include: tasks/controle_ansible.yaml

- hosts: dossierdata
  remote_user: root

  tasks:
  - include: tasks/OHO_user_export.yml 
  - include: tasks/OHO_user_basis.yml
  - include: tasks/OHO_config_status.yml
  - include: tasks/OHO_reboot.yml
  - include: tasks/OHO_notificatie.yml

  roles:
   - { role: users }
```
@title[Standaard ansible template]

@[13-14](Maakt users en groepen aan en voegt ssh-keys toe wordt eerst uitgevoerd)
@[9](Zet antwoord-pagina goed voor F5-healthcheck)
@[10-11](Laat server herstarten en nadien notificatie in RocketChat)




