import os
import sys

from fabric.api import *

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from oe_fabric.tasks import (
    create_virtualenv,
    create_virtualenv_if_not_exists,
    install_js_utilities,
    install_nginx,
    install_redis,
    ldap_build,
    ldap_rechten,
    ldap_setup,
    ldap_systeemgebruikers,
    redis_flush_cache,
    update_redis_config,
    supervisor_restart,
    create_log_folder,
    create_projects_folder,
    create_db,
    drop_db,
    initialize_db,
    db_rechten_init,
    restore_db,
    db_rechten_update,
    check_barman,
    initialize_barman,
    _redeploy_config
)
from oe_fabric.variables import (
    dev_general_vars,
    test_general_vars,
    prod_general_vars
)
from oe_fabric.utils import (
    copy_and_replace,
    install_virtual_env_libs,
    virtualenv,
    get_secret_setting,
    env_invullen,
    create_build_config_dir,
    get_project_versions,
    save_version_history,
    run_with_proxy,
    get_ip,
    install_gunicorn,
    install_requirements
)

env.use_v_config = False
env.applicatie_naam = 'dossiers'
env.applicatie_id = 'vioe-dossiers'
env.dossier_proj_dir = '/var/projects/dossierdata'
env.schema_proj_dir = '/var/projects/schemas'
env.venv_dir = '/var/projects/dossierdata/venv'
env.code_dir = './dossierdata'
env.activate = 'source /var/projects/dossierdata/venv/bin/activate' 
env.proj_dir = '/var/projects/dossierdata'
env.crabpy_root = '/var/projects/dogpile_data'
env.gunicorn_port = '8080'
env.gunicorn_workers = '2'
env.gunicorn_threads = '1'

env.ip_config = {
    'vioe-dossierdata-dev-1.vm.cumuli.be': {
        'nginx_pr_interface': get_ip('vioe-dossierdata-dev-1.vm.cumuli.be'),
        'redis_host': get_ip('vioe-dossierdata-dev-1.vm.cumuli.be')
    },
    'vioe-dossierdata-test-1.vm.cumuli.be': {
        'nginx_pr_interface': get_ip('vioe-dossierdata-test-1.vm.cumuli.be'),
        'redis_host': get_ip('vioe-dossierdata-test-1.vm.cumuli.be')
    },
    'vioe-dossierdata-prod-1.vm.cumuli.be': {
        'nginx_pr_interface': get_ip('vioe-dossierdata-prod-1.vm.cumuli.be'),
        'redis_host': get_ip('vioe-dossierdata-prod-1.vm.cumuli.be')
    }
}


@task
def update_ubuntu():
    '''
    Make sure all needed libraries are present in Ubuntu.
    '''
    with settings(user='root'):
        run_with_proxy('apt-get update')
        install_virtual_env_libs()
        run_with_proxy('apt-get -y install libxslt1-dev')
        run_with_proxy('apt-get -y install libxml2-dev')
        run_with_proxy('apt-get -y install git')
        run_with_proxy('apt-get -y install supervisor')
        # run_with_proxy('apt-get install python-dev libpq-dev')
        run_with_proxy('apt-get -y install python-dev')
        run_with_proxy('apt-get -y install libpq-dev')
        run_with_proxy('apt-get -y install libffi-dev')
        run_with_proxy('apt-get -y install build-essential')
        run_with_proxy('apt-get -y install libssl-dev')
        run_with_proxy("cd /tmp && export http_proxy='%s'&&export https_proxy='%s'&&wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2 && tar -xvf geos-3.4.2.tar.bz2" % (env.server_http_proxy, env.server_http_proxy))
        run_with_proxy("cd /tmp/geos-3.4.2 && ./configure && make && make install")
        run_with_proxy("ldconfig")
        install_redis()
        install_nginx()


