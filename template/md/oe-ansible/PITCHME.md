---?image=template/img/pencils.jpg
@title[Code Presenting Templates]

## @color[black](Code Presenting<br>Slide Templates)

@fa[arrow-down text-black]

@snap[south docslink span-50]
[The Template Docs](https://gitpitch.com/docs/the-template)
@snapend


+++?code=template/src/go/server.go&lang=golang
@title[Repo Source File]

@[1,3-6](Present code found within any repository source file.)
@[8-18](Without ever leaving your slideshow.)
@[19-28](Using GitPitch code-presenting with (optional) annotations.)

@snap[north-east template-note text-gray]
Code presenting repository source file template.
@snapend


+++?color=lavender
@title[Fenced Code Block]

```javascript
// Include http module.
var http = require("http");

// Create the server. Function passed as parameter
// is called on every request made.
http.createServer(function (request, response) {
  // Attach listener on end event.  This event is
  // called when client sent, awaiting response.
  request.on("end", function () {
    // Write headers to the response.
    // HTTP 200 status, Content-Type text/plain.
    response.writeHead(200, {
      'Content-Type': 'text/plain'
    });
    // Send data and end response.
    response.end('Hello HTTP!');
  });

// Listen on the 8080 port.
}).listen(8080);
```

@[1,2](You can present code inlined within your slide markdown too.)
@[9-17](Your code is displayed using code-syntax highlighting just like your IDE.)
@[19-20](Again, all of this without ever leaving your slideshow.)

@snap[north-east template-note text-gray]
Code presenting fenced code block template.
@snapend


+++?gist=onetapbeyond/494e0fecaf0d6a2aa2acadfb8eb9d6e8&lang=scala&color=black
@title[GitHub GIST]

@[1-6](You can even present code found within any GitHub GIST.)
@[41-53](GIST source code is beautifully rendered on any slide.)
@[57-62](Code-presenting works seamlessly both online and offline.)

@snap[north-east template-note text-white]
Code presenting GitHub GIST template.
@snapend

+++

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

+++?code=template/src/ansible/OHO_dossierdata.yml&lang=yamlex
@title[Standaard ansible template]

@[1-7](Standaard ansible-template)
@[8-9](Maakt users en groepen aan en voegt ssh-keys toe wordt eerst uitgevoerd)
@[5](Zet antwoord-pagina goed voor F5-healthcheck)
@[6-7](Laat server herstarten en nadien notificatie in RocketChat)


+++?color=#36454F
@title[Fenced Text Block]

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
├── fabfile.py
├── fabfile.pyc
├── memo.py
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

@[1-3, 6](Code presenting can also be used to step through any text-based content.)
@[4,5,7,12](Here for example we can navigate through the directory structure for this template.)
@[12-23](We can see that this template uses GitPitch's cool modular markdown support @fa[smile-o fa-spin])

@snap[north-east template-note text-white]
Code presenting fenced text block template.
@snapend

---?code=template/src/fabric/fabfile.py&lang=python
@title[Fabric-bestand voor dossierdata]


