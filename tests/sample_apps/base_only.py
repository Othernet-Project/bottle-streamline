from streamline import RouteBase


class MyRoute(RouteBase):
    path = '/'

    def get(self):
        self.response.headers['foo'] = 'bar'
        return 'Hello world!'


class MyOtherRoute(RouteBase):
    path = '/other'

    def post(self):
        return 'Posted'

    def delete(self):
        return 'Deleted'

    def patch(self):
        return 'Patched'


def main():
    MyRoute.route()
    MyOtherRoute.route()
    MyRoute.bottle.run()


if __name__ == '__main__':
    main()
