from urlshort import create_app

def test_shorten(client):
    #we want to find the word shorten on ou homepage
    response = client.get('/')
    assert b'Shorten' in response.data