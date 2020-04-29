from fabric import Connection, Config

from codebase_controller import CodebaseController
from server_values_reader import ServerValuesReader
from user_creator import UserCreator

if __name__ == '__main__':

    svr = ServerValuesReader()
    uc = UserCreator()
    cc = CodebaseController()

    server_values = svr.get_server_values()

    connect_kwargs = {
        'key_filename': server_values.pem_path
    }
    connection = Connection(host=server_values.host, user=server_values.user, connect_kwargs=connect_kwargs)
    uc.create(connection, server_values.user_create, server_values.password_create)

    # Recreating connection with new user
    connect_kwargs = {
        'password': server_values.password_create
    }
    config = Config(overrides={'sudo': {'password': server_values.password_create}})
    connection = Connection(host=server_values.host, user=server_values.user_create, config=config)
    cc.clone(connection, server_values.code_base_url, server_values.site_name)

    print(server_values.site_name, server_values.host, server_values.user, server_values.pem_path)