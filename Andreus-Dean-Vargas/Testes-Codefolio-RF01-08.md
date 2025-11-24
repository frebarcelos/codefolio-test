## Casos de Teste RF01-RF08

### CT-01 - Edição de Perfil do Usuário

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF1 - O sistema deve permitir que o usuário edite seu perfil, incluindo a atualização da foto, do nome exibido e links para suas redes sociais.

**Objetivo:**  
Verificar se o sistema permite que o usuário altere suas informações de perfil (foto, nome exibido e links de redes sociais) e salva corretamente as alterações.

**Pré-condição:**
- Usuário autenticado e na página de perfil (`/profile`)
- Usuário já possui uma foto, nome e links cadastrados

**Passos de execução:**
1. Acessar o menu "Perfil" no topo da aplicação
2. Clicar em "Editar Perfil"
3. Alterar o campo "Nome exibido" para "Andreus Dean"
4. Atualizar os campos de redes sociais:
   - Instagram: `https://instagram.com/andreusvargas`
   - LinkedIn: `https://linkedin.com/in/andreusvargas`
5. Clicar em "Salvar Alterações"

**Dados de Entrada:**
- Nome: "Andreus Dean"
- Instagram: `https://instagram.com/andreusvargas`
- LinkedIn: `https://linkedin.com/in/andreusvargas`

**Resultado Esperado:**  
O sistema deve exibir mensagem "Perfil atualizado com sucesso" e mostrar o novo nome imediatamente no perfil, além de exibir os links atualizados das redes sociais.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-02 - Cadastro de Curso

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF2 - O sistema deve permitir que o professor cadastre um novo curso, podendo definir ou não um PIN de acesso.

**Objetivo:**  
Verificar se o professor consegue cadastrar um novo curso sem definir PIN de acesso e se o curso fica disponível na lista.

**Pré-condição:**
- Usuário autenticado como professor
- Acesso à página de listagem de cursos (`/listcurso`)

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Clicar no botão "Adicionar Curso" ou "Novo Curso"
3. Preencher campo Título: "Introdução ao Selenium WebDriver"
4. Preencher campo Descrição: "Curso completo de automação de testes com Selenium WebDriver e Java"
5. Deixar campo PIN vazio
6. Clicar no botão "SALVAR" ou "Cadastrar"

**Dados de Entrada:**
- Título: "Introdução ao Selenium WebDriver"
- Descrição: "Curso completo de automação de testes com Selenium WebDriver e Java"
- PIN: (vazio)

**Resultado Esperado:**  
O sistema deve cadastrar o curso com sucesso e exibir mensagem de confirmação. O curso deve aparecer na lista de cursos e estar acessível sem necessidade de PIN.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-03 - Edição de Curso

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF3 - O sistema deve permitir que o professor edite os dados de um curso existente (título, descrição, PIN).

**Objetivo:**  
Verificar se o professor consegue editar o título de um curso existente e se a alteração é persistida corretamente no sistema.

**Pré-condição:**
- Usuário autenticado como professor
- Curso já cadastrado no sistema
- Acesso à lista de cursos (`/listcurso`)

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Localizar o curso desejado na lista
3. Clicar no botão "Editar" do curso
4. Alterar o campo Título para: "Selenium WebDriver - Atualizado"
5. Clicar no botão "SALVAR" ou "Atualizar"
6. Verificar se o título foi atualizado na lista

**Dados de Entrada:**
- Novo Título: "Selenium WebDriver - Atualizado"

**Resultado Esperado:**  
O sistema deve atualizar o título do curso com sucesso. O novo título deve aparecer na lista de cursos e a alteração deve ser persistida no banco de dados.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-04 - Exclusão de Curso

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF4 - O sistema deve permitir que o professor exclua um curso, solicitando confirmação antes da exclusão.

**Objetivo:**  
Verificar se o sistema solicita confirmação antes de excluir um curso e se a exclusão é realizada corretamente após confirmação do usuário.

**Pré-condição:**
- Usuário autenticado como professor
- Curso já cadastrado no sistema
- Acesso à lista de cursos (`/listcurso`)

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Localizar o curso a ser excluído
3. Clicar no botão "Excluir" do curso
4. Aguardar modal/diálogo de confirmação aparecer
5. Verificar mensagem de confirmação
6. Clicar no botão "Confirmar" ou "Sim"
7. Aguardar processamento
8. Verificar se o curso foi removido da lista

**Dados de Entrada:** Não aplicável

**Resultado Esperado:**  
O sistema deve exibir um modal de confirmação antes da exclusão. Após confirmação, o curso deve ser excluído com sucesso e não deve mais aparecer na lista. Mensagem de sucesso deve ser exibida.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-05 - Cadastro de Vídeo

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF5 - O sistema deve permitir que o professor adicione vídeos do YouTube aos cursos.

**Objetivo:**  
Verificar se o professor consegue adicionar um vídeo do YouTube a um curso e se o vídeo é exibido corretamente.

**Pré-condição:**
- Usuário autenticado como professor
- Curso já cadastrado no sistema
- Acesso à página interna do curso

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Clicar em "Acessar" no curso desejado
3. Localizar e clicar no botão "Adicionar Vídeo" ou "Novo Vídeo"
4. Preencher campo Título: "Aula 01 - Introdução ao Selenium"
5. Preencher campo Descrição: "Nesta aula veremos os conceitos básicos do Selenium WebDriver"
6. Preencher campo Link: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
7. Clicar no botão "SALVAR" ou "Cadastrar"

**Dados de Entrada:**
- Título: "Aula 01 - Introdução ao Selenium"
- Descrição: "Nesta aula veremos os conceitos básicos do Selenium WebDriver"
- Link: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

**Resultado Esperado:**  
O sistema deve cadastrar o vídeo com sucesso e exibir mensagem de confirmação. O vídeo deve aparecer na lista de vídeos do curso e o link do YouTube deve ser válido e funcional.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-06 - Edição de Vídeo

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF6 - O sistema deve permitir que o professor edite os dados de vídeos já cadastrados (título, descrição, link).

**Objetivo:**  
Verificar se o professor consegue editar o título de um vídeo já cadastrado e se a alteração é persistida corretamente.

**Pré-condição:**
- Usuário autenticado como professor
- Curso com vídeo já cadastrado
- Acesso à página do curso

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Clicar em "Acessar" no curso desejado
3. Localizar o vídeo a ser editado
4. Clicar no botão "Editar" do vídeo
5. Alterar o campo Título para: "Aula 01 - Introdução [ATUALIZADO]"
6. Clicar no botão "SALVAR" ou "Atualizar"

**Dados de Entrada:**
- Novo Título: "Aula 01 - Introdução [ATUALIZADO]"

**Resultado Esperado:**  
O sistema deve atualizar o título do vídeo com sucesso. O novo título deve aparecer na lista de vídeos e o vídeo deve continuar funcionando normalmente.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-07 - Exclusão de Vídeo

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF7 - O sistema deve permitir que o professor exclua vídeos dos cursos, solicitando confirmação antes da exclusão.

**Objetivo:**  
Verificar se o sistema permite excluir um vídeo após confirmação do usuário e se outros vídeos permanecem intactos.

**Pré-condição:**
- Usuário autenticado como professor
- Curso com vídeo já cadastrado
- Acesso à página do curso

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Clicar em "Acessar" no curso desejado
3. Localizar o vídeo a ser excluído
4. Clicar no botão "Excluir" do vídeo
5. Aguardar modal de confirmação
6. Clicar no botão "Confirmar" ou "Sim"
7. Verificar se o vídeo foi removido da lista

**Dados de Entrada:** Não aplicável

**Resultado Esperado:**  
O sistema deve exibir um modal de confirmação antes da exclusão. Após confirmação, o vídeo deve ser excluído e não deve mais aparecer na lista. Outros vídeos do curso devem permanecer intactos.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

### CT-08 - Cadastro de Slides

**Tipo de teste:** Funcional - Caixa Preta  
**Status:** Passível de execução  
**Autor:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Requisito:** RF8 - O sistema deve permitir que o professor adicione slides do Google Presentations aos cursos através do código HTML de embed.

**Objetivo:**  
Verificar se o professor consegue adicionar slides do Google Presentations a um curso através do código HTML de embed e se os slides são renderizados corretamente.

**Pré-condição:**
- Usuário autenticado como professor
- Curso já cadastrado
- Código HTML de embed do Google Presentations disponível

**Passos de execução:**
1. Acessar a página de cursos (`/listcurso`)
2. Clicar em "Acessar" no curso desejado
3. Localizar e clicar no botão "Adicionar Slides" ou "Novo Slide"
4. Preencher campo Título: "Slides - Aula 01: Introdução"
5. Preencher campo Código HTML com o iframe do Google Presentations
6. Clicar no botão "SALVAR" ou "Cadastrar"

**Dados de Entrada:**
- Título: "Slides - Aula 01: Introdução"
- Código HTML: `<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQv9.../embed" frameborder="0" width="960" height="569"></iframe>`

**Resultado Esperado:**  
O sistema deve cadastrar os slides com sucesso e exibir mensagem de confirmação. Os slides devem aparecer na lista de materiais do curso, o código HTML deve ser renderizado corretamente e os slides devem ser visualizáveis na plataforma.

**Resultado Obtido:** ✅ Correspondência ao esperado

---

## Informações Técnicas

### Estrutura do Projeto Python

**Linguagem:** Python 3.11+  
**Framework de Teste:** pytest 8.0+  
**Framework de Automação:** Selenium WebDriver 4.26.0  
**Navegador:** Google Chrome (Versão 142)  
**Gerenciador de Pacotes:** pip / poetry

### Dependências (requirements.txt)

```txt
pytest==8.0.0
selenium==4.26.0
pytest-html==4.1.1
pytest-xdist==3.5.0
webdriver-manager==4.0.1
```

## Pré-requisitos para Execução

✅ Python 3.11+ instalado  
✅ pip atualizado  
✅ Google Chrome atualizado (versão 142+)  
✅ ChromeDriver compatível (gerenciado automaticamente pelo webdriver-manager)  
✅ Conta de professor na plataforma Codefolio  

---

## Testador RF01-RF08

**Nome:** Andreus Dean Ferreira Almeida Rodrigues Vargas  
**Email:** andreusvargas.aluno@unipampa.edu.br  
**Instituição:** UNIPAMPA - Universidade Federal do Pampa  
**Campus:** Alegrete, RS, Brasil

---
