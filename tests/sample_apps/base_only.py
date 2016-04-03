from streamline import RouteBase


class MyRoute(RouteBase):
    def get(self):
        self.response.headers['foo'] = 'bar'
        return 'Hello world!'


class MyOtherRoute(RouteBase):
    def post(self):
        return 'Posted'

    def delete(self):
        return 'Deleted'

    def patch(self):
        return 'Patched'


def main():
    MyRoute.route('/')
    MyOtherRoute.route('/other')
    MyRoute.bottle.run()


if __name__ == '__main__':
    main()
