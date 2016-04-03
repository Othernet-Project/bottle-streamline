from streamline import RouteBase


class MyRoute(RouteBase):
    def get(self):
        return """Hello world!

        <form method="POST">
            <button type="submit" name="foo" value="bar">Click me!</button>
        </form>
        """


def main():
    MyRoute.route('/')
    MyRoute.bottle.run()


if __name__ == '__main__':
    main()
