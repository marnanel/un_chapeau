from .settings import UN_CHAPEAU

class Config(object):

    def __getitem__(self, field):
        return self.get(field)

    def get(self, field, **kwargs):
        return UN_CHAPEAU[field].format(
                hostname = UN_CHAPEAU['HOSTNAME'],
                **kwargs,
                )

config = Config()
