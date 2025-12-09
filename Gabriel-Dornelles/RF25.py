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
from selenium.common.exceptions import ElementClickInterceptedException
import traceback

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"
FIREBASE_DOMAIN = "https://react-na-pratica.firebaseapp.com/"

FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''


class RF25(unittest.TestCase):
    def setUp(self):
        # Prefer Firefox. HEADLESS configurable via env var HEADLESS
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
            # Fallback to Chrome if Firefox not available
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = ChromeOptions()
            if headless_env in ('1', 'true', 'yes'):
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

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

    def test_atribuicao_notas(self):
        """Requisito: Atribuição de notas — como professor, acessar avaliações, abrir correção e atribuir nota."""
        driver = self.driver
        wait = self.wait

        try:
            print("Navegando para 'Minhas Avaliações'...")
            # tenta clicar no link de avaliações no topbar
            try:
                avaliacoes_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/minhas-avaliacoes']")))
                self.driver.execute_script("arguments[0].click();", avaliacoes_link)
            except Exception:
                # alternativa: botão ou item de menu com texto 'Avaliações'
                avaliacoes_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Avaliações') or contains(., 'Avaliacões') or //button[contains(., 'Avaliações')]]")))
                self.driver.execute_script("arguments[0].click();", avaliacoes_link)

            wait.until(EC.url_contains("/minhas-avaliacoes"))
            print("Página de avaliações carregada")

            # localizar o card do curso
            course_title = "Curso Teste - Frederico Barcelos"
            print(f"Procurando curso: {course_title}")
            course_card_xpath = f"//h5[normalize-space()='{course_title}']"
            wait.until(EC.presence_of_element_located((By.XPATH, course_card_xpath)))

            # expandir avaliações do curso
            try:
                expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//h5[normalize-space()='" + course_title + "']/ancestor::div[contains(@class, 'MuiCard-root')]//button[contains(@class, 'MuiAccordionSummary-root')]")))
                self.driver.execute_script("arguments[0].click();", expand_button)
            except Exception:
                print("Falha ao expandir via botão padrão, tentando click por JS no header do card...")
                header = self.driver.find_element(By.XPATH, course_card_xpath)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
                driver.execute_script("arguments[0].click();", header)

            # aguardar que a lista de avaliações seja visível
            evaluation_title = "Teste 1"
            eval_locator = (By.XPATH, "//div[contains(@class,'MuiCollapse-entered')]//p[normalize-space()='" + evaluation_title + "']")
            wait.until(EC.visibility_of_element_located(eval_locator))
            print(f"Avaliação '{evaluation_title}' encontrada e visível")

            # tentar encontrar botão de avaliar/corrigir/visualizar tentativas
            grading_selectors = [
                (By.XPATH, "//button[normalize-space()='Corrigir']"),
                (By.XPATH, "//button[contains(., 'Avaliar') or contains(., 'Corrigir')]") ,
                (By.XPATH, "//a[contains(., 'Ver tentativas') or contains(., 'Ver Tentativas')]") ,
                (By.XPATH, "//button[contains(., 'Ver Tentativas') or contains(., 'Ver tentativas')]")
            ]

            grading_button = None
            for by, sel in grading_selectors:
                try:
                    grading_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
                    break
                except Exception:
                    continue

            if not grading_button:
                # tenta localizar link dentro do bloco da avaliação
                try:
                    container = driver.find_element(By.XPATH, "//div[contains(@class,'MuiCollapse-entered')]")
                    grading_button = container.find_element(By.XPATH, ".//button|.//a")
                except Exception:
                    grading_button = None

            if not grading_button:
                # salvar debug e falhar
                page = driver.page_source
                with open('debug_page_source_atribuicao_notas.html', 'w', encoding='utf-8') as f:
                    f.write(page)
                driver.save_screenshot('debug_screenshot_atribuicao_notas.png')
                self.fail('Não foi possível encontrar o botão de correção/avaliação para o curso.')

            # clicar no botão de correção
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", grading_button)
                driver.execute_script("arguments[0].click();", grading_button)
            except Exception as e:
                print('Tentativa direta de click falhou:', e)
                try:
                    from selenium.webdriver import ActionChains
                    ActionChains(driver).move_to_element(grading_button).click().perform()
                except Exception as e2:
                    traceback.print_exc()
                    self.fail(f'Falha ao clicar no botão de correção: {e2}')

            # agora na página de listagem de tentativas / corretor
            time.sleep(2)

            # tentar abrir a primeira submissão/tentativa
            try:
                # procura por botões com 'Corrigir' ou 'Corrigir tentativa' no conteúdo
                first_attempt = None
                possible_attempts = [
                    (By.XPATH, "(//button[contains(., 'Corrigir') or contains(., 'Avaliar')])[1]"),
                    (By.XPATH, "(//a[contains(., 'Corrigir') or contains(., 'Avaliar')])[1]"),
                ]
                for locator in possible_attempts:
                    try:
                        first_attempt = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(locator))
                        break
                    except Exception:
                        continue

                if not first_attempt:
                    # tenta clicar no primeiro item da tabela de tentativas
                    first_attempt = driver.find_element(By.XPATH, "(//table//tr//button|//table//tr//a)[1]")

                driver.execute_script("arguments[0].click();", first_attempt)
            except Exception as e:
                traceback.print_exc()
                self.fail(f'Não foi possível abrir a primeira tentativa para correção: {e}')

            # aguardar editor/campo de nota aparecer
            try:
                # possíveis seletores para o campo de nota
                note_input_selectors = [
                    (By.XPATH, "//input[@type='number' and (@name='grade' or contains(@placeholder,'Nota'))]"),
                    (By.XPATH, "//input[contains(@placeholder,'Nota') or contains(@aria-label,'Nota')]") ,
                    (By.XPATH, "//input[@type='text' and contains(@placeholder,'Nota')]")
                ]
                note_input = None
                for by, sel in note_input_selectors:
                    try:
                        note_input = WebDriverWait(driver, 4).until(EC.presence_of_element_located((by, sel)))
                        break
                    except Exception:
                        continue

                if not note_input:
                    # tenta localizar qualquer input na área de correção
                    note_input = driver.find_element(By.XPATH, "//div[contains(@class,'correction') or contains(@class,'grading')]//input")

                # atribuir nota (exemplo: 8.5)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", note_input)
                note_input.clear()
                note_input.send_keys('8.5')
                time.sleep(0.5)

                # procurar botão salvar/enviar nota
                save_selectors = [
                    (By.XPATH, "//button[normalize-space()='Salvar']"),
                    (By.XPATH, "//button[contains(., 'Salvar') or contains(., 'Enviar nota') or contains(., 'Enviar')]"),
                ]
                saved = False
                for by, sel in save_selectors:
                    try:
                        btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
                        driver.execute_script("arguments[0].click();", btn)
                        saved = True
                        break
                    except Exception:
                        continue

                if not saved:
                    # fallback: tentar submeter com ENTER
                    note_input.send_keys(Keys.ENTER)

                time.sleep(2)

                # Verificar se a nota foi registrada: procurar por texto/label com 'Nota: 8.5' ou similar
                try:
                    confirmation = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(., '8.5') or contains(., 'Nota') or contains(., 'nota')]") ))
                    print("Nota atribuída — confirmação encontrada.")
                except Exception:
                    # salvar debug
                    with open('debug_page_source_after_grade.html', 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    driver.save_screenshot('debug_screenshot_after_grade.png')
                    self.fail('Não foi possível confirmar visualmente que a nota foi atribuída.')

            except Exception as e:
                traceback.print_exc()
                self.fail(f'Erro ao atribuir nota: {e}')

            print('Fluxo de atribuição de notas executado com sucesso (fluxo automático).')

        except Exception as e:
            traceback.print_exc()
            self.fail(f'Erro geral no teste de atribuição de notas: {e}')


if __name__ == "__main__":
    unittest.main()