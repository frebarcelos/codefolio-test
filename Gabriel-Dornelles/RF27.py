# RF27.py - Seleção Manual de Estudante (versão simplificada)
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

class TestRF27SelecaoManual(unittest.TestCase):

    def setUp(self):
        # Inicia Firefox sem nenhuma configuração externa
        self.driver = webdriver.Firefox(service=Service())
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def tearDown(self):
        self.driver.quit()

    def test_rf27_selecao_manual_estudante(self):

        driver = self.driver
        wait = self.wait

        # --- ACESSA O SITE ---
        driver.get(URL_BASE)
        time.sleep(2)

        # --- LOGIN MANUAL (espera o usuário fazer login) ---
        print("\n📌 Faça login manualmente no CodeFólio e depois aperte ENTER aqui...")
        input()

        # --- MENU QUIZ ---
        botao_quiz = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Quiz')]"))
        )
        botao_quiz.click()

        # --- SELECIONAR O PRIMEIRO QUIZ ---
        quiz_item = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'quiz-card')])[1]"))
        )
        quiz_item.click()

        # --- BOTÃO SELECIONAR ALUNO ---
        botao_selecao = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Selecionar Estudante')]"))
        )
        botao_selecao.click()

        # --- ESCOLHE O PRIMEIRO ALUNO ---
        aluno = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'student-item')])[1]"))
        )
        nome_aluno = aluno.text.strip()
        aluno.click()

        # --- CONFIRMAR ---
        botao_confirmar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirmar')]"))
        )
        botao_confirmar.click()

        # --- VERIFICAÇÃO ---
        aluno_selecionado = wait.until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{nome_aluno}') and contains(text(),'selecionado')]"))
        )

        self.assertIn(nome_aluno, aluno_selecionado.text)

        print("\n✅ RF27 – Teste de Seleção Manual de Estudante executado com sucesso!")

if __name__ == "__main__":
    unittest.main()
