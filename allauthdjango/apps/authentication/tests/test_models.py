
from ..models import User
from .test_data.test_data import user
from .test_base import BaseTest


class ModelTest(BaseTest):
    def test_can_create_a_user(self):
        new_user = User.objects.create_user(
            user['username'], user['email'], user['password'])
        self.assertEqual(str(new_user), 'crycetruly')