def multi_env_settings():
    env.applicatie_folder = 'dossierdata'  # override global env.applicatie_folder

    env.dossier_nginx_server_name = env_invullen('{environment}dossiers.onroerenderfgoed.be')
    env.schema_nginx_server_name = env_invullen('{environment}schemas.onroerenderfgoed.be')

    # OAuth instellingen
    env.oeauth_consumer_key = 'vioe-dossiers'
    env.oeauth_consumer_secret = get_secret_setting(env.omgeving, 'dossiers', 'oeauth_consumer_secret')
    env.oeauth_callback = env_invullen('https://{environment}dossiers.onroerenderfgoed.be/oauth')
    env.session_factory_secret = get_secret_setting(env.omgeving, 'dossiers', 'session_factory_secret')

    env.storageprovider_collection = 'dossiers'
    env.es_index = 'dossiers'
    env.process_mapping = '%s/process_mapping.yml' % env.dossier_proj_dir

    env.db_prefix = 'dossierdata'
    env.db_admin_pwd = get_secret_setting(env.omgeving, env.applicatie_naam, '{0}_dba'.format(env.db_prefix))
    env.db_admin_user = '{0}_dba'.format(env.db_prefix)
    env.db_admin_url = 'vioe-dossierdata-postgres-{0}-1.vm.cumuli.be:5432'.format(env.omgeving_uitgebreid)
    env.db_url = 'vioe-dossierdata-postgres-{0}-1.vm.cumuli.be:5432'.format(env.omgeving_uitgebreid)
    env.db_name = '{0}_{1}'.format(env.db_prefix, env.omgeving_uitgebreid)
    env.db_pwd = get_secret_setting(env.omgeving, env.applicatie_naam, '{0}'.format(env.db_prefix))
    env.db_user = '{0}'.format(env.db_prefix)

    env.uri_root = env_invullen('https://{environment}id.erfgoed.net')
    env.uri_rewrite = env_invullen('https:/{environment}id.erfgoed.net/processen')
    env.dossiers_uri = env_invullen(
        'https://{environment}id.erfgoed.net/dossiers/{placeholder0}', '{0}')
    env.process_mapping_source = 'process_mapping-{0}.yml'.format(env.omgeving)
    env.regioverantwoordelijken = '{0}'.format(env.omgeving)
    env.processen = 'processen-{0}.json'.format(env.omgeving)
    env.alembic_location = 'dossierdata/alembic'


@task
def barman_dev():
    env.hosts = ['']
    dev_general_vars()
    multi_env_settings()
    env.hosts = [env.barman_host]


@task
def dev_db():
    env.hosts = ['vioe-dossierdata-postgres-dev-1.vm.cumuli.be']
    dev_general_vars()
    multi_env_settings()


@task
def barman_test():
    env.hosts = ['']
    test_general_vars()
    multi_env_settings()
    env.hosts = [env.barman_host]


@task
def test_db():
    env.hosts = ['vioe-dossierdata-postgres-test-1.vm.cumuli.be']
    test_general_vars()
    multi_env_settings()


@task
def barman_prod():
    env.hosts = ['']
    prod_general_vars()
    multi_env_settings()
    env.hosts = [env.barman_host]


@task
def prod_db():
    env.hosts = ['vioe-dossierdata-postgres-prod-1.vm.cumuli.be']
    prod_general_vars()
    multi_env_settings()


@task
def dev():
    env.hosts = ['vioe-dossierdata-dev-1.vm.cumuli.be']
    dev_general_vars()
    multi_env_settings()
    env.server_no_proxy = 'localhost,msb-vioe-dev.lb.cumuli.be,vioe-pypi-pr-vioe-test.lb.cumuli.be,vioe-es-dev.lb.cumuli.be,openam-vioe-dev.lb.cumuli.be,vioe-storage-dev.lb.cumuli.be'
    # Versie
    env.deploy_version = '0.9.1'
    env.redis_memory = '256M'



