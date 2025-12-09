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
 

# Reuse the same firebase key/value used across RFxx (adjust tokens if needed)
FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438492669","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1765251419562","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1MTg5MTkxMTA3NjA1NDM0NGUxNWUyNTY0MjViYjQyNWVlYjNhNWMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBEb3JuZWxsZXMgZG9zIFNhbnRvcyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLLVRpeW93LXBINVlMWkFiQjlybjQ0OHlzTkY3WGdPTjJCSFBpakpXR3JBV09LU0E9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdGVzLWNvZGVmb2xpbyIsImF1ZCI6InRlc3Rlcy1jb2RlZm9saW8iLCJhdXRoX3RpbWUiOjE3NjUyNTE0MTksInVzZXJfaWQiOiJ4bDF5dGh5MXQwZkVmeTUwaVBzeVpaZ0NYV1AyIiwic3ViIjoieGwxeXRoeTF0MGZFZnk1MGlQc3laWmdDWFdQMiIsImlhdCI6MTc2NTI1MTQxOSwiZXhwIjoxNzY1MjU1MDE5LCJlbWFpbCI6ImdhYnJpZWxkb3JuZWxsZXMuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDkxNzI5ODY2NzIxMTY0NzY2MTIiXSwiZW1haWwiOlsiZ2FicmllbGRvcm5lbGxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.clAo078xMikQiKPrecLA00fsyl0fo78vtV4GRlBVddfIrluEvCb-tBXXrOAJHxxTbWs8QJmkFe2Z8uz5NWJU4A_xSRRZ6d_QCFKGSoBYsN9cTcwCH_Cr5VkXlAvrR5WUIJEGlaZVN0I-Xh16IRwoulvvDpILEcDfW7zORRb7hLQjv8_6IXfcfBPpKn0TLXgCRSQAJ79C_SRkxo3vmIi77gMjjfdYQVEEkSqNQN8cBcWGWc7X7G6DsNIfePJOeBEz-EolFgpKiIqnT-wHWgALNZT7RCDdGlz0fVvofrEdrmjeHW1w_D9wRkkUO0ywjjYevVgaWScWG4PUKy47G6ehYw","expirationTime":1765255334013,"refreshToken":"AMf-vBzNg3a_AOOdTUcOG12ZVrL5FSCj7y1CLqkkfsL3SZbWMf9_lK_10_NYB9vY_wO1tqP4LgHh5kdSMu4LJE2UWRo1cr22vjlJ_u7QmntDar9YIe9CSEsE-d1vOVpM0IwRwseRcbTzLRuTQT3Hqh-2EjNq_7sYSD0Qplf5pgwxDNJnSMrcNAXYbUMDjZtG2ibXvEicP-Q9pvR4bRcG1QoroXSUYKo24u0U-T5SUDhE0k6kXNPaoy2a_MLThv3TkxXqB1t2yKW6MYmxRa75574IR4e7M2sLskI9p5oQNouxPJI6dOR2yU4KI_FIIzZJQNxyYkUvDCHvcxXhN2-HJdXAiSIu_EPZMwg_i2XlkM4GIqkPD1-uFjvtVPOsI87IOQRe81_UpeTVvHn2br3b0zy8ahWkbPj1qNr0ku2C5_3l2kHxv_QaCKZFRouVRsiW9sfBaEZNHlJqsRxNB1Eqn50clHJeuw2bUrRXzptKdEdjdkx56t4wCho","tenantId":null,"uid":"xl1ythy1t0fEfy50iPsyZZgCXWP2","_redirectEventId":null}'''


