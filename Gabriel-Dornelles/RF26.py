# RF26.py - Seleção Aleatória de Estudante
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

TIMEOUT = 20
URL_BASE = "https://testes.codefolio.com.br/"
FIREBASE_DOMAIN = "https://react-na-pratica.firebaseapp.com/"

FIREBASE_KEY = "firebase:authUser:5Jj2OvuSvubRzgdAZdNS3sDNE003:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''


class TestRF26SelecaoAleatoria(unittest.TestCase):

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

    # 🔥 RF26 – Sortear aluno
    def test_rf26_selecao_aleatoria(self):
        print("\n=== RF26 – Seleção Aleatória de Estudante ===")

        # Tentar rotas/entradas onde o botão de sortear pode estar
        tried_routes = []

        def try_navigate_routes():
            # 1) Ir direto para minhas-avaliacoes
            try:
                self.driver.get(URL_BASE + "minhas-avaliacoes")
                time.sleep(1)
                tried_routes.append("/minhas-avaliacoes")
                return
            except Exception:
                pass

            # 2) Ir para listcurso e tentar abrir o primeiro curso
            try:
                self.driver.get(URL_BASE + "listcurso")
                time.sleep(1)
                tried_routes.append("/listcurso")
                try:
                    first_acessar = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]"))
                    )
                    try:
                        self.driver.execute_script("arguments[0].click();", first_acessar)
                    except Exception:
                        first_acessar.click()
                    time.sleep(1)
                    return
                except Exception:
                    pass
            except Exception:
                pass

            # 3) Tentar ir ao dashboard e clicar em 'Avaliações' no topbar
            try:
                self.driver.get(URL_BASE + "dashboard")
                time.sleep(1)
                tried_routes.append("/dashboard")
                try:
                    aval = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Avaliações') or contains(., 'Avaliação')]")
                    )
                    )
                    try:
                        self.driver.execute_script("arguments[0].click();", aval)
                    except Exception:
                        aval.click()
                    time.sleep(1)
                    return
                except Exception:
                    pass
            except Exception:
                pass

        try:
            try_navigate_routes()

            # Lista de seletores possíveis para o botão de sortear
            sortear_selectors = [
                (By.XPATH, "//button[contains(., 'Sortear estudante') or contains(., 'Sortear aluno') or contains(., 'Sortear') ]"),
                (By.XPATH, "//button[contains(., 'Sorteio') or contains(., 'Sortear') ]"),
                (By.XPATH, "//a[contains(., 'Sortear') ]"),
                (By.CSS_SELECTOR, "button[data-testid*='sortear'], button.sortear, .btn-sortear"),
            ]

            btn_sortear = None
            for by, sel in sortear_selectors:
                try:
                    btn_sortear = WebDriverWait(self.driver, 8).until(
                        EC.element_to_be_clickable((by, sel))
                    )
                    if btn_sortear:
                        break
                except Exception:
                    continue

            if not btn_sortear:
                # salvar debug
                ts = int(time.time())
                try:
                    html_path = f"debug_page_source_rf26_fail_{ts}.html"
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                    print(f"Página salva em: {html_path}")
                except Exception as se:
                    print("Falha ao salvar page_source:", se)
                try:
                    ss_path = f"debug_screenshot_rf26_fail_{ts}.png"
                    self.driver.save_screenshot(ss_path)
                    print(f"Screenshot salva em: {ss_path}")
                except Exception as se:
                    print("Falha ao salvar screenshot:", se)

                self.fail(f"Falha ao localizar o botão de sorteio. Rotas tentadas: {tried_routes}")

            # Clicar no botão de sorteio
            try:
                self.driver.execute_script("arguments[0].click();", btn_sortear)
            except Exception:
                btn_sortear.click()

            time.sleep(2)

            # Verificar se algum aluno foi exibido como sorteado
            aluno_sorteado = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sorteado') or contains(@class,'estudante-sorteado')]")
            )
            )

            nome = aluno_sorteado.text.strip()
            print(f"Aluno sorteado: {nome}")

            self.assertTrue(len(nome) > 0, "Nenhum aluno foi sorteado!")

        except TimeoutException as e:
            ts = int(time.time())
            try:
                html_path = f"debug_page_source_rf26_fail_{ts}.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print(f"Página salva em: {html_path}")
            except Exception as se:
                print("Falha ao salvar page_source:", se)
            try:
                ss_path = f"debug_screenshot_rf26_fail_{ts}.png"
                self.driver.save_screenshot(ss_path)
                print(f"Screenshot salva em: {ss_path}")
            except Exception as se:
                print("Falha ao salvar screenshot:", se)
            self.fail("Falha ao selecionar aluno aleatoriamente — elemento não encontrado.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