@task
def test():
    env.hosts = ['vioe-dossierdata-test-1.vm.cumuli.be']
    test_general_vars()
    multi_env_settings()
    env.server_no_proxy = 'localhost,msb-vioe-test.lb.cumuli.be,vioe-pypi-pr-vioe-test.lb.cumuli.be,vioe-es-test.lb.cumuli.be,openam-vioe-test.lb.cumuli.be,vioe-storage-test.lb.cumuli.be'
    # Versie
    env.deploy_version = '0.9.1'
    env.redis_memory = '256M'


@task
def prod():
    env.hosts = ['vioe-dossierdata-prod-1.vm.cumuli.be']
    prod_general_vars()
    multi_env_settings()
    env.server_no_proxy = 'localhost,msb-vioe-prod.lb.cumuli.be,vioe-pypi-pr-vioe-prod.lb.cumuli.be,vioe-es-prod.lb.cumuli.be,openam-vioe-prod.lb.cumuli.be,vioe-storage-prod.lb.cumuli.be'
    # Versie
    env.deploy_version = '0.9.1'
    env.redis_memory = '256M'


@task
def build():
    '''
    Build a software distribution.
    '''
    dist_dir = './dist'
    with settings(warn_only=True):
        if local("test -d %s" % env.code_dir).failed:
            local('git clone git@github.com:OnroerendErfgoed/dossierdata.git %s' % env.code_dir)
        get_project_versions('dossierdata')

    env.dossierdata_naam = '%s-%s' % ('dossierdata', env.url_slug)
    env.dossierdata_actual = '%s-%s' % ('dossierdata', env.actual_version)


    # Als de versie nog niet bestaat, builden
    with settings(warn_only=True):
        if local("test -f ./dist/%s.tar.gz" % (env.dossierdata_naam)).failed:
            local('mkdir -p %s' % dist_dir)

            with settings(warn_only=False):
                with lcd('%s/dossierdata/dossierdata/static' % env.code_dir):
                    local('bower install')

                with lcd('%s/dossierdata' % env.code_dir):
                    local('python setup.py sdist')
                    local('mv ./dist/{0}.tar.gz ../../dist/{1}.tar.gz'.format(env.dossierdata_actual, env.dossierdata_naam))

    create_build_config_dir()
    local('mkdir %s/data' % env.build_config_dir)

    mapping = _get_mapping()

    copy_and_replace(os.path.join(os.getcwd(), 'config/dossierdata.nginx'), '%s/dossierdata.nginx' % env.build_config_dir, mapping)
    copy_and_replace(os.path.join(os.getcwd(), 'config/%s' % env.process_mapping_source), '%s/process_mapping.yml' % env.build_config_dir, mapping)
    copy_and_replace(os.path.join(os.getcwd(), 'config/schema.nginx'), '%s/schema.nginx' % env.build_config_dir, mapping)
    copy_and_replace(os.path.join(os.getcwd(), 'config/status.nginx'), '%s/status.nginx' % env.build_config_dir, mapping)
    copy_and_replace(os.path.join(os.getcwd(), 'config/nginx.nginx'),
        '%s/nginx.nginx' % env.build_config_dir, mapping)
    copy_and_replace(os.path.join(os.getcwd(), 'config/supervisor_dossierdata.conf'), '%s/supervisor_dossierdata.conf' % env.build_config_dir, mapping)
    copy_and_replace('%s/dossierdata/production.ini' % env.code_dir, '%s/production.ini' % env.build_config_dir, mapping)
    copy_and_replace('%s/dossierdata/processen.json' % env.code_dir, '%s/data/processen.json' % env.build_config_dir, mapping)


