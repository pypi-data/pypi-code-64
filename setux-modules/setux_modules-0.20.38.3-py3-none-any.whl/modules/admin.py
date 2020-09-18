from setux.core.module import Module


class Distro(Module):
    '''Set User as sudoer
    kw:
        usr : User name
        pub : Piblic key

    - Create User if not present
    - Add User to sudoers
    - Send User's public key
    '''

    def deploy(self, target, **kw):

        usr = kw['usr']
        pub = kw['pub']

        distro = target.distro

        if not distro.user(usr).deploy():
            return False

        if not target.deploy('sudoers', user=usr):
            return False

        if not target.deploy('copy_id', **kw):
            return False

        return True
