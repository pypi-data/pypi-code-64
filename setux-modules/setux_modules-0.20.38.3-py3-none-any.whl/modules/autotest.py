from setux.core.module import Module


class Distro(Module):
    '''Setux self test

    - test deploy
    - test remote
    - test run
    '''

    def deploy(self, target, **kw):

        target.deploy('infos')
        target.remote('infos')
        target('setux infos')

        return True
