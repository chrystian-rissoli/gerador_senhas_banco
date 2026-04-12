import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"API Gerador de Senhas Banc\xc3\xa1rias est\xc3\xa1 no ar!" in response.data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_gerar_senha_default(client):
    response = client.get('/gerar-senha')
    assert response.status_code == 200
    data = response.get_json()
    assert 'senha' in data
    senha = data['senha']
    assert len(senha) == 12
    # Verificar se tem pelo menos um de cada tipo
    assert any(c.isupper() for c in senha)
    assert any(c.islower() for c in senha)
    assert any(c.isdigit() for c in senha)
    assert any(c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for c in senha)

def test_gerar_senha_custom(client):
    response = client.get('/gerar-senha?comprimento=16&especiais=false')
    assert response.status_code == 200
    data = response.get_json()
    assert 'senha' in data
    senha = data['senha']
    assert len(senha) == 16
    assert any(c.isupper() for c in senha)
    assert any(c.islower() for c in senha)
    assert any(c.isdigit() for c in senha)
    # Sem especiais
    assert not any(c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for c in senha)

def test_gerar_senha_invalid_comprimento(client):
    response = client.get('/gerar-senha?comprimento=5')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Comprimento deve estar entre 8 e 128"}

def test_gerar_senha_no_types(client):
    response = client.get('/gerar-senha?maiusculas=false&minusculas=false&numeros=false&especiais=false')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Pelo menos um tipo de caractere deve ser selecionado"}

def test_gerar_senha_invalid_comprimento_type(client):
    response = client.get('/gerar-senha?comprimento=abc')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Parâmetro 'comprimento' deve ser um inteiro"}