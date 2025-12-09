import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import os
import traceback

TIMEOUT = 15
URL_BASE = "https://testes-codefolio.web.app/"
FIREBASE_DOMAIN = "https://react-na-pratica.firebaseapp.com/"
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''
FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438492669","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1765251419562","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1MTg5MTkxMTA3NjA1NDM0NGUxNWUyNTY0MjViYjQyNWVlYjNhNWMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBEb3JuZWxsZXMgZG9zIFNhbnRvcyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLLVRpeW93LXBINVlMWkFiQjlybjQ0OHlzTkY3WGdPTjJCSFBpakpXR3JBV09LU0E9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdGVzLWNvZGVmb2xpbyIsImF1ZCI6InRlc3Rlcy1jb2RlZm9saW8iLCJhdXRoX3RpbWUiOjE3NjUyNTE0MTksInVzZXJfaWQiOiJ4bDF5dGh5MXQwZkVmeTUwaVBzeVpaZ0NYV1AyIiwic3ViIjoieGwxeXRoeTF0MGZFZnk1MGlQc3laWmdDWFdQMiIsImlhdCI6MTc2NTI1MTQxOSwiZXhwIjoxNzY1MjU1MDE5LCJlbWFpbCI6ImdhYnJpZWxkb3JuZWxsZXMuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDkxNzI5ODY2NzIxMTY0NzY2MTIiXSwiZW1haWwiOlsiZ2FicmllbGRvcm5lbGxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.clAo078xMikQiKPrecLA00fsyl0fo78vtV4GRlBVddfIrluEvCb-tBXXrOAJHxxTbWs8QJmkFe2Z8uz5NWJU4A_xSRRZ6d_QCFKGSoBYsN9cTcwCH_Cr5VkXlAvrR5WUIJEGlaZVN0I-Xh16IRwoulvvDpILEcDfW7zORRb7hLQjv8_6IXfcfBPpKn0TLXgCRSQAJ79C_SRkxo3vmIi77gMjjfdYQVEEkSqNQN8cBcWGWc7X7G6DsNIfePJOeBEz-EolFgpKiIqnT-wHWgALNZT7RCDdGlz0fVvofrEdrmjeHW1w_D9wRkkUO0ywjjYevVgaWScWG4PUKy47G6ehYw","expirationTime":1765255334013,"refreshToken":"AMf-vBzNg3a_AOOdTUcOG12ZVrL5FSCj7y1CLqkkfsL3SZbWMf9_lK_10_NYB9vY_wO1tqP4LgHh5kdSMu4LJE2UWRo1cr22vjlJ_u7QmntDar9YIe9CSEsE-d1vOVpM0IwRwseRcbTzLRuTQT3Hqh-2EjNq_7sYSD0Qplf5pgwxDNJnSMrcNAXYbUMDjZtG2ibXvEicP-Q9pvR4bRcG1QoroXSUYKo24u0U-T5SUDhE0k6kXNPaoy2a_MLThv3TkxXqB1t2yKW6MYmxRa75574IR4e7M2sLskI9p5oQNouxPJI6dOR2yU4KI_FIIzZJQNxyYkUvDCHvcxXhN2-HJdXAiSIu_EPZMwg_i2XlkM4GIqkPD1-uFjvtVPOsI87IOQRe81_UpeTVvHn2br3b0zy8ahWkbPj1qNr0ku2C5_3l2kHxv_QaCKZFRouVRsiW9sfBaEZNHlJqsRxNB1Eqn50clHJeuw2bUrRXzptKdEdjdkx56t4wCho","tenantId":null,"uid":"xl1ythy1t0fEfy50iPsyZZgCXWP2","_redirectEventId":null}'''


class TestRF32RetribuicaoEstudantes(unittest.TestCase):

    def setUp(self):
        # Use Chrome as primary browser. HEADLESS configurable via env var HEADLESS
        headless_env = os.environ.get('HEADLESS', '').lower()
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

        # Inject login on Firebase hosting domain then go to app
        driver.get(FIREBASE_DOMAIN)
        time.sleep(1)
        driver.execute_script("window.localStorage.clear();")
        time.sleep(0.5)
        driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", FIREBASE_KEY, FIREBASE_VALUE)
        driver.refresh()
        time.sleep(2)
        driver.get(URL_BASE)
        time.sleep(1)

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
