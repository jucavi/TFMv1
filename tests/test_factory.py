from . import BaseTestClass

class AppTestFactory(BaseTestClass):
    def test_config(self):
        self.assertTrue(self.app.testing)


    def test_hello(self):
        client = self.app.test_client()
        response = client.get('/hello')
        self.assertEqual(response.data, b'Hello Flask!')