from .. import AppBaseTest


class FrontendRouteTests(AppBaseTest):

    def test_dashboard(self):
        rv = self.app.get('/')
        assert 'Redirecting' in rv.data