def _get_mapping():
    return [
        ('venv_dir', env.venv_dir),
        ('dossier.proj_dir', env.dossier_proj_dir),
        ('schema.proj_dir', env.schema_proj_dir),
        ('http_proxy', env.server_http_proxy),
        ('no_proxy', env.server_no_proxy),
        ('static_location', '/static/%s' % env.deploy_version),
        ('oeauth.secret', 'djqw5wqdq452s14ds44R'),
        ('oeauth.consumer_key', env.oeauth_consumer_key),
        ('oeauth.consumer_secret', env.oeauth_consumer_secret),
        ('oeauth.callback_url', env.oeauth_callback),
        ('oeauth.oauth_host', env.oeauth_oauth_host),
        ('oeauth.authorize_url', env.oeauth_authorize_url),
        ('dossier.nginx.server_name', env.dossier_nginx_server_name),
        ('schema.nginx.server_name', env.schema_nginx_server_name),
        ('schema.nginx.server_alias', env.schema_nginx_server_name),
        ('nginx.pr_interface', env.ip_config[env.host]['nginx_pr_interface']),
        ('db_url', env.db_url),
        ('db_pwd', env.db_pwd),
        ('db_name', env.db_name),
        ('storageprovider.baseurl', env.storageprovider_baseurl),
        ('storageprovider.collection', env.storageprovider_collection),
        ('es_url', env.searchengine_baseurl),
        ('es_index', env.es_index),
        ('db_user', env.db_user),
        ('deploy_user', env.deploy_user),
        ('redis.host', env.ip_config[env.host]['redis_host']),
        ('oeauth.actor_url', env.oeauth_actor_url),
        ('process.mapping', env.process_mapping),
        ('dossiers.uri', env.dossiers_uri),
        ('uri_root', env.uri_root),
        ('uri_rewrite', env.uri_rewrite),
        ('session_factory.secret', env.session_factory_secret),
        ('urireferencer.registry_url', env.urireferencer_registry_url),
        ('crabpy.root', env.crabpy_root),
        ('gunicorn.port', env.gunicorn_port),
        ('gunicorn.workers', env.gunicorn_workers),
        ('gunicorn.threads', env.gunicorn_threads),
        ('administratievegrenzen.url', env.administratievegrenzen_url),
        ('crabpy.capakey.user', env.capakey_user),
        ('crabpy.capakey.password', env.capakey_password),
        ('regio_email.noord', env.regio_email_noord),
        ('regio_email.oost', env.regio_email_oost),
        ('regio_email.west', env.regio_email_west)
    ]


@task
def update_schemas():
    create_build_config_dir()

    mapping = _get_mapping()

    local('mkdir %s/schemas' % env.build_config_dir)

    for subdir, dirs, files in os.walk('schemas'):
        for file in files:
            filepath = os.path.join(subdir,file)
            inputfile = os.path.join(os.getcwd(),filepath)
            outputpath = os.path.join(env.build_config_dir, subdir)
            outputfile = '{0}/{1}'.format(env.build_config_dir,filepath)
            if not os.path.exists(outputpath):
                try:
                    os.makedirs(outputpath)
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            copy_and_replace(inputfile, outputfile, mapping)

    with settings(user=env.deploy_user):
        run('mkdir -p %s' % env.schema_proj_dir)
        run('rm -rf %s/*' % env.schema_proj_dir)
        put('%s/schemas/*' % env.build_config_dir, '%s' % env.schema_proj_dir)


@task
def copy():
    '''
    Copy stuff to server.
    '''
    with settings(user=env.deploy_user):
        run('rm -rf /home/%s/dossierdata*' % env.deploy_user)
        put('./dist/%s.tar.gz' % env.dossierdata_naam, '/home/%s' % env.deploy_user)
        run('mkdir -p %s' % env.dossier_proj_dir)
        put('%s/*' % (env.build_config_dir), '%s' % env.dossier_proj_dir)


