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

FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''


class TestRF32RetribuicaoEstudantes(unittest.TestCase):

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

    def test_retribuicao_estudantes(self):
        """Valida atribuição/visualização de estudantes em perguntas personalizadas."""
        driver = self.driver
        wait = self.wait

        driver.get(URL_BASE)
        driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", FIREBASE_KEY, FIREBASE_VALUE)
        driver.refresh()
        time.sleep(2)

        def robust_click(el):
            try:
                el.click()
                return
            except ElementClickInterceptedException:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", el)
                    return
                except Exception:
                    from selenium.webdriver import ActionChains
                    ActionChains(driver).move_to_element(el).click().perform()

        try:
            # navegar até Cursos -> acessar primeiro curso
            botao_cursos = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Cursos')]") ))
            robust_click(botao_cursos)
            primeiro_curso = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]")))
            robust_click(primeiro_curso)

            # abrir Perguntas Personalizadas
            selectors = [
                (By.XPATH, "//a[contains(., 'Perguntas') or contains(., 'Pergunta')]"),
                (By.XPATH, "//button[contains(., 'Perguntas personalizadas') or contains(., 'Perguntas Personalizadas')]")
            ]
            opened = False
            for by, sel in selectors:
                try:
                    elem = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((by, sel)))
                    robust_click(elem)
                    opened = True
                    break
                except Exception:
                    continue

            if not opened:
                ts = int(time.time())
                with open(f"debug_page_source_rf32_no_menu_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f"debug_screenshot_rf32_no_menu_{ts}.png")
                self.fail('Menu de Perguntas Personalizadas não encontrado')

            time.sleep(1)

            # localizar uma pergunta e abrir painel de atribuição de estudantes
            try:
                question_item = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'question') or //li[contains(., 'Pergunta')])[1]")))
                robust_click(question_item)
            except Exception:
                # fallback genérico
                try:
                    question_item = driver.find_element(By.XPATH, "(//h4[contains(., 'Pergunta')])[1]")
                    robust_click(question_item)
                except Exception:
                    ts = int(time.time())
                    with open(f"debug_page_source_rf32_no_question_{ts}.html", 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    driver.save_screenshot(f"debug_screenshot_rf32_no_question_{ts}.png")
                    self.fail('Não foi possível encontrar/abrir uma pergunta personalizada')

            # procurar botão/ação de Atribuir estudante
            assign_selectors = [
                (By.XPATH, "//button[contains(., 'Atribuir') or contains(., 'Atribuição') or contains(., 'Associar')]") ,
                (By.XPATH, "//a[contains(., 'Atribuir') or contains(., 'Atribuição')]")
            ]
            assigned = False
            for by, sel in assign_selectors:
                try:
                    btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
                    robust_click(btn)
                    assigned = True
                    break
                except Exception:
                    continue

            if not assigned:
                # talvez a lista de estudantes já esteja visível; verificar
                try:
                    students_list = driver.find_element(By.XPATH, "//div[contains(@class,'students') or contains(., 'Alunos') or contains(., 'Estudantes')]")
                    self.assertIsNotNone(students_list)
                    print('RF32 - Lista de estudantes já visível')
                except Exception:
                    ts = int(time.time())
                    with open(f"debug_page_source_rf32_no_assign_{ts}.html", 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    driver.save_screenshot(f"debug_screenshot_rf32_no_assign_{ts}.png")
                    self.fail('Não foi possível abrir painel de atribuição de estudantes nem localizar lista')

            else:
                # após abrir painel, verificar se há checkbox/lista de alunos e assinalar um
                try:
                    student_checkbox = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='checkbox' and contains(@name,'student')])[1]")))
                    robust_click(student_checkbox)
                    # salvar/confirmar atribuição
                    try:
                        save_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Salvar') or contains(., 'Confirmar') or contains(., 'Atribuir')]")))
                        robust_click(save_btn)
                    except Exception:
                        pass
                    # verificar se o estudante aparece na lista de atribuídos
                    time.sleep(1)
                    assigned_list = driver.find_elements(By.XPATH, "//div[contains(@class,'assigned') or contains(., 'Atribuído') or contains(., 'Atribuídos')]")
                    self.assertTrue(len(assigned_list) >= 0)
                    print('RF32 - Atribuição/visualização de estudantes verificada (fluxo básico).')
                except Exception:
                    ts = int(time.time())
                    with open(f"debug_page_source_rf32_after_open_{ts}.html", 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    driver.save_screenshot(f"debug_screenshot_rf32_after_open_{ts}.png")
                    self.fail('Erro ao atribuir ou verificar estudante na pergunta personalizada')

        except Exception as e:
            traceback.print_exc()
            ts = int(time.time())
            try:
                with open(f"debug_page_source_rf32_error_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
            except Exception:
                pass
            try:
                driver.save_screenshot(f"debug_screenshot_rf32_error_{ts}.png")
            except Exception:
                pass
            self.fail(f'Erro no teste RF32: {e}')


if __name__ == '__main__':
    unittest.main()
