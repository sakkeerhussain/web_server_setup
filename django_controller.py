import os

from slugify import slugify


class DjangoController:

    def setup(self, connection, name):
        slug = slugify(name)
        code_folder = os.path.join(slug, 'code')
        connection.sudo('apt-get -qq update')
        connection.sudo('apt-get -qq upgrade')
        connection.sudo('apt-get -qq install python-virtualenv')
        with connection.cd(slug):
            connection.run('virtualenv venv -p $(which python3)')
            connection.run('source venv/bin/activate')
            connection.run('pip install -r code/requirements.txt')
            connection.run('pip freeze')
        # try:
        # except Exception as e:
        #     pass

        print('Setup django completed')