class TestRF30ExibicaoRespostas(unittest.TestCase):

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

    def test_exibicao_respostas(self):
        """Verifica se, após responder/avançar, existe a opção/área de exibição de respostas."""
        driver = self.driver
        wait = self.wait

        # LOGIN (injetar no domínio do Firebase Hosting, depois ir para o app)
        driver.get("https://react-na-pratica.firebaseapp.com/")
        time.sleep(1)
        driver.execute_script("window.localStorage.clear();")
        time.sleep(0.5)
        driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", FIREBASE_KEY, FIREBASE_VALUE)
        driver.refresh()
        time.sleep(2)
        driver.get(URL_BASE)
        time.sleep(1)

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
            botao_cursos = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Cursos') or contains(., 'Cursos')]") ))
            robust_click(botao_cursos)
            time.sleep(1)

            # clicar na aba 'Em Andamento' para ver cursos em progresso (busca case-insensitive)
            try:
                aba_xpath = ("//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'em andamento')]"
                             " | //a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'em andamento')]"
                             " | //div[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'em andamento')]")
                aba_andamento = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, aba_xpath)))
                robust_click(aba_andamento)
                time.sleep(1)
            except Exception:
                # se não houver aba ou não for necessário, prossegue
                pass

            # procurar o curso específico por título parcial
            course_title = 'Curso técnico de ES powered by GPT-'
            primeiro_curso = None
            try:
                # localizar elemento que contenha o título do curso (qualquer elemento que contenha o texto)
                title_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(., '{course_title}')]") ))
                # subir para o container do curso (ancestro que contenha um botão)
                try:
                    container = title_el.find_element(By.XPATH, "ancestor::div[.//button][1]")
                except Exception:
                    container = title_el
                # dentro do container, procurar botão de entrar/começar/acessar
                try:
                    btn = container.find_element(By.XPATH, ".//button[contains(., 'Começar') or contains(., 'Acessar') or contains(., 'Entrar')]")
                    primeiro_curso = btn
                    robust_click(primeiro_curso)
                except Exception:
                    # fallback: clicar primeiro botão disponível no container
                    try:
                        btn2 = container.find_element(By.XPATH, ".//button")
                        primeiro_curso = btn2
                        robust_click(primeiro_curso)
                    except Exception:
                        primeiro_curso = None
            except Exception:
                primeiro_curso = None

            # se não encontrou o curso específico, tentar os seletores globais (primeiro curso na lista)
            if primeiro_curso is None:
                course_selectors = [
                    (By.XPATH, "(//button[contains(., 'Acessar')])[1]"),
                    (By.XPATH, "(//button[contains(., 'Começar')])[1]"),
                    (By.XPATH, "(//button[contains(., 'Entrar')])[1]")
                ]
                for by, sel in course_selectors:
                    try:
                        primeiro_curso = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
                        robust_click(primeiro_curso)
                        break
                    except Exception:
                        continue
            if primeiro_curso is None:
                ts = int(time.time())
                with open(f"debug_page_source_rf30_no_course_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f"debug_screenshot_rf30_no_course_{ts}.png")
                self.fail('Botão de acesso/começo do curso não encontrado')

            botao_quiz = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Quiz')]") ))
            robust_click(botao_quiz)

            # responder (selecionar primeira alternativa) e avançar
            answered = False
            # tentativa 1: input radio/checkbox genérico (antigo)
            try:
                alt = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio' or @type='checkbox'])[1]")))
                robust_click(alt)
                answered = True
            except Exception:
                pass

            # tentativa 2: input radio com value 0 (ex.: opção 'sim') — clicar no label pai para evitar inputs ocultos
            if not answered:
                try:
                    inp = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='radio' and @value='0'])[1]")))
                    try:
                        label = inp.find_element(By.XPATH, "ancestor::label[1]")
                        robust_click(label)
                    except Exception:
                        robust_click(inp)
                    answered = True
                except Exception:
                    pass

            # tentativa 3: localizar label que contenha o texto 'sim' (variações de caixa) e clicar nele
            if not answered:
                try:
                    # procura label cujo filho div contenha o texto 'sim' (case-insensitive aproximado)
                    labels = driver.find_elements(By.XPATH, "//label[.//div and (contains(translate(normalize-space(.//div/text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sim'))]")
                    if labels:
                        robust_click(labels[0])
                        answered = True
                except Exception:
                    pass

            if not answered:
                # fallback: salva debug para inspecionar
                ts = int(time.time())
                with open(f"debug_page_source_rf30_no_answer_{ts}.html", 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f"debug_screenshot_rf30_no_answer_{ts}.png")
                # não falhar o teste aqui — prosseguimos para tentar avançar e detectar ausência mais adiante

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
