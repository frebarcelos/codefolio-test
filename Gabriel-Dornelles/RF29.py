# RF29.py - Navegação entre questões do quiz.

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

# --- SUAS CREDENCIAIS DO FIREBASE (copie de RF28 se necessário) ---
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400773157","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763312937265","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"<ACCESS_TOKEN>","expirationTime":1763316840772,"refreshToken":"<REFRESH_TOKEN>"},"uid":"5Jj2OvuSvubRzgdAZdNS3sDNE003","_redirectEventId":null}'''


class TestRF29NavegacaoQuestoes(unittest.TestCase):

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

	def test_navegacao_entre_questoes(self):
		"""Requisito: Navegação entre questões — avançar e voltar entre questões do quiz."""
		driver = self.driver
		wait = self.wait

		# --------------------------------
		# LOGIN VIA LOCALSTORAGE FIREBASE
		# --------------------------------
		driver.get(URL_BASE)
		driver.execute_script(
			"window.localStorage.setItem(arguments[0], arguments[1]);",
			FIREBASE_KEY,
			FIREBASE_VALUE,
		)
		driver.refresh()
		time.sleep(2)

		# -----------------------------
		# Navegar para o curso -> Quiz
		# -----------------------------
		try:
			botao_cursos = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Cursos')]") ))
		except Exception:
			ts = int(time.time())
			with open(f"debug_page_source_rf29_no_cursos_{ts}.html", 'w', encoding='utf-8') as f:
				f.write(driver.page_source)
			driver.save_screenshot(f"debug_screenshot_rf29_no_cursos_{ts}.png")
			self.fail('Botão "Cursos" não encontrado')

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

		try:
			primeiro_curso = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Acessar')])[1]")))
			robust_click(primeiro_curso)
		except Exception:
			ts = int(time.time())
			with open(f"debug_page_source_rf29_no_acessar_{ts}.html", 'w', encoding='utf-8') as f:
				f.write(driver.page_source)
			driver.save_screenshot(f"debug_screenshot_rf29_no_acessar_{ts}.png")
			self.fail('Não foi possível acessar o primeiro curso')

		try:
			botao_quiz = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Quiz') or contains(., 'Quiz')]")))
			robust_click(botao_quiz)
		except Exception:
			ts = int(time.time())
			with open(f"debug_page_source_rf29_no_quiz_{ts}.html", 'w', encoding='utf-8') as f:
				f.write(driver.page_source)
			driver.save_screenshot(f"debug_screenshot_rf29_no_quiz_{ts}.png")
			self.fail('Botão do Quiz não encontrado')

		time.sleep(2)

		# --------------------------------
		# Validar navegação: Próxima -> Anterior
		# --------------------------------
		try:
			# localizar elemento que representa o conteúdo da questão
			question_locators = [
				(By.XPATH, "//div[contains(., 'Questão')][1]"),
				(By.XPATH, "//div[contains(@class,'question') or contains(@class,'Questao')]"),
				(By.XPATH, "//h4[contains(., 'Questão') or contains(@class,'question')]"),
			]

			question_el = None
			for by, sel in question_locators:
				try:
					question_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, sel)))
					break
				except Exception:
					continue

			if not question_el:
				ts = int(time.time())
				with open(f"debug_page_source_rf29_no_question_{ts}.html", 'w', encoding='utf-8') as f:
					f.write(driver.page_source)
				driver.save_screenshot(f"debug_screenshot_rf29_no_question_{ts}.png")
				self.fail('Não foi possível localizar o elemento da questão inicial')

			initial_text = question_el.text.strip()[:200]

			# clicar em Próxima
			try:
				btn_next = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Próxima') or contains(., 'Avançar') or contains(., 'Próximo')]")))
			except Exception:
				ts = int(time.time())
				with open(f"debug_page_source_rf29_no_next_{ts}.html", 'w', encoding='utf-8') as f:
					f.write(driver.page_source)
				driver.save_screenshot(f"debug_screenshot_rf29_no_next_{ts}.png")
				self.fail('Botão "Próxima" não encontrado')

			robust_click(btn_next)

			# aguardar mudança no conteúdo da questão
			try:
				def question_changed(drv):
					try:
						el = None
						for by, sel in question_locators:
							try:
								el = drv.find_element(by, sel)
								break
							except Exception:
								continue
						if not el:
							return False
						return el.text.strip()[:200] != initial_text
					except Exception:
						return False

				WebDriverWait(driver, 8).until(question_changed)
			except Exception:
				ts = int(time.time())
				with open(f"debug_page_source_rf29_after_next_{ts}.html", 'w', encoding='utf-8') as f:
					f.write(driver.page_source)
				driver.save_screenshot(f"debug_screenshot_rf29_after_next_{ts}.png")
				self.fail('Após clicar em Próxima, o conteúdo da questão não mudou')

			# capturar texto atual
			try:
				current_question_el = None
				for by, sel in question_locators:
					try:
						current_question_el = driver.find_element(by, sel)
						break
					except Exception:
						continue
				current_text = current_question_el.text.strip()[:200]
			except Exception:
				current_text = None

			# clicar em Anterior
			try:
				btn_prev = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Anterior') or contains(., 'Voltar') or contains(., 'Anterior')]")))
			except Exception:
				ts = int(time.time())
				with open(f"debug_page_source_rf29_no_prev_{ts}.html", 'w', encoding='utf-8') as f:
					f.write(driver.page_source)
				driver.save_screenshot(f"debug_screenshot_rf29_no_prev_{ts}.png")
				self.fail('Botão "Anterior" não encontrado')

			robust_click(btn_prev)

			try:
				def question_back(drv):
					try:
						el = None
						for by, sel in question_locators:
							try:
								el = drv.find_element(by, sel)
								break
							except Exception:
								continue
						if not el:
							return False
						return el.text.strip()[:200] == initial_text
					except Exception:
						return False

				WebDriverWait(driver, 8).until(question_back)
			except Exception:
				ts = int(time.time())
				with open(f"debug_page_source_rf29_after_prev_{ts}.html", 'w', encoding='utf-8') as f:
					f.write(driver.page_source)
				driver.save_screenshot(f"debug_screenshot_rf29_after_prev_{ts}.png")
				self.fail('Após clicar em Anterior, a questão inicial não foi restaurada')

			print('\nRF29 - Navegação entre questões (Próxima e Anterior) validada com sucesso!')

		except Exception as e:
			traceback.print_exc()
			ts = int(time.time())
			try:
				with open(f"debug_page_source_rf29_general_{ts}.html", 'w', encoding='utf-8') as f:
					f.write(driver.page_source)
			except Exception:
				pass
			try:
				driver.save_screenshot(f"debug_screenshot_rf29_general_{ts}.png")
			except Exception:
				pass
			self.fail(f'Erro no fluxo de navegação entre questões: {e}')


if __name__ == "__main__":
	unittest.main()

