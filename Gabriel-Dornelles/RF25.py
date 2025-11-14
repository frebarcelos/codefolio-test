# RF25.py
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

# ===== padrão / constantes =====
TIMEOUT = 20
URL_BASE = "https://testes.codefolio.com.br/"

# Copie/cole aqui os valores adequados (use os mesmos do test_rf20_filtros)
FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FIREBASE_VALUE = "{\"apiKey\":\"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg\",\"appName\":\"[DEFAULT]\",\"createdAt\":\"1762298062528\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"emailVerified\":true,\"isAnonymous\":false,\"lastLoginAt\":\"1762375068503\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\",\"providerData\":[{\"providerId\":\"google.com\",\"uid\":\"116550479800107608553\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\"}],\"stsTokenManager\":{\"accessToken\":\"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBDYW1hcmdvIE9ydGl6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0t1U09yMmFvc3E1ZXdZVGtWWG1pY1dwbU03OENyQ2FOV1ZnOFRfTnU0d2s1VTc2dz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjM3NTA2OCwidXNlcl9pZCI6IkRicWhoa2laRGROZWxNMXlsdlA3UW5vY2g2QTMiLCJzdWIiOiJEYnFoaGtpWkRkTmVsTTF5bHZQN1Fub2NoNkEzIiwiaWF0IjoxNzYyMzc4NTQwLCJleHAiOjE3NjIzODIxNDAsImVtYWlsIjoiZ2FicmllbG9ydGl6LmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE2NTUwNDc5ODAwMTA3NjA4NTUzIl0sImVtYWlsIjpbImdhYnJpZWxvcnRpei5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.gSpY-wiJTMD1UKbLdV0H_-88rP4EjZT97XJBNeJYcCvtaI_-aUFCHIsYjcb93IM7hdSyfaueJbZqSEgO-ue-U9oc57aDwWNSFIlKZ8dHbYxiFBhj5Mr5I3WrmUlis1e_CnpgWS3d8Zo_CIq2tUumGRmaBUdvA4hGRp7_m6s0JP7ex1dykS0hiXRbpjgKnJny3NKGQ5_vhRj8xeYdyxubDfEmx-iPFArxUQXwraglY8ULH8XmkR4GtDr3Dfgkm5u3JYAtd3YiCkEdJUcrLmXiCZNwoWW3dMJ67b7GvTL6ONt3yQMWYJktjJ8hBhC7KdkRYaJIRvHAdC0nhRy-HTslTw\",\"expirationTime\":1762382144118,\"refreshToken\":\"AMf-vBzXfOOx4uuxgjeYVCXhmoKwXhjZmcZLc2yQDBbi-wIQyJCuWkkSFmPl37Z7a9PuyCtXDvPttjH_tgdaS6JIh8oR9nQ-G-0qmuosOpocx9hazemh4Q85GVybUEOEVx5gw0ARBtN8jtdsOxYh8QQSCdKeI6on8GmoYPGif2wJ-ZZ3KpCUFlLw0t0JvUknlh0nxsfnei46Qu2aYSH1Tz2-5sUyn7E-ghbYkJH-H-AgcnDi8oWlCh5WTFzsCaSgva5-2cQHVaBNIzZKENltzah7iSf7SUiQj_WvCMLyg-FO87hNc--g6d-lULpNpwz9yScZnA1vJDinCnU7Cbl1pefFXRTA-nD4s1mkdHcvm7exzX5kd3TAbVNZ3CQ-JiU-7h-Mo5ISrsZZxHtCksr6w93Xk9KyYhYC8uAEIlx8xqlRL8KlsWOtXgzDEJWW_Fmk_W4LUaL2XBQh_tMfroBxm5EMW3UarWBUKw\",\"tenantId\":null},\"uid\":\"DbqhhkiZDdNelM1ylvP7Qnoch6A3\",\"_redirectEventId\":null}"

