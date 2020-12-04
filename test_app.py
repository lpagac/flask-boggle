from unittest import TestCase

from app import app, games

from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="newWordForm"', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            resp = client.get('/api/new-game')
            response_data = resp.get_json()
            self.assertIsInstance(response_data, dict)
            self.assertIsInstance(response_data['gameId'], str)
            
            # check if the board is a list of lists
            self.assertIsInstance(response_data['board'], list)
            self.assertIsInstance(response_data['board'][0], list)
            
            ## check if gameID is stored in game dictionary
            gameId_test = response_data['gameId']
            self.assertIn(gameId_test, games.keys())
            
            # check that value in game dictionary is an instance of BoggleGame
            game_test = games[gameId_test]
            self.assertIsInstance(game_test, BoggleGame)