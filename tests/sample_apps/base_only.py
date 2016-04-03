from streamline import RouteBase


class MyRoute(RouteBase):
    def get(self):
        return 'Hello world!'


def main():
    MyRoute.route('/')
    MyRoute.bottle.run()


if __name__ == '__main__':
    main()
