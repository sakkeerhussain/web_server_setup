from patchwork import files
from slugify import slugify


class DjangoController:

    def setup(self, connection, codebase_url, name):
        slug = slugify(name)
        try:
            connection.run('mkdir {}'.format(slug))
        except Exception as e:
            pass

        if codebase_url.startswith('git'):
            codebase_base_url = codebase_url[4:].split(':')[0]
        elif codebase_url.startswith('https'):
            codebase_base_url = codebase_url[8:].split('/')[0].split('@')[-1]
        else:
            print('Invalid git protocol found, Skipping adding ssh key white listing')
            codebase_base_url = None
        if codebase_base_url:
            connection.sudo('ssh-keyscan -t rsa {} >> ~/.ssh/known_hosts'.format(codebase_base_url))
            print('Adding {} to known hosts'.format(codebase_base_url))

        connection.run('pwd')
        ssh_file = '~/.ssh/id_rsa'
        ssh_pub_file = ssh_file + '.pub'
        if not files.exists(connection, ssh_pub_file):
            connection.run('ssh-keygen -b 2048 -t rsa -f {} -q -N ""'.format(ssh_file))
            connection.run('cat {}'.format(ssh_pub_file))
            input('Hit enter after adding git deployment key')

        with connection.cd(slug):
            connection.run('git clone {}'.format(codebase_url))

        print('Cloned code repo to path: {}'.format(slug))
