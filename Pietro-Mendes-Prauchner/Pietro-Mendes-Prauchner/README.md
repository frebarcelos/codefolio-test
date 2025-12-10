# RF41 - Teste de Comentários em Vídeos

## Descrição

Teste Selenium para validar a funcionalidade RF41: Comentar em vídeos disponíveis através da HOME.

## Requisito

O sistema deve permitir que o estudante comente nos vídeos disponíveis através da "home".

## Estrutura do Teste

### Arquivo Principal
- `RF41_CT01_ComentarEmVideos.py` - Teste Selenium unitário com fluxo completo

### Arquivos de Suporte
- `login_util.py` - Autenticação Firebase via localStorage (credenciais: Pietro Mendes Prauchner)
- `chrome_config.py` - Configuração do Chrome WebDriver
- `requirements.txt` - Dependências do projeto

## Dependências

```
selenium>=4.0.0
webdriver-manager>=3.8.0
pytest>=7.0.0
```

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

### Com pytest (recomendado)
```bash
pytest RF41_CT01_ComentarEmVideos.py -v -s
```

### Com unittest
```bash
python -m unittest RF41_CT01_ComentarEmVideos
```

## Fluxo do Teste

1. **LOGIN** - Injeção de credenciais Firebase no localStorage
2. **VALIDAR LOGIN** - Verifica se o login foi bem-sucedido
3. **NAVEGAR PARA HOME** - Acessa a página inicial
4. **PROCURAR VÍDEO** - Localiza o iframe do YouTube
5. **CLICAR EM COMENTÁRIOS** - Abre o modal de comentários
6. **PROCURAR CAMPO** - Localiza o input de comentário no modal
7. **DIGITAR E ENVIAR** - Digita comentário e clica botão de envio
8. **VALIDAR PUBLICAÇÃO** - Verifica se o comentário foi publicado

## Estrutura das Credenciais

As credenciais de Pietro Mendes Prauchner estão armazenadas em `login_util.py`:

```python
Email: pietroprauchner.aluno@unipampa.edu.br
Nome: Pietro Mendes Prauchner
```

## Resultado Esperado

- ✅ PASSED: Teste executa com sucesso e comentário é publicado
- ✅ ~50-70 segundos de duração
- ✅ Browser fecha automaticamente ao final

## Troubleshooting

### Erro: Token expirado
Se receber erro de token expirado, os tokens Firebase em `login_util.py` precisam ser renovados com novas credenciais.

### Erro: Campo de comentário não encontrado
Verifique se o modal de comentários abriu corretamente após clicar em "Comentários".

### Erro: WebDriver não encontrado
Execute `pip install webdriver-manager` para download automático do ChromeDriver.

## Notas

- O teste usa credenciais injetadas no localStorage, não faz login via UI
- O Chrome é executado em modo normal (não headless) por padrão
- Para headless mode, descomente em `chrome_config.py`
- Timestamps são adicionados aos comentários para garantir unicidade

---

**Última atualização:** 2025-11-26  
**Status:** ✅ Funcional e Testado
