from unittest import TestCase

from app import app, games

from boggle import BoggleGame

from flask import jsonify

import json

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


    def test_api_score_word(self):
        """ Test making a post request to score word """
        with self.client as client:
            resp = client.get('/api/new-game')
            response_data = resp.get_json()
            gameId_test = response_data['gameId']

            # set board to letters we can test
            games[gameId_test].board = [['N', 'L', 'C', 'N', 'M'],
                                        ['Z', 'S', 'U', 'P', 'X'],
                                        ['T', 'C', 'A', 'P', 'C'],
                                        ['A', 'T', 'V', 'E', 'U'],
                                        ['U', 'K', 'O', 'U', 'E']]
                                        
            # set test cases and expected results
            test_cases = {
                "CAP": "ok",
                "HELLO": "not-on-board",
                "JNFN": "not-word",
                "123": 'not-word',
                ' ': 'not-word',
            }

            for word, result in test_cases.items():

                score_resp = client.post(
                    '/api/score-word',
                    data=json.dumps({"word": word,
                                  "gameId": gameId_test}),
                    content_type="application/json")
     
                score_resp_data = score_resp.get_json()
                self.assertEqual(score_resp_data['result'], result)

