class Environment(object):
    def __init__(self):
        self._base_url = "http://192.168.0.105/"
        self.username = "admin"
        self.password = "admin123"

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        # print("wether need to change another variable")
        self._base_url = value
        # print("base_url::set base_url success! ==> {}".format(self._base_url))


