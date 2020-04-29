import crypt


class UserCreator:

    def create(self, connection, user_create, password_create):
        encrypted_password = crypt.crypt(password_create)

        try:
            connection.sudo('useradd -m -p {password} -s /bin/bash {user}'.format(password=encrypted_password,
                                                                                  user=user_create))
        except Exception as e: # Used for handling user already exists error
            pass

        connection.sudo('usermod -aG sudo {user}'.format(user=user_create))
        print('Created user and added to sudoers group')

        connection.sudo('sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" '
                        '/etc/ssh/sshd_config')
        connection.sudo('sudo service sshd restart')
        print('Enabled password authentication')