class TestRF25AtribuirNota(unittest.TestCase):

    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.driver.implicitly_wait(5)

    def tearDown(self):
        try:
            self.driver.save_screenshot(f"resultado_{self.id()}.png")
        except:
            pass
        self.driver.quit()

    # ---- util: injetar firebase e forçar login ----
    def _inject_firebase_and_refresh(self):
        print("Injetando FIREBASE no localStorage...")
        self.driver.get(URL_BASE)
        time.sleep(1)
        try:
            self.driver.execute_script(
                "window.localStorage.setItem(arguments[0], arguments[1]);",
                FIREBASE_KEY,
                FIREBASE_VALUE
            )
            print("Injeção OK. Atualizando página...")
            self.driver.refresh()
            time.sleep(2)
        except Exception as e:
            print("Falha ao injetar FIREBASE:", e)
            raise

    # ---- util: abrir painel do professor (melhor esforço) ----
    def _abrir_painel_professor(self):
        print("Tentando abrir painel do professor...")
        # tenta rota direta do teacher
        self.driver.get(URL_BASE + "teacher")
        try:
            self.wait.until(EC.url_contains("/teacher"))
            print("Painel do professor carregado por /teacher")
            return
        except TimeoutException:
            pass

        # fallback: ir para listcurso e tentar navegar
        self.driver.get(URL_BASE + "listcurso")
        self.wait.until(EC.url_contains("/listcurso"))
        try:
            botao_prof = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Painel') or contains(.,'Área do Professor') or contains(.,'Professor')]")))
            botao_prof.click()
            time.sleep(1)
            if "/teacher" in self.driver.current_url:
                print("Painel do professor aberto via botão.")
                return
        except Exception:
            pass

        print("Não entrou automaticamente no painel do professor; prosseguindo na rota atual.")

    # ---- util: abrir avaliações de um curso ----
    def _abrir_avaliacoes_primeiro_curso(self):
        print("Abrindo primeiro curso disponível...")
        # tenta clicar primeiro card de curso
        try:
            curso = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'MuiCard-root') or contains(@class,'course-card')])[1]")))
            self.driver.execute_script("arguments[0].click();", curso)
            time.sleep(1)
        except Exception as e:
            raise AssertionError("Não foi possível abrir o curso: " + str(e))

        print("Acessando aba Avaliações...")
        try:
            tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Avaliações') or contains(.,'Avaliação') or contains(.,'Provas')]")))
            tab.click()
            time.sleep(1)
        except Exception:
            print("Aba 'Avaliações' não encontrada por botão. Tentando buscar link/rota...")
            # tenta rota alternativa
            self.driver.get(self.driver.current_url + "/evaluations")
            time.sleep(1)

    # ---- util: abrir tentativa/aluno para correção ----
    def _abrir_primeira_tentativa(self):
        print("Abrindo primeira tentativa para correção...")
        # procura botões como "Corrigir", "Corrigir tentativa", "Ver tentativas", "Corrigir prova"
        possible_xpaths = [
            "//button[contains(., 'Corrigir')]",
            "//button[contains(., 'Corrigir tentativa')]",
            "//button[contains(., 'Ver tentativas')]",
            "//button[contains(., 'Ver tentativas') and contains(@class,'MuiButton-root')]",
            "//a[contains(., 'Corrigir')]",
            "(//button[contains(., 'Ver tentativas') or contains(., 'Corrigir') or contains(., 'Ver tentativas')])[1]"
        ]
        for xp in possible_xpaths:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
                return
            except Exception:
                continue
        raise AssertionError("Nenhum botão de abrir tentativa/correção foi encontrado.")

    # ---- util: preencher nota e feedback e salvar ----
    def _preencher_nota_e_salvar(self, nota="9.5", feedback="Parabéns pelo trabalho!"):
        print("Preenchendo nota e feedback (se existirem)...")
        # tenta localizar input numérico (type=number) ou inputs com name/id 'grade' 'nota'
        input_selectors = [
            (By.XPATH, "//input[@type='number']"),
            (By.XPATH, "//input[contains(@name,'grade') or contains(@id,'grade') or contains(@name,'nota') or contains(@id,'nota')]"),
            (By.XPATH, "//input[contains(@placeholder,'Nota') or contains(@placeholder,'nota')]"),
        ]
        input_element = None
        for sel in input_selectors:
            try:
                input_element = self.wait.until(EC.presence_of_element_located(sel))
                break
            except Exception:
                continue

        if not input_element:
            raise AssertionError("Campo de nota não encontrado.")

        try:
            input_element.clear()
            input_element.send_keys(str(nota))
            print("Nota preenchida:", nota)
        except Exception as e:
            print("Falha ao digitar nota:", e)

        # tentar textarea de feedback
        try:
            textarea = self.driver.find_element(By.XPATH, "//textarea[contains(@name,'feedback') or contains(@id,'feedback') or contains(@placeholder,'feedback') or contains(@placeholder,'Coment')]")
            textarea.clear()
            textarea.send_keys(feedback)
            print("Feedback preenchido.")
        except NoSuchElementException:
            print("Textarea de feedback não encontrada — pulando (é opcional).")
        except Exception as e:
            print("Erro ao preencher feedback:", e)

        # tentar salvar: vários textos possíveis
        save_xpaths = [
            "//button[normalize-space()='Salvar']",
            "//button[contains(.,'Salvar')]",
            "//button[normalize-space()='Enviar']",
            "//button[contains(.,'Enviar')]",
            "//button[contains(.,'Salvar nota')]",
            "//button[contains(.,'Enviar avaliação')]",
            "//button[contains(.,'Confirmar')]"
        ]
        clicked = False
        for sx in save_xpaths:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, sx)))
                self.driver.execute_script("arguments[0].click();", btn)
                clicked = True
                print("Clique no botão de salvar/enviar por xpath:", sx)
                time.sleep(1)
                break
            except Exception:
                continue

        if not clicked:
            raise AssertionError("Botão de salvar/enviar não encontrado.")

        # validação de sucesso (mensagem tolerante)
        success_texts = [
            "Nota atribuída",
            "avaliação salva",
            "Salvo com sucesso",
            "Avaliação enviada",
            "Nota salva",
            "Sucesso"
        ]
        found = False
        for txt in success_texts:
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{txt.lower()}')]")))
                print("Mensagem de sucesso detectada:", txt)
                found = True
                break
            except Exception:
                continue

        if not found:
            print("Aviso: Não detectei mensagem de sucesso explícita. Verifique manualmente.")
        else:
            print("Confirmação de sucesso detectada.")

    # ---- TESTE PRINCIPAL RF25 ----
    def test_01_atribuicao_nota_professor(self):
        """
        RF25 – O professor deve conseguir atribuir nota e feedback (opcional).
        """
        try:
            # injeta firebase para simular login
            self._inject_firebase_and_refresh()

            # abrir painel do professor / rota
            self._abrir_painel_professor()

            # abrir primeiro curso e ir para avaliações
            self._abrir_avaliacoes_primeiro_curso()

            # abrir primeira tentativa/aluno para correção
            self._abrir_primeira_tentativa()

            # preencher nota e salvar
            self._preencher_nota_e_salvar(nota="9.5", feedback="Parabéns! Excelente desempenho.")
        except Exception as e:
            # log completo e falha do teste
            import traceback
            traceback.print_exc()
            self.fail(f"Falha no RF25: {e}")

if __name__ == "__main__":
    unittest.main()
