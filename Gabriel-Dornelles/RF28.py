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
from selenium.webdriver.common.keys import Keys
import traceback

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

# --- SUAS CREDENCIAIS DO FIREBASE ---
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''



class TestRF28EscolhaAlternativaCorreta(unittest.TestCase):

    def setUp(self):
        # Prefer Firefox. HEADLESS configurable via env var HEADLESS (true/1/yes)
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

    def test_atribuicao_notas(self):
        """Requisito: Atribuição de notas — como professor, acessar avaliações, abrir correção e atribuir nota."""
        driver = self.driver
        wait = self.wait

        try:
            print("Navegando para 'Minhas Avaliações'...")
            try:
                driver.get(URL_BASE + "minhas-avaliacoes")
                wait.until(EC.url_contains("/minhas-avaliacoes"))
            except Exception:
                # fallback: ir para listcurso e abrir primeiro curso
                driver.get(URL_BASE + "listcurso")
                time.sleep(1)
                try:
                    first_acessar = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]"))
                    )
                    try:
                        driver.execute_script("arguments[0].click();", first_acessar)
                    except Exception:
                        first_acessar.click()
                    time.sleep(1)
                    # tentar navegar para minhas-avaliacoes via topbar
                    try:
                        aval = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Avaliações') or contains(., 'Avaliação') or @href='/minhas-avaliacoes']"))
                        )
                        driver.execute_script("arguments[0].click();", aval)
                        wait.until(EC.url_contains("/minhas-avaliacoes"))
                    except Exception:
                        pass
                except Exception:
                    pass

            print("Página de avaliações carregada (ou tentativa feita)")

            # localizar o card do curso
            course_title = "Curso Teste - Frederico Barcelos"
            print(f"Procurando curso: {course_title}")
            course_card_xpath = f"//h5[normalize-space()='{course_title}']"
            wait.until(EC.presence_of_element_located((By.XPATH, course_card_xpath)))

            # expandir avaliações
            try:
                expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//h5[normalize-space()='" + course_title + "']/ancestor::div[contains(@class, 'MuiCard-root')]//button[contains(@class, 'MuiAccordionSummary-root')]")))
                driver.execute_script("arguments[0].click();", expand_button)
            except Exception:
                header = driver.find_element(By.XPATH, course_card_xpath)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
                driver.execute_script("arguments[0].click();", header)

            # aguardar a avaliação específica
            evaluation_title = "Teste 1"
            eval_locator = (By.XPATH, "//div[contains(@class,'MuiCollapse-entered')]//p[normalize-space()='" + evaluation_title + "']")
            wait.until(EC.visibility_of_element_located(eval_locator))
            print(f"Avaliação '{evaluation_title}' encontrada e visível")

            # helper robusto para clicar
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
                        try:
                            from selenium.webdriver import ActionChains
                            ActionChains(driver).move_to_element(el).click().perform()
                            return
                        except Exception:
                            raise

            # localizar botão de correção/avaliar
            grading_selectors = [
                (By.XPATH, "//button[normalize-space()='Corrigir']"),
                (By.XPATH, "//button[contains(., 'Avaliar') or contains(., 'Corrigir')]") ,
                (By.XPATH, "//a[contains(., 'Ver tentativas') or contains(., 'Ver Tentativas')]"),
            ]

            grading_button = None
            for by, sel in grading_selectors:
                try:
                    grading_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
                    break
                except Exception:
                    continue

            if not grading_button:
                # salvar debug e falhar
                ts = int(time.time())
                try:
                    with open(f"debug_page_source_rf28_atribuicao_{ts}.html", 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                except Exception:
                    pass
                try:
                    driver.save_screenshot(f"debug_screenshot_rf28_atribuicao_{ts}.png")
                except Exception:
                    pass
                self.fail('Não foi possível encontrar o botão de correção/avaliação para o curso.')

            # clicar no botão de correção
            try:
                robust_click(grading_button)
            except Exception as e:
                traceback.print_exc()
                self.fail(f'Falha ao clicar no botão de correção: {e}')

            time.sleep(2)

            # abrir primeira tentativa
            try:
                first_attempt = None
                possible_attempts = [
                    (By.XPATH, "(//button[contains(., 'Corrigir') or contains(., 'Avaliar')])[1]"),
                    (By.XPATH, "(//a[contains(., 'Corrigir') or contains(., 'Avaliar')])[1]")
                ]
                for locator in possible_attempts:
                    try:
                        first_attempt = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(locator))
                        break
                    except Exception:
                        continue

                if not first_attempt:
                    first_attempt = driver.find_element(By.XPATH, "(//table//tr//button|//table//tr//a)[1]")

                driver.execute_script("arguments[0].click();", first_attempt)
            except Exception as e:
                traceback.print_exc()
                self.fail(f'Não foi possível abrir a primeira tentativa para correção: {e}')

            # localizar campo de nota e atribuir
            try:
                note_input = None
                note_selectors = [
                    (By.XPATH, "//input[@type='number' and (contains(@name,'grade') or contains(@placeholder,'Nota'))]"),
                    (By.XPATH, "//input[contains(@placeholder,'Nota') or contains(@aria-label,'Nota')]")
                ]
                for by, sel in note_selectors:
                    try:
                        note_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((by, sel)))
                        break
                    except Exception:
                        continue

                if not note_input:
                    note_input = driver.find_element(By.XPATH, "//div[contains(@class,'correction') or contains(@class,'grading')]//input")

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", note_input)
                note_input.clear()
                note_input.send_keys('8.5')

                # salvar/enviar nota
                saved = False
                save_selectors = [
                    (By.XPATH, "//button[normalize-space()='Salvar']"),
                    (By.XPATH, "//button[contains(., 'Salvar') or contains(., 'Enviar nota') or contains(., 'Enviar')]"),
                ]
                for by, sel in save_selectors:
                    try:
                        btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
                        driver.execute_script("arguments[0].click();", btn)
                        saved = True
                        break
                    except Exception:
                        continue

                if not saved:
                    note_input.send_keys(Keys.ENTER)

                time.sleep(2)

                # verificar confirmação simples
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(., '8.5') or contains(., 'Nota') or contains(., 'nota')]") ))
                    print("Nota atribuída — confirmação encontrada.")
                except Exception:
                    ts = int(time.time())
                    try:
                        with open(f"debug_page_source_rf28_after_grade_{ts}.html", 'w', encoding='utf-8') as f:
                            f.write(driver.page_source)
                    except Exception:
                        pass
                    try:
                        driver.save_screenshot(f"debug_screenshot_rf28_after_grade_{ts}.png")
                    except Exception:
                        pass
                    self.fail('Não foi possível confirmar visualmente que a nota foi atribuída.')

            except Exception as e:
                traceback.print_exc()
                self.fail(f'Erro ao atribuir nota: {e}')

            print('Fluxo de atribuição de notas em RF28 executado com sucesso.')

        except Exception as e:
            traceback.print_exc()
            self.fail(f'Erro geral no teste de atribuição de notas (RF28): {e}')

if __name__ == "__main__":
    unittest.main()
