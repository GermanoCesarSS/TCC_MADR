import pytest

from tcc_madr.utils import sanitize_input


@pytest.mark.parametrize(
    'input_str, expected',
    [
        ('Machado de Assis', 'machado de assis'),
        ('Manuel        Bandeira', 'manuel bandeira'),
        ('Edgar Alan Poe         ', 'edgar alan poe'),
        ('Androides Sonham Com Ovelhas Elétricas?', 'androides sonham com ovelhas elétricas'),
        ('  breve  história  do tempo ', 'breve história do tempo'),
        ('O mundo assombrado pelos demônios', 'o mundo assombrado pelos demônios'),
        # Casos adicionais para cobertura completa
        ('', ''),  # String vazia
        ('     ', ''),  # Apenas espaços
        ('Especial!@#$$%^&*()_+', 'especial'),  # Apenas caracteres especiais
        ('São Paulo é incrível!!!', 'são paulo é incrível'),
        ('\tNova Linha\t', 'nova linha'),  # Tabs
        ('\nQuebra de linha\n', 'quebra de linha'),  # Quebras de linha
        ('Múltiplos   tipos \t de espaços\n', 'múltiplos tipos de espaços'),
        ('Café com Leite', 'café com leite'),  # Com acentos
        ('1234567890', '1234567890'),  # Números
        ('Nome_Sem_Underscores', 'nomesemunderscores'),  # Sem Underscores
        ('Misto de Letras e Números 123', 'misto de letras e números 123'),
    ]
)
def test_sanitize_input(input_str, expected):
    assert sanitize_input(input_str) == expected
