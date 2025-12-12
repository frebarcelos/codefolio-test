# RF29.py - Navegação entre questões do quiz.

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
from selenium.webdriver.common.keys import Keys
import traceback

TIMEOUT = 15
URL_BASE = "https://testes-codefolio.web.app/"

# --- SUAS CREDENCIAIS DO FIREBASE (copie de RF28 se necessário) ---
FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"

FIREBASE_VALUE = '''{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438492669","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1765251419562","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c","providerData":[{"providerId":"google.com","uid":"109172986672116476612","displayName":"Gabriel Dornelles dos Santos","email":"gabrieldornelles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocK-Tiyow-pH5YLZAbB9rn448ysNF7XgON2BHPijJWGrAWOKSA=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1MTg5MTkxMTA3NjA1NDM0NGUxNWUyNTY0MjViYjQyNWVlYjNhNWMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBEb3JuZWxsZXMgZG9zIFNhbnRvcyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLLVRpeW93LXBINVlMWkFiQjlybjQ0OHlzTkY3WGdPTjJCSFBpakpXR3JBV09LU0E9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdGVzLWNvZGVmb2xpbyIsImF1ZCI6InRlc3Rlcy1jb2RlZm9saW8iLCJhdXRoX3RpbWUiOjE3NjUyNTE0MTksInVzZXJfaWQiOiJ4bDF5dGh5MXQwZkVmeTUwaVBzeVpaZ0NYV1AyIiwic3ViIjoieGwxeXRoeTF0MGZFZnk1MGlQc3laWmdDWFdQMiIsImlhdCI6MTc2NTI1MTQxOSwiZXhwIjoxNzY1MjU1MDE5LCJlbWFpbCI6ImdhYnJpZWxkb3JuZWxsZXMuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDkxNzI5ODY2NzIxMTY0NzY2MTIiXSwiZW1haWwiOlsiZ2FicmllbGRvcm5lbGxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.clAo078xMikQiKPrecLA00fsyl0fo78vtV4GRlBVddfIrluEvCb-tBXXrOAJHxxTbWs8QJmkFe2Z8uz5NWJU4A_xSRRZ6d_QCFKGSoBYsN9cTcwCH_Cr5VkXlAvrR5WUIJEGlaZVN0I-Xh16IRwoulvvDpILEcDfW7zORRb7hLQjv8_6IXfcfBPpKn0TLXgCRSQAJ79C_SRkxo3vmIi77gMjjfdYQVEEkSqNQN8cBcWGWc7X7G6DsNIfePJOeBEz-EolFgpKiIqnT-wHWgALNZT7RCDdGlz0fVvofrEdrmjeHW1w_D9wRkkUO0ywjjYevVgaWScWG4PUKy47G6ehYw","expirationTime":1765255334013,"refreshToken":"AMf-vBzNg3a_AOOdTUcOG12ZVrL5FSCj7y1CLqkkfsL3SZbWMf9_lK_10_NYB9vY_wO1tqP4LgHh5kdSMu4LJE2UWRo1cr22vjlJ_u7QmntDar9YIe9CSEsE-d1vOVpM0IwRwseRcbTzLRuTQT3Hqh-2EjNq_7sYSD0Qplf5pgwxDNJnSMrcNAXYbUMDjZtG2ibXvEicP-Q9pvR4bRcG1QoroXSUYKo24u0U-T5SUDhE0k6kXNPaoy2a_MLThv3TkxXqB1t2yKW6MYmxRa75574IR4e7M2sLskI9p5oQNouxPJI6dOR2yU4KI_FIIzZJQNxyYkUvDCHvcxXhN2-HJdXAiSIu_EPZMwg_i2XlkM4GIqkPD1-uFjvtVPOsI87IOQRe81_UpeTVvHn2br3b0zy8ahWkbPj1qNr0ku2C5_3l2kHxv_QaCKZFRouVRsiW9sfBaEZNHlJqsRxNB1Eqn50clHJeuw2bUrRXzptKdEdjdkx56t4wCho","tenantId":null,"uid":"xl1ythy1t0fEfy50iPsyZZgCXWP2","_redirectEventId":null}'''



class TestRF29NavegacaoQuestoes(unittest.TestCase):

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

	def test_navegacao_entre_questoes(self):
		"""Requisito: Navegação entre questões — avançar e voltar entre questões do quiz."""
		driver = self.driver
		wait = self.wait

		# --------------------------------
		# LOGIN VIA LOCALSTORAGE FIREBASE (injetar no domínio do Firebase)
		# --------------------------------
		driver.get("https://react-na-pratica.firebaseapp.com/")
		time.sleep(1)
		driver.execute_script("window.localStorage.clear();")
		time.sleep(0.5)
		# Use argumentized execute_script to avoid quoting/escape issues
		driver.execute_script(
			"window.localStorage.setItem(arguments[0], arguments[1]);",
			FIREBASE_KEY,
			FIREBASE_VALUE,
		)

		driver.refresh()
		time.sleep(2)
		driver.get(URL_BASE)
		time.sleep(1)

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

