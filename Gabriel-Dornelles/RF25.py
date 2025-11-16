import unittest
import time
import os
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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"
FIREBASE_DOMAIN = "https://react-na-pratica.firebaseapp.com/"

FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''


class RF25(unittest.TestCase):
    def setUp(self):
        # Prefer Chrome. HEADLESS configurable via env var HEADLESS
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
            # Fallback to Firefox
            firefox_service = FirefoxService(GeckoDriverManager().install())
            firefox_options = FirefoxOptions()
            if headless_env in ('1', 'true', 'yes'):
                firefox_options.add_argument("--headless=new")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-gpu")
            self.driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)

        # 1) ABRIR O DOMÍNIO CORRETO = o Firebase Hosting
        print("Abrindo domínio real do app (Firebase Hosting)...")
        self.driver.get(FIREBASE_DOMAIN)
        time.sleep(2)

        # 2) LIMPAR localStorage
        self.driver.execute_script("window.localStorage.clear();")
        time.sleep(1)

        print("Injetando usuário no DOMÍNIO CORRETO...")
        # 3) INJETAR O FIREBASE LOGIN
        try:
            self.driver.execute_script(
                "window.localStorage.setItem(arguments[0], arguments[1]);",
                FIREBASE_KEY,
                FIREBASE_VALUE,
            )
        except Exception as e:
            print("Falha ao injetar FIREBASE:", e)
            raise

        # 4) DAR REFRESH PARA O APP LER O LOGIN
        self.driver.refresh()
        time.sleep(4)

        # 5) SÓ AGORA VÁ PARA O SITE TESTES
        print("Redirecionando para o site testes.codefolio.com.br...")
        self.driver.get(URL_BASE)
        time.sleep(3)

    def tearDown(self):
        try:
            self.driver.save_screenshot(f"resultado_{self.id()}.png")
        except Exception:
            pass
        self.driver.quit()

    # ---- TESTE ----
    def test_login(self):
        print("Abrindo domínio de testes já logado...")
        self.driver.get(URL_BASE)
        time.sleep(2)

        # Valida se carregou como logado (exemplo: foto do usuário/logado)
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//img[contains(@src,'googleusercontent')]")
                )
            )
            print("LOGIN RECONHECIDO NO SITE. OK!")
        except Exception:
            self.fail("O site NÃO reconheceu o login mesmo após injeção.")


if __name__ == "__main__":
    unittest.main()