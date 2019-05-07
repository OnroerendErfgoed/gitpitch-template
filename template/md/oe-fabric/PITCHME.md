---?code=template/src/fabric/fabfile.py&lang=python
@title[Fabric-bestand voor dossierdata]

---
```text
.
├── ansible
...
├── dossierdata
│   ├── config
│   │   ├── dossierdata.nginx
│   │   ├── nginx.nginx
│   │   ├── process_mapping-dev.yml
│   │   ├── process_mapping-pr.yml
│   │   ├── process_mapping-test.yml
│   │   ├── processen-dev.json
│   │   ├── processen-pr.json
│   │   ├── processen-test.json
│   │   ├── redis.conf
│   │   ├── regioverantwoordelijken
│   │   ├── schema.nginx
│   │   ├── status.nginx
│   │   ├── supervisor_dossierdata.conf
│   │   └── werkgebieden
│   ├── fabfile.py
│   ├── memo.py
│   ├── schemas
│   │   ├── 1
│   │   ├── 2
│   │   ├── 4
│   │   ├── 5
│   │   ├── 6
│   │   ├── 7
│   │   ├── common
│   │   └── schema.json
│   └── scripts
│       ├── gebruikers-dev.ldif
│       ├── gebruikers-prod.ldif
│       ├── gebruikers-test.ldif
│       ├── rollen.ldif
│       ├── rollen_clear.ldif
│       ├── rqworker
│       ├── rqworker.sh
│       └── systeemgebruikers.ldif
...
```