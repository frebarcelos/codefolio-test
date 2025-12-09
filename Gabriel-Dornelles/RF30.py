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
import traceback

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

# Reuse the same firebase key/value used across RFxx (adjust tokens if needed)
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''


class TestRF30ExibicaoRespostas(unittest.TestCase):

    def setUp(self):
        firefox_service = FirefoxService(GeckoDriverManager().install())
        firefox_options = FirefoxOptions()
        headless_env = os.environ.get('HEADLESS', '').lower()
        if headless_env in ('1', 'true', 'yes'):
            firefox_options.add_argument("--headless=new")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-gpu")
        try:
            self.driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        except Exception:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = ChromeOptions()
            if headless_env in ('1', 'true', 'yes'):
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def tearDown(self):
        try:
            self.driver.save_screenshot(f"resultado_{self.id()}.png")
        except Exception:
            pass
        self.driver.quit()

    def test_exibicao_respostas(self):
        """Verifica se, após responder/avançar, existe a opção/área de exibição de respostas."""
        driver = self.driver
        wait = self.wait

        # LOGIN
        driver.get(URL_BASE)
        driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", FIREBASE_KEY, FIREBASE_VALUE)
        driver.refresh()
        time.sleep(2)

        def robust_click(elem):
            try:
                elem.click()
                return
            except ElementClickInterceptedException:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", elem)
                    return
                except Exception:
                    from selenium.webdriver import ActionChains
                    ActionChains(driver).move_to_element(elem).click().perform()

        try:
            botao_cursos = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Cursos')]") ))
            robust_click(botao_cursos)

            primeiro_curso = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]")))
            robust_click(primeiro_curso)

            botao_quiz = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Quiz')]") ))
            robust_click(botao_quiz)

            # responder (selecionar primeira alternativa) e avançar
            try:
                alt = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio' or @type='checkbox'])[1]")))
                robust_click(alt)
            except Exception:
                pass

            try:
                btn_prox = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Próxima') or contains(., 'Avançar') or contains(., 'Próximo')]") ))
                robust_click(btn_prox)
            except Exception:
                ts = int(time.time())
                with open(f"debug_page_source_rf30_no_next_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f"debug_screenshot_rf30_no_next_{ts}.png")
                self.fail('Botão Próxima não encontrado para avançar')

            time.sleep(1)

            # procura por botão/área de exibir respostas
            show_selectors = [
                (By.XPATH, "//button[contains(., 'Mostrar resposta') or contains(., 'Mostrar respostas') or contains(., 'Ver respostas')]") ,
                (By.XPATH, "//div[contains(., 'Respostas') or contains(., 'Resposta')]")
            ]
            found = False
            for by, sel in show_selectors:
                try:
                    el = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((by, sel)))
                    if el:
                        found = True
                        break
                except Exception:
                    continue

            if not found:
                ts = int(time.time())
                with open(f"debug_page_source_rf30_no_show_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f"debug_screenshot_rf30_no_show_{ts}.png")
                self.fail('Não foi encontrada a opção/área de exibição de respostas')

            print("RF30 - Exibição de respostas encontrada com sucesso.")

        except Exception as e:
            traceback.print_exc()
            ts = int(time.time())
            try:
                with open(f"debug_page_source_rf30_error_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
            except Exception:
                pass
            try:
                driver.save_screenshot(f"debug_screenshot_rf30_error_{ts}.png")
            except Exception:
                pass
            self.fail(f'Erro no teste RF30: {e}')


if __name__ == '__main__':
    unittest.main()
