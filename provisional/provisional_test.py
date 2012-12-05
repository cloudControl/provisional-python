import unittest

from mock import patch
import provisional
from provisional import Provisional

'''
    @author: Dimitris Verraros (dv@cloudcontrol.de)
    @author: Denis Neuling (dn@cloudcontrol.de)
'''


class ProvisionalTestMain(unittest.TestCase):

    @patch.dict('os.environ', {"DEP_NAME": "app/dep"})
    @patch('sys.exit')
    @patch('sys.stderr')
    @patch('flask.Flask.run')
    def testMain(self, exit, stderr, flask_run):
        main_arguments = ["sdfgsgsgs"]
        provisional.main(main_arguments)
        self.assertEquals(2, stderr.write.call_count)
        self.assertEquals(1, exit.call_count)


class ProvisionalTestCase(unittest.TestCase):

    def setUp(self):
        provisional.app.credentials = ""
        provisional.app.provisional = Provisional()
        self.app = provisional.app.test_client()

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testGetRoot(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.get('/').data
        assert 'Ok' in resp

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testGetHealthCheck(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.get('/health-check').data
        assert "Ok" in resp

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testGetResource(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.get('/cloudcontrol/resources/12').data
        assert "Not found" in resp

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testCreateResource(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.post('/cloudcontrol/resources/').data
        assert "Bad Request" in resp

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testUpdateResource(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.put('/cloudcontrol/resources/14').data
        assert "Bad Request" in resp

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testDeleteResource(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.delete('/cloudcontrol/resources/15').data
        assert "Not found" in resp

    @patch('provisional.request')
    @patch('provisional.check_auth')
    def testInvalidRequest(self, request, check_auth):
        request.authorization.return_value = True
        check_auth.return_value = True
        resp = self.app.get('/cloudcontrol/resources/').data
        assert "405" in resp


if __name__ == '__main__':
    unittest.main()