@task
def install():
    '''
    Install stuff on server.
    '''
    with settings(user=env.deploy_user):
        install_gunicorn()
        virtualenv('pip install --upgrade --force-reinstall --no-deps /home/%s/*.tar.gz' % (env.deploy_user))
        run ('tar -xzf /home/%s/dossierdata*.tar.gz' % env.deploy_user)
        install_requirements('dossierdata*')
        run ('rm -rf /home/%s/dossierdata*' % env.deploy_user)
        save_version_history(env.url_slug)

    with settings(user='root'):
        run('service nginx stop', pty=False)
        run('mv %s/dossierdata.nginx /etc/nginx/conf.d/dossierdata.conf' % env.dossier_proj_dir)
        run('mv %s/status.nginx /etc/nginx/conf.d/status.conf' % env.dossier_proj_dir)
        run('mv %s/nginx.nginx /etc/nginx/nginx.conf' % env.proj_dir)
        run('mv %s/schema.nginx /etc/nginx/conf.d/schema.conf' % env.dossier_proj_dir)
        run('mv %s/supervisor_dossierdata.conf /etc/supervisor/conf.d/' % env.dossier_proj_dir)
        run('service nginx start', pty=False)
        run('mkdir -p /var/log/gunicorn')
        supervisor_restart()


@task
def firstboot():
    '''
    Tasks that are needed after fresh vm and before deploy app
    '''
    update_ubuntu()
    create_log_folder()


@task
def deploy():
    '''
    Build the latest version and deploy it to the servers.
    '''
    build()
    copy()
    update_schemas()
    create_virtualenv_if_not_exists()
    install()


@runs_once
@task
def initialize_regioverantwoordelijken_es():
    mapping = _get_mapping()
    local('mkdir -p %s/data' % env.build_config_dir)
    local('cat '
          './config/regioverantwoordelijken/opening_bracket '
          './config/regioverantwoordelijken/{1}/*.json '
          './config/regioverantwoordelijken/closing_bracket '
          '> {0}/data/regioverantwoordelijken.json'
          .format(env.build_config_dir, env.regioverantwoordelijken))
    with settings(user=env.deploy_user):
        put('%s/data/regioverantwoordelijken.json' % (env.build_config_dir), '%s/data/regioverantwoordelijken.json' % env.dossier_proj_dir)
        virtualenv('initialize_regioverantwoordelijken_es {0}/production.ini#dossierdata {0}/data/regioverantwoordelijken.json'.format(env.dossier_proj_dir))


@runs_once
@task
def initialize_werkgebieden_es(): 
    with settings(user=env.deploy_user):
        put('config/werkgebieden/{0}/*'.format(env.omgeving), '/tmp/')
        virtualenv('initialize_werkgebieden_en_werkregios_es {0}/production.ini#dossierdata /tmp/discipline_archeologie_email.xlsx /tmp/discipline_bouwkundig_email.xlsx /tmp/discipline_landschappen_email.xlsx'.format(env.dossier_proj_dir))


@task
def initialize_processen_es():
    mapping = _get_mapping()
    local('mkdir -p %s/data' % env.build_config_dir)
    copy_and_replace(os.path.join(os.getcwd(), 'config/%s' % env.processen), '%s/data/processen.json' % env.build_config_dir, mapping)
    with settings(user=env.deploy_user):
        put('%s/data/processen.json' % (env.build_config_dir), '%s/data/processen.json' % env.dossier_proj_dir)
        virtualenv('initialize_processen_es {0}/production.ini#dossierdata {0}/data/processen.json'.format(env.dossier_proj_dir))


@task
def es_initialize():
    with settings(user=env.deploy_user):
        virtualenv('export no_proxy="{1}"&&export http_proxy="{2}"&&export https_proxy="{2}"&&initialize_dossierdata_es {0}/production.ini#dossierdata'.format(env.proj_dir, env.server_no_proxy, env.server_http_proxy))


@task
def es_reindex():
    with settings(user=env.deploy_user):
        virtualenv('export no_proxy="{1}"&&export http_proxy="{2}"&&export https_proxy="{2}"&&reindex_dossierdata_es {0}/production.ini#dossierdata'.format(env.proj_dir, env.server_no_proxy, env.server_http_proxy))


@task
def redeploy_config():
    _redeploy_config(_get_mapping, 'dossierdata')
