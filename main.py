import sys

from fabric import Connection, Config

from codebase_controller import CodebaseController
from django_controller import DjangoController
from server_values_reader import ServerValuesReader
from user_creator import UserCreator

if __name__ == '__main__':

    # Reading arguments
    use_already_saved_values = False
    skip_user_create = False
    skip_codebase_setup = False
    skip_django_setup = False
    try:
        argv = sys.argv[1:]
        use_already_saved_values = '-use_already_saved_values' in argv
        skip_user_create = '-skip_user_create' in argv
        skip_codebase_setup = '-skip_codebase_setup' in argv
        skip_django_setup = '-skip_django_setup' in argv
    except Exception as e:
        print('Reading parameter error')
        sys.exit(2)

    # Creating controller objects
    svr = ServerValuesReader()
    uc = UserCreator()
    cc = CodebaseController()
    dc = DjangoController()

    server_values = svr.get_server_values(use_already_saved_values)

    if not skip_user_create:
        connect_kwargs = {
            'key_filename': server_values.pem_path
        }
        connection = Connection(host=server_values.host, user=server_values.user, connect_kwargs=connect_kwargs)
        uc.create(connection, server_values.user_create, server_values.password_create)

    # Recreating connection with new user
    connect_kwargs = {'password': server_values.password_create}
    config = Config(overrides={'sudo': {'password': server_values.password_create}})
    connection = Connection(host=server_values.host, user=server_values.user_create, config=config,
                            connect_kwargs=connect_kwargs)

    if not skip_codebase_setup:
        cc.clone(connection, server_values.code_base_url, server_values.site_name)
    if not skip_django_setup:
        dc.setup(connection, server_values.site_name)

    print(server_values.site_name, server_values.host, server_values.user, server_values.pem_path)
