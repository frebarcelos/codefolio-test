import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class AcessoCursosTest(unittest.TestCase):

    def setUp(self):
        
        self.TIMEOUT = 15
        self.URL_BASE = "https://testes.codefolio.com.br/"
        
        # --- 1. DADOS DO FIREBASE (MANTIDOS POR SER REQUISITO DE LOGIN) ---
        self.FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
        self.FIREBASE_VALUE = """{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400711892","displayName":"Bruno da Silva Rocha","email":"brunorocha.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1762433722027","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocJXjw8Ot4lIsX06tsyT7jGw9FnxOzTul0fdApQaEHEd1sRz1NE=s96-c","providerData":[{"providerId":"google.com","uid":"117737474264388906032","displayName":"Bruno da Silva Rocha","email":"brunorocha.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocJXjw8Ot4lIsX06tsyT7jGw9FnxOzTul0fdApQaEHEd1sRz1NE=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQnJ1bm8gZGEgU2lsdmEgUm9jaGEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSlhqdzhPdDRsSXNYMDZ0c3lUN2pHdzlGbnhPelR1bDBmZEFwUWFFSEVkMXNSejFORT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjQzMzcyMiwidXNlcl9pZCI6Im5DV21lMzhMcDFibWF0UTU3dnlUbVlFTm1mRzMiLCJzdWIiOiJuQ1dtZTM4THAxYm1hdFE1N3Z5VG1ZRU5tZkczIiwiaWF0IjoxNzYyNzE5NTE4LCJleHAiOjE3NjI3MjMxMTgsImVtYWlsIjoiYnJ1bm9yb2NoYS5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNzczNzQ3NDI2NDM4ODkwNjAzMiJdLCJlbWFpbCI6WyJicnVub3JvY2hhLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.mU2_c1T1U9DxhBlqv2uKT64TkXvKl9SK12qGD_hz8TdRfwd3LIORJ5A-VQhih_vJxX3vanaDF2oWmsr8gwbaMDHAo_0tRTyxeYRPDalu127Quvj89HziWhwQ0JiIWgEa6tKEMB_SFEIiisEIRmJ9SKTzzh2_Vj0M-9-moSk1xptkjGnhfd2X-H_mAG938RWz56rjV6yl2a0gjXw24MNgUy9jogeRD87SGYoHnB_oi3zeAlHz4XCZCS5BP10ZOYOjnYSrqHGJLften02_AtFG7_PcIwRJFjVvHDHaS5ZlGu4C5qwIa_09dOK_tpEC04UiDE1RcI_oqxSnnMNDTDdvkQ","expirationTime":1762723118009,"refreshToken":"AMf-vBxY_jDI2tZJwZag5yCOIDkf5gFUflsSz4UXF9ne9-xC9HdXY6rgUeY5UZqb6AeiIOL3Kd_gFpIytGxZmTJTNABtMCU2AoJLJqjk44ewZYLQtC7LULxSE2ZLWs1VTxdqTcws2pcxxUluOqBqhvgO5U2E8FETwiNvrZmS2vpSvP1Es9QMDSC6iJ9c8GD8LvEQp0PdbboFxtCFm5lVO4aB5RwBTG40-RMoXrSkG7LZBajvvdvTrh6EXF-tmX-sKzcvHEcVsRvOwZnGezautqDr5wGvZ8pTsMVvSGhs6IPkUkibxKR2sdl6gjSCjoOgom720itSGqHIccEZ-totIfuU1anFrJmxWiEU3qdCxLR3mIZXaVAI4VJ0W_HSUgyF8PhKnzJEbfHH9ajfbenKSBX1p9fkepYK0Ml5s5AmUR7qhpFM5SCo8jVEVvnxfjUsuMGFDxZSsbADc6F-NLfzWRCKiVX4Mg6qQQ"},"tenantId":null,"uid":"nCWme38Lp1bmatQ57vyTmYENmfG3","_redirectEventId":null}"""

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
    
    def test_visuallizacao_de_ranking_no_quiz(self):
        """Testa o acesso à resultados do Quiz."""
        print("Acessando o ranking do Quiz...")
        
        XPATH_BOTAO_VER_CURSO = "//h6[normalize-space(text())='Curso Grupo 4 sem PIN']/ancestor::div[contains(@class, 'MuiCard-root')]//button[text()='Ver Curso']"
        XPATH_RESULTADO_ALUNO = "//button[@title='Ver resultados dos estudantes']"
        XPATH_BOTAO_FECHAR = "//button[text()='Fechar']"
        try: 
            curso_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section[2]/div[2]/div/div[1]/div/div[2]/div/a[2]'))
            )
            curso_link.click()
            
            cursos_concluidos = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div/div/button[3]'))
            )
            cursos_concluidos.click()
            
            botao_comecar_curso = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_VER_CURSO))
            )
            botao_comecar_curso.click()
            
            botao_fechar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_FECHAR))
            )
            botao_fechar.click()
            time.sleep(2)
            
            botao_resultados_aluno = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_RESULTADO_ALUNO))
            )
            botao_resultados_aluno.click()  
            time.sleep(2)
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
            time.sleep(2)

            self.wait.until(EC.url_contains("/studentDashboard"))
            
        except Exception as e:
            self.fail(f"Falha ao acessar os resultados do quiz: {e}")
        print("Teste de acesso aos resultados do Quiz concluído com sucesso.")
    
    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            time.sleep(10)
            self.driver.quit() 

if __name__ == "__main__":
    unittest.main()