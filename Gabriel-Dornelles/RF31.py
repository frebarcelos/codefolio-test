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
FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438492669","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1765251419562","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1MTg5MTkxMTA3NjA1NDM0NGUxNWUyNTY0MjViYjQyNWVlYjNhNWMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBEb3JuZWxsZXMgZG9zIFNhbnRvcyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLLVRpeW93LXBINVlMWkFiQjlybjQ0OHlzTkY3WGdPTjJCSFBpakpXR3JBV09LU0E9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdGVzLWNvZGVmb2xpbyIsImF1ZCI6InRlc3Rlcy1jb2RlZm9saW8iLCJhdXRoX3RpbWUiOjE3NjUyNTE0MTksInVzZXJfaWQiOiJ4bDF5dGh5MXQwZkVmeTUwaVBzeVpaZ0NYV1AyIiwic3ViIjoieGwxeXRoeTF0MGZFZnk1MGlQc3laWmdDWFdQMiIsImlhdCI6MTc2NTI1MTQxOSwiZXhwIjoxNzY1MjU1MDE5LCJlbWFpbCI6ImdhYnJpZWxkb3JuZWxsZXMuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDkxNzI5ODY2NzIxMTY0NzY2MTIiXSwiZW1haWwiOlsiZ2FicmllbGRvcm5lbGxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.clAo078xMikQiKPrecLA00fsyl0fo78vtV4GRlBVddfIrluEvCb-tBXXrOAJHxxTbWs8QJmkFe2Z8uz5NWJU4A_xSRRZ6d_QCFKGSoBYsN9cTcwCH_Cr5VkXlAvrR5WUIJEGlaZVN0I-Xh16IRwoulvvDpILEcDfW7zORRb7hLQjv8_6IXfcfBPpKn0TLXgCRSQAJ79C_SRkxo3vmIi77gMjjfdYQVEEkSqNQN8cBcWGWc7X7G6DsNIfePJOeBEz-EolFgpKiIqnT-wHWgALNZT7RCDdGlz0fVvofrEdrmjeHW1w_D9wRkkUO0ywjjYevVgaWScWG4PUKy47G6ehYw","expirationTime":1765255334013,"refreshToken":"AMf-vBzNg3a_AOOdTUcOG12ZVrL5FSCj7y1CLqkkfsL3SZbWMf9_lK_10_NYB9vY_wO1tqP4LgHh5kdSMu4LJE2UWRo1cr22vjlJ_u7QmntDar9YIe9CSEsE-d1vOVpM0IwRwseRcbTzLRuTQT3Hqh-2EjNq_7sYSD0Qplf5pgwxDNJnSMrcNAXYbUMDjZtG2ibXvEicP-Q9pvR4bRcG1QoroXSUYKo24u0U-T5SUDhE0k6kXNPaoy2a_MLThv3TkxXqB1t2yKW6MYmxRa75574IR4e7M2sLskI9p5oQNouxPJI6dOR2yU4KI_FIIzZJQNxyYkUvDCHvcxXhN2-HJdXAiSIu_EPZMwg_i2XlkM4GIqkPD1-uFjvtVPOsI87IOQRe81_UpeTVvHn2br3b0zy8ahWkbPj1qNr0ku2C5_3l2kHxv_QaCKZFRouVRsiW9sfBaEZNHlJqsRxNB1Eqn50clHJeuw2bUrRXzptKdEdjdkx56t4wCho","tenantId":null,"uid":"xl1ythy1t0fEfy50iPsyZZgCXWP2","_redirectEventId":null}'''


class TestRF31PerguntasPersonalizadas(unittest.TestCase):

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

    def test_perguntas_personalizadas(self):
        """Abre a área de perguntas personalizadas e valida que existe pelo menos uma pergunta/elemento de edição."""
        driver = self.driver
        wait = self.wait

        # Inject login on Firebase hosting domain so the app recognizes the session
        driver.get("https://react-na-pratica.firebaseapp.com/")
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

            # procurar link/menu de Perguntas Personalizadas
            selectors = [
                (By.XPATH, "//a[contains(., 'Perguntas') or contains(., 'Pergunta')]"),
                (By.XPATH, "//button[contains(., 'Perguntas personalizadas') or contains(., 'Perguntas Personalizadas')]")
            ]
            found = False
            for by, sel in selectors:
                try:
                    menu = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((by, sel)))
                    robust_click(menu)
                    found = True
                    break
                except Exception:
                    continue

            if not found:
                ts = int(time.time())
                with open(f"debug_page_source_rf31_no_menu_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f"debug_screenshot_rf31_no_menu_{ts}.png")
                self.fail('Menu de Perguntas Personalizadas não encontrado')

            time.sleep(1)

            # verificar existência de pelo menos uma pergunta/listagem
            try:
                q = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'question') or //li[contains(., 'Pergunta')]]")))
                self.assertTrue(q is not None)
            except Exception:
                # fallback: procurar títulos/labels
                try:
                    q2 = driver.find_element(By.XPATH, "//h4[contains(., 'Pergunta') or contains(., 'Personalizada')]")
                    self.assertTrue(q2 is not None)
                except Exception:
                    ts = int(time.time())
                    with open(f"debug_page_source_rf31_no_questions_{ts}.html", 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    driver.save_screenshot(f"debug_screenshot_rf31_no_questions_{ts}.png")
                    self.fail('Nenhuma pergunta personalizada visível')

            print('RF31 - Área de perguntas personalizadas acessada e validada com sucesso.')

        except Exception as e:
            traceback.print_exc()
            ts = int(time.time())
            try:
                with open(f"debug_page_source_rf31_error_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
            except Exception:
                pass
            try:
                driver.save_screenshot(f"debug_screenshot_rf31_error_{ts}.png")
            except Exception:
                pass
            self.fail(f'Erro no teste RF31: {e}')


if __name__ == '__main__':
    unittest.main()
