import bottle
from streamline import FormRoute

try:
    unicode = unicode
except NameError:
    unicode = str

required = lambda v: v and v.strip()
numeric = lambda v: unicode(v).strip().isnumeric() if v else True


class Simple(FormRoute):
    path = '/simple'

    def show_form(self):
        return 'Imagine this is a form'

    def form_valid(self):
        return 'OK: {} {}'.format(self.form.data.get('string', ''),
                                  self.form.data.get('number', ''))

    def form_invalid(self):
        self.response.status = 400
        return 'WRONG'

Simple.form_factory.validators['string'] = required
Simple.form_factory.validators['number'] = numeric


def main():
    Simple.route()
    bottle.run(debug=True)


if __name__ == '__main__':
    main()
