# test_rf26_sorteio.py
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

# 🔑 MESMO FIREBASE DO RF20 E RF25
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FIREBASE_VALUE = "{\"apiKey\":\"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg\",\"appName\":\"[DEFAULT]\",\"createdAt\":\"1762298062528\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"emailVerified\":true,\"isAnonymous\":false,\"lastLoginAt\":\"1762375068503\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\",\"providerData\":[{\"providerId\":\"google.com\",\"uid\":\"116550479800107608553\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\"}],\"stsTokenManager\":{\"accessToken\":\"TOKEN\",\"expirationTime\":1762382144118,\"refreshToken\":\"REFRESH\",\"tenantId\":null},\"uid\":\"DbqhhkiZDdNelM1ylvP7Qnoch6A3\",\"_redirectEventId\":null}"

class TestRF26Sorteio(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.driver.get(URL_BASE)

        # 🔥 INSERE LOGIN PELO LOCALSTORAGE
        self.driver.execute_script(
            f"window.localStorage.setItem('{FIREBASE_KEY}', '{FIREBASE_VALUE}')"
        )
        time.sleep(1)
        self.driver.refresh()
        time.sleep(2)

    def test_rf26_sorteio_de_estudante(self):
        driver = self.driver
        wait = self.wait

        print("\n🔍 Acessando tela de avaliações...")
        driver.get("https://testes.codefolio.com.br/dashboard")

        # Aguardar carregamento da dashboard
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("➡️ Abrindo avaliação para realizar o sorteio...")
        avaliacao = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Avaliações')]")
        ))
        avaliacao.click()

        # Seleciona uma avaliação específica
        item = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[contains(@class,'avaliacao-card')])[1]")
        ))
        item.click()

        print("🎲 Iniciando o sorteio aleatório...")
        botao_sorteio = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Sortear estudante')]")
        ))
        botao_sorteio.click()

        print("⏳ Aguardando resultado do sorteio...")
        sorteado = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(@class,'estudante-sorteado')]")
        ))

        nome_sorteado = sorteado.text.strip()
        print(f"🎉 Estudante sorteado: {nome_sorteado}")

        # VALIDAÇÃO
        self.assertTrue(len(nome_sorteado) > 0, "Nenhum estudante foi sorteado!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
