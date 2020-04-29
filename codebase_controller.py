from invoke.util import cd
from slugify import slugify


class CodebaseController:

    def clone(self, connection, codebase_url, name):
        slug = slugify(name)
        connection.sudo('mkdir {}'.format(slug))
        with cd(slug):
            connection.run('git clone {}'.format(codebase_url))

        print('Cloned code repo to path: {}'.format(slug))