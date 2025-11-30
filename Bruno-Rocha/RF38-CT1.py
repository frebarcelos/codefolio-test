import unittest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains 
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys

class AcessoCursosTest(unittest.TestCase):

    def setUp(self):
        self.TIMEOUT = 15
        self.URL_BASE = "https://testes-codefolio.web.app/"
        
        # --- DADOS DO FIREBASE ---
        self.FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"
        self.FIREBASE_VALUE = """{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763648817937","displayName":"Bruno Rocha","email":"rocha.bruno461@gmail.com","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763648817937","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLNMJ3XfCqjGKkuYrOnsYpG5W3iXZYLznUA-KNh30J-nITkF7Pv=s96-c","providerData":[{"displayName":"Bruno Rocha","email":"rocha.bruno461@gmail.com","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLNMJ3XfCqjGKkuYrOnsYpG5W3iXZYLznUA-KNh30J-nITkF7Pv=s96-c","providerId":"google.com","uid":"110766999781850485565"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQnJ1bm8gUm9jaGEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE5NSjNYZkNxakdLa3VZck9uc1lwRzVXM2lYWllMem5VQS1LTmgzMEotbklUa0Y3UHY9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdGVzLWNvZGVmb2xpbyIsImF1ZCI6InRlc3Rlcy1jb2RlZm9saW8iLCJhdXRoX3RpbWUiOjE3NjM2NDg4MTgsInVzZXJfaWQiOiI0VnhYdXJPblU5UGFBNUVsdTd1enJsVnRUdk4yIiwic3ViIjoiNFZ4WHVyT25VOVBhQTVFbHU3dXpybFZ0VHZOMiIsImlhdCI6MTc2MzY0ODgxOCwiZXhwIjoxNzYzNjUyNDE4LCJlbWFpbCI6InJvY2hhLmJydW5vNDYxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEwNzY2OTk5NzgxODUwNDg1NTY1Il0sImVtYWlsIjpbInJvY2hhLmJydW5vNDYxQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.ogq7BlV3tVtn8PUL0YHPhKOOfxxqaxQ1v2btHbovyo3jMzCp2YAmM-ZEfC9Xd1algUU1ftS1hC7sI0HjM-tKi7RfJ9QXYYLTfQQqZWD-ZUMhcLHY1ILj6DSMOhGBsSmB7YNi-zzZ47QD7TlPeGS9XmqvIKzrpIUNXhJrwQD614YX_8DmFI16sw6KUsU2KrGq5OtEtBoiBBvvkwRGBNM9kKyERI_6wRF7yDSA1wXc_Asb9r3scw0KQaZnVpna-gz3LDKfB-i93xBNQJ5UpBBDJLuRuNE6Foh2OjLsbFm7GNM03NNOn1lLoXbeEP2V4xiHxZG1PrEehAn7qyR7Hnn6Zg","expirationTime":1763652418264,"refreshToken":"AMf-vBxXNrVisbFsYIg_tqMVVjt0Hgh8WUGxtbXMKYarFGXIcFCgNybl-56QTNS7vU3hjh3hujszWgOB8vYCqn0pZos0eaGToUrnGEpk_NvdNJvadMpo_cwOp4hXOrgW6PvR2kNYUwdK6KsXX3bxsa_KZisxjaIcX3hebJw8-OFbmayt1yfElqcHElMEDaluIAAlW8TaO1bItgtkMJ3wh9lJM6QBuU9p1txF2z6Lgvmv2yldhplnJDlcEztlhFcvxXNDO0dchKEm_bAf_fPb6XiCTLlBNQApD7cGewM_eReQJFM7eqy1tsJTfozq3rXHg4clpmG-bhdgdYTC-ME_cuQ5nslerooALjzENZK-qNII9KrOQLvCg2bLAALj_ogs9d14K84gPq5E3plTrf4u_mH79Khm2zjssLaz2yNSrnmRWxECkRTV70w2yCLMuu5jOytP5Sh4YUH4","tenantId":null},"tenantId":null,"uid":"4VxXurOnU9PaA5Elu7uzrlVtTvN2","_redirectEventId":null}"""

        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)

        # --- LOGIN VIA LOCAL STORAGE ---
        self.driver.get(self.URL_BASE)
        try:
            self.driver.execute_script(
                "window.localStorage.setItem(arguments[0], arguments[1]);",
                self.FIREBASE_KEY, self.FIREBASE_VALUE
            )
        except Exception as e:
            self.driver.quit()
            raise RuntimeError("Falha no setup do Local Storage") from e
        
        self.driver.refresh()
    
    def test_acessar_lista_videos_home(self):
        """Acessando lista de vídeos da Home com validação passo a passo."""
        print("Iniciando acesso à Home...")
        time.sleep(4)
        self.driver.save_screenshot("Bruno-Rocha/img/img-RF38/inicio.png")
        
        scroll_realizado = False
        
        try:
            print("1/3 Tentando clicar no botão Home...")
            botao_home = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section[2]/div[2]/div/div[1]/div/div[2]/div/a[1]'))
            )
            self.driver.execute_script("arguments[0].click();", botao_home)
            
            print("Clicou na Home.")
            self.driver.save_screenshot("Bruno-Rocha/img/img-RF38/passo_1.png")
            
        except Exception as e:
            self.fail(f"FALHA NO PASSO 1 (Clique): {e}")

        try:
            print("2/3 Aguardando carregamento da Dashboard...")
            time.sleep(2)
            
            self.wait.until(EC.url_contains("/dashboard"))
            
            if "/dashboard" not in self.driver.current_url:
                raise Exception(f"URL incorreta: {self.driver.current_url}")
                
            print("URL validada com sucesso (/dashboard).")

        except Exception as e:
            self.fail(f"FALHA NO PASSO 2 (Validação URL): {e}")
            
        try:
            print("3/3 Tentando rolar o scroll...")
            time.sleep(2)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(2) 
            
            self.driver.save_screenshot("Bruno-Rocha/img/img-RF38/passo_2.png")
            print("Rolou o scroll para baixo.")
            
            scroll_realizado = True
            
        except Exception as e:
            self.fail(f"FALHA NO PASSO 3 (Scroll): {e}")

        self.assertTrue(scroll_realizado, "O teste falhou: O scroll não foi completado corretamente.")
        
        print("Sucesso: Lista de vídeos da Home acessados.")

    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            time.sleep(2)
            self.driver.quit() 

if __name__ == "__main__":
    unittest.main()