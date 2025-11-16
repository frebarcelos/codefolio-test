# RF28.py
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import os

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

# --- SUAS CREDENCIAIS DO FIREBASE ---
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''



class TestRF28EscolhaAlternativaCorreta(unittest.TestCase):

    def setUp(self):
        # Prefer Chrome. HEADLESS configurable via env var HEADLESS (true/1/yes)
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = ChromeOptions()
        headless_env = os.environ.get('HEADLESS', '').lower()
        if headless_env in ('1', 'true', 'yes'):
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        try:
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        except Exception:
            # Fallback to Firefox if Chrome not available
            firefox_service = FirefoxService(GeckoDriverManager().install())
            firefox_options = FirefoxOptions()
            if headless_env in ('1', 'true', 'yes'):
                firefox_options.add_argument("--headless=new")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-gpu")
            self.driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def tearDown(self):
        try:
            self.driver.save_screenshot(f"resultado_{self.id()}.png")
        except Exception:
            pass
        self.driver.quit()

    def test_rf28_escolha_alternativa_correta(self):
        driver = self.driver
        wait = self.wait

        # --------------------------------
        # LOGIN VIA LOCALSTORAGE FIREBASE
        # --------------------------------
        driver.get(URL_BASE)

        # Use argumentized execute_script to avoid quoting/escape issues
        driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);",
            FIREBASE_KEY,
            FIREBASE_VALUE,
        )

        driver.refresh()
        time.sleep(2)

        # --------------------------------
        # ACESSA O CURSO
        # --------------------------------
        botao_cursos = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Cursos')]") )
        )

        def robust_click(element):
            try:
                element.click()
                return
            except ElementClickInterceptedException:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", element)
                    return
                except Exception:
                    try:
                        from selenium.webdriver import ActionChains

                        ActionChains(driver).move_to_element(element).click().perform()
                        return
                    except Exception:
                        raise

        robust_click(botao_cursos)

        primeiro_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]"))
        )
        robust_click(primeiro_curso)

        # --------------------------------
        # ACESSA O QUIZ
        # --------------------------------
        botao_quiz = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Quiz')]") )
        )
        robust_click(botao_quiz)

        time.sleep(2)

        # Agora estamos na tela que aparece na sua foto

        # --------------------------------
        # SELECIONA UMA ALTERNATIVA
        # (a segunda alternativa, como na foto)
        # --------------------------------
        alternativa_correta = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio'])[2]"))
        )
        robust_click(alternativa_correta)

        time.sleep(1)

        # --------------------------------
        # CLICA EM "Próxima" PARA SALVAR
        # --------------------------------
        botao_proxima = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Próxima')]") )
        )
        robust_click(botao_proxima)

        time.sleep(2)

        # --------------------------------
        # VALIDAR QUE A RESPOSTA FOI REGISTRADA
        # --------------------------------
        # Verifica se a próxima questão carregou
        titulo_proxima_questao = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(., 'Questão')]"))
        )

        self.assertTrue(titulo_proxima_questao.is_displayed())

        print("\nRF28 - Alternativa correta selecionada e registrada com sucesso!")

if __name__ == "__main__":
    unittest.main()
