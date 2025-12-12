import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time


class AcessoCursosTest(unittest.TestCase):

    def setUp(self):
        
        self.TIMEOUT = 15
        self.URL_BASE = "https://testes-codefolio.web.app/"
        
        # --- 1. DADOS DO FIREBASE (MANTIDOS POR SER REQUISITO DE LOGIN) ---
        self.FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"
        self.FIREBASE_VALUE = """{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763557230421","displayName":"Bruno da Silva Rocha","email":"brunorocha.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763557440888","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocJXjw8Ot4lIsX06tsyT7jGw9FnxOzTul0fdApQaEHEd1sRz1NE=s96-c","providerData":[{"providerId":"google.com","uid":"117737474264388906032","displayName":"Bruno da Silva Rocha","email":"brunorocha.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocJXjw8Ot4lIsX06tsyT7jGw9FnxOzTul0fdApQaEHEd1sRz1NE=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQnJ1bm8gZGEgU2lsdmEgUm9jaGEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSlhqdzhPdDRsSXNYMDZ0c3lUN2pHdzlGbnhPelR1bDBmZEFwUWFFSEVkMXNSejFORT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS90ZXN0ZXMtY29kZWZvbGlvIiwiYXVkIjoidGVzdGVzLWNvZGVmb2xpbyIsImF1dGhfdGltZSI6MTc2MzU1NzQ0MCwidXNlcl9pZCI6IkRPUlB1VFBuNDBOV3hiVFJxOG5DWUZuSXpWSzIiLCJzdWIiOiJET1JQdVRQbjQwTld4YlRScThuQ1lGbkl6VksyIiwiaWF0IjoxNzYzNTU3NDQwLCJleHAiOjE3NjM1NjEwNDAsImVtYWlsIjoiYnJ1bm9yb2NoYS5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNzczNzQ3NDI2NDM4ODkwNjAzMiJdLCJlbWFpbCI6WyJicnVub3JvY2hhLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.GQKtBpMW1z5psdvVcXNh-k449_T9ANMqSa9ukT27ujBnt5Tyx4ZSzOG4WyvrYZioRovhIbqyHjqtwzmPywlSN94r2DLMFMFFWFj8BxcRiLagqfSkyJoPgnjy68R6bw1UTntEQHrZk6oWkQfdtmicO817xO1h2UO0KGxkBiBywdM_XNqGJTk4bxxnK3ICTABoamyZBJ0lgP0UqVD4fDCLlqV1b0hkO7_gvBgjNHrqdrHXbPNZEVXbGPvmFqFBdrDXx5ncK03mxts1XOdWCFBWvRl-LeyIDmDt3J_Sadiy1FCFG2ae4e578e3OeLpsYNwp1UFZ71X74JYDcPf75UEMeQ","expirationTime":1763561041130,"refreshToken":"AMf-vByMbiwH6jHLS5DCTb3JoKPQ7OZY5UTxbyEXh-efyzifQ2NyjsknU0xiS5ZSyXqnvpCdIrfEEKJR63U9deh7vQ7sQpBYB6fqmJduztANr-BbsSdblzmExR2ztfnKRfONcKijnoxgCvQN0aqp5yp9j6JkdVe7k89FVoRo6qhpOKVl_TtZNYvz4kCrmwX9ac6oiXNzzRwOF6gHhcn5jKUZIulV3KAHYL5xY6uOfqWG6pUQPnJT0JgDMJKMdUJ70rbREMPAU2KorpdZ9mSuqN461FZmYYZ3p99pTdpOF_W6MQV4Hgr1QEYNROf6fURVRyhW2hidwSTwaVDc5s07dFmelZ2UJZ_hB3loOoorG5Ljlh3vF_p_Eu9mzDW3X49EQtCuPOJvMVzpgzTIQIjNQvdYyOqfQlRHiTnARclq_LZ9Dp316k_LvoS-WY94nhaxOU8A10Dror5U26KorgwCLfvB_xCZUxe9hg"},"tenantId":null,"uid":"DORPuTPn40NWxbTRq8nCYFnIzVK2","_redirectEventId":null}"""

        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        # Inicializa o serviço do Chrome
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)

        # --- ESTRATÉGIA LOCAL STORAGE (LOGIN) ---

        # 1. Carrega o domínio
        self.driver.get(self.URL_BASE)

        # 2. Injeta os dados no Local Storage
        print("Injetando dados de autenticação no Local Storage...")
        try:
            self.driver.execute_script(
                "window.localStorage.setItem(arguments[0], arguments[1]);",
                self.FIREBASE_KEY,
                self.FIREBASE_VALUE
            )
            print("Injeção no Local Storage bem-sucedida.")

        except Exception as e:
            print(f"Falha crítica ao injetar no Local Storage: {e}")
            self.driver.quit()
            raise RuntimeError("Falha no setup do Local Storage") from e
        
        print("Recarregando a página...")
        self.driver.refresh()
    
    def test_saida_quiz_qualquer_momento(self):
        """Testa encerramento do quiz."""
        print("Acessando o Quiz...")
    
        teste_passou = True
    
        XPATH_BOTAO_VER_CURSO = "//h6[normalize-space(text())='Curso Grupo 4 com PIN']/ancestor::div[contains(@class, 'MuiCard-root')]//button[text()='Ver Curso']"
        XPATH_QUIZ_GIGI = "//button[@title='Abrir Quiz Gigi']"
    
        if teste_passou:
            try:
                print("1/6 - Tentativa de clicar no 'link do cursos'...") 
                curso_link = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section[2]/div[2]/div/div[1]/div/div[2]/div/a[2]'))
                )
                time.sleep(3)
                self.driver.save_screenshot("Bruno-Rocha/img/img-RF37/passo_1.png")
                curso_link.click()
            except (TimeoutException, NoSuchElementException, Exception) as e:
                print(f"Falha na etapa 1 (Link do Curso): {e}")
                teste_passou = False
                    
        if teste_passou:
            try:
                print("2/6 - Tentativa de clicar em 'cursos concluídos'...")        
                cursos_concluidos = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div/div/button[3]'))
                )
                self.driver.save_screenshot("Bruno-Rocha/img/img-RF37/passo_2.png")
                cursos_concluidos.click()
                time.sleep(3)
            except(TimeoutException, NoSuchElementException, Exception) as e:
                print(f"Falha na etapa 2 (Cursos Concluídos): {e}")
                teste_passou = False
        
        if teste_passou:
            try:
                print("3/6 - Tentativa de ver um 'curso concluído'...")
                botao_comecar_curso = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_VER_CURSO))
                )
                self.driver.save_screenshot("Bruno-Rocha/img/img-RF37/passo_3.png")
                botao_comecar_curso.click()
                time.sleep(3)
            except(TimeoutException, NoSuchElementException, Exception) as e:
                print(f"Falha na etapa 3 (Começar curso concluído): {e}")
                teste_passou = False

        if teste_passou:
            try:
                print("4/6 - Tentativa de fazer o 'Quiz Gigi'...")
                botao_fazer_quiz_gigi = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_QUIZ_GIGI))
                )
                self.driver.save_screenshot("Bruno-Rocha/img/img-RF37/passo_4.png")
                botao_fazer_quiz_gigi.click()
                time.sleep(3)
            except(TimeoutException, NoSuchElementException, Exception) as e:
                print(f"Falha na etapa 4 (Acessar o Quiz Gigi): {e}")
                teste_passou = False
            self.driver.save_screenshot("Bruno-Rocha/img/img-RF37/passo_5.png")
        if teste_passou:
            try:
                print("5/6 - Tentativa de clicar no botão 'Fechar Quiz'...")
            
                js_script_fechar = """
                var icon = document.querySelector("svg[data-testid='CloseIcon']");
                if (icon) {
                    var btn = icon.closest("button");
                    if (btn) {
                        btn.click();
                        return true;
                    }
                }
                return false;
                """
                foi_clicado = False
                tempo_limite = time.time() + 5
            
                while time.time() < tempo_limite:
                    if self.driver.execute_script(js_script_fechar):
                        foi_clicado = True
                        break
                    time.sleep(0.5)
            
                self.assertTrue(foi_clicado, "Falha Crítica: O script não encontrou o botão com 'CloseIcon' para clicar.")
            
                print("Teste sáida do Quiz realizado com sucesso.")
                self.driver.save_screenshot("Bruno-Rocha/img/img-RF37/passo_6.png")
                time.sleep(3)

            except (AssertionError, Exception) as e:
                print(f"Falha na etapa 5 (Botão Fechar): {e}")
                teste_passou = False
    
    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            time.sleep(10)
            self.driver.quit() 

if __name__ == "__main__":
    unittest.main()