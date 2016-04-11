import os
import bottle

from streamline import TemplateRoute, ROCARoute


THISDIR = os.path.abspath(os.path.dirname(__file__))
VIEWSDIR = os.path.join(THISDIR, 'views')

bottle.TEMPLATE_PATH.insert(0, VIEWSDIR)


class MyRoute(TemplateRoute):
    path = '/hello/:name'
    template_name = 'hello'

    def get(self, name):
        return locals()


class MyRocaRoute(ROCARoute):
    path = '/roca'
    template_name = 'roca_base'
    partial_template_name = 'roca_partial'

    def get(self):
        return


def main():
    MyRoute.route()
    MyRocaRoute.route()
    bottle.run()


if __name__ == '__main__':
    main()
