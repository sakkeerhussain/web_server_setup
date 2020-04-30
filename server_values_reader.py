import collections
import os

import yaml

from slugify import slugify


ServerValues = collections.namedtuple('ServerValues', ['site_name', 'host', 'user', 'pem_path', 'user_create',
                                                       'password_create', 'code_base_url'])


class ServerValuesReader:

    def __init__(self):
        self._config_file_path = 'config.yml'
        self._environ = {}
        self._site_prefix = ''
        self._overwrite_env_values = False
        self._use_already_saved_values = False

    def _get_slug(self, name):
        env_name = '{}-{}'.format(self._site_prefix, name) if self._site_prefix else name
        return slugify(env_name)

    def _read_value(self, name, options=None, yes_or_no=False):
        if yes_or_no and not options:
            options = ['y', 'n']
        slug = self._get_slug(name)
        env_val = self._environ.get(slug, '')

        if env_val != '' and self._use_already_saved_values:
            res = env_val
        else:
            message = "Please provide {} ".format(name)
            if env_val != '':
                message = message + ", Leave blank for '{}'".format(env_val)
            if options:
                message = message + " ({})".format('/'.join(options))
            user_val = input(message + ': ')
            res = user_val if user_val else env_val

        if yes_or_no:
            res = res == 'y' or res

        if self._overwrite_env_values:
            self._environ[slug] = res
        return res

    def _read_environ(self):
        global environ
        if not os.path.exists(self._config_file_path): return
        file = open(self._config_file_path, 'r')
        environ = yaml.load(file, Loader=yaml.FullLoader)

    def _save_environ(self):
        file = open(self._config_file_path, 'w')
        yaml.dump(environ, file)

    def get_server_values(self):
        self._read_environ()

        self._use_already_saved_values = self._read_value('use already saved values', yes_or_no=True)

        site_prefix_name = 'site prefix'
        self._site_prefix = self._read_value(site_prefix_name)
        overwrite_env_name = 'overwrite env values'
        self._overwrite_env_values = self._read_value(overwrite_env_name, yes_or_no=True)
        if self._overwrite_env_values:
            site_prefix_slug = self._get_slug(site_prefix_name)
            overwrite_env_slug = self._get_slug(overwrite_env_name)
            self._environ[site_prefix_slug] = self._site_prefix
            self._environ[overwrite_env_slug] = self._overwrite_env_values

        site_name = self._read_value('name')
        host = self._read_value('host address')
        user = self._read_value('user name')
        pem_path = self._read_value('pem file location')
        user_create = self._read_value('user name to be created')
        password_create = self._read_value('password of the new user')
        code_base_url = self._read_value('code base url')

        self._save_environ()

        return ServerValues(site_name=site_name, host=host, user=user, pem_path=pem_path, user_create=user_create,
                            password_create=password_create, code_base_url=code_base_url)
