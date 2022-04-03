import unittest
import requests

SERVER_ADDRESS = 'http://localhost:5000/'

class FsServerTests(unittest.TestCase):

        def test_nivel_A(self):
                            
            response = requests.post(f'{SERVER_ADDRESS}/spotify')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.content.decode(), 
                render_template('/ui-spotify.html', mytitle='top 50 canciones más populares', contenido=D)
            )

            response = requests.post(f'{SERVER_ADDRESS}/twitter')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.content.decode(), 
                render_template('/ui-twitter.html', artista=artista, contenido=array_data )    
            )

            response = requests.post(f'{SERVER_ADDRESS}/red_social')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.content.decode(), 
                render_template('/ui-redsocial.html', contenido=tweets)
            )
