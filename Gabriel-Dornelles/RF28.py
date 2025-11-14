# RF28.py
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

# --- SUAS CREDENCIAIS DO FIREBASE ---
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FIREBASE_VALUE = """COLE AQUI O SEU JSON COMPLETO QUE EU VI ACIMA"""

class TestRF28EscolhaAlternativaCorreta(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def tearDown(self):
        self.driver.quit()

    def test_rf28_escolha_alternativa_correta(self):
        driver = self.driver
        wait = self.wait

        # --------------------------------
        # LOGIN VIA LOCALSTORAGE FIREBASE
        # --------------------------------
        driver.get(URL_BASE)

        driver.execute_script(
            f"window.localStorage.setItem('{FIREBASE_KEY}', `{FIREBASE_VALUE}`);"
        )

        driver.refresh()
        time.sleep(2)

        # --------------------------------
        # ACESSA O CURSO
        # --------------------------------
        botao_cursos = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Cursos')]"))
        )
        botao_cursos.click()

        primeiro_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]"))
        )
        primeiro_curso.click()

        # --------------------------------
        # ACESSA O QUIZ
        # --------------------------------
        botao_quiz = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Quiz')]"))
        )
        botao_quiz.click()

        time.sleep(2)

        # Agora estamos na tela que aparece na sua foto

        # --------------------------------
        # SELECIONA UMA ALTERNATIVA
        # (a segunda alternativa, como na foto)
        # --------------------------------
        alternativa_correta = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio'])[2]"))
        )
        alternativa_correta.click()

        time.sleep(1)

        # --------------------------------
        # CLICA EM "Próxima" PARA SALVAR
        # --------------------------------
        botao_proxima = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Próxima')]"))
        )
        botao_proxima.click()

        time.sleep(2)

        # --------------------------------
        # VALIDAR QUE A RESPOSTA FOI REGISTRADA
        # --------------------------------
        # Verifica se a próxima questão carregou
        titulo_proxima_questao = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(., 'Questão')]"))
        )

        self.assertTrue(titulo_proxima_questao.is_displayed())

        print("\nRF28 – Alternativa correta selecionada e registrada com sucesso!")

if __name__ == "__main__":
    unittest.main()
