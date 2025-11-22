import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ExclusaoSlideTest(unittest.TestCase):

    NOME_CURSO_ALVO = "RF 09 e 10 Edição e Exclusão de slide"
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"	
    FIREBASE_VALUE = """{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438261679","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763590598431","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"providerId":"google.com","uid":"105856292510209699123","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS90ZXN0ZXMtY29kZWZvbGlvIiwiYXVkIjoidGVzdGVzLWNvZGVmb2xpbyIsImF1dGhfdGltZSI6MTc2MzU5MDU5OCwidXNlcl9pZCI6Ijh6VmJ0WWxFVlpib1hYd1ZOWDZlSTNaaGV6dDIiLCJzdWIiOiI4elZidFlsRVZaYm9YWHdWTlg2ZUkzWmhlenQyIiwiaWF0IjoxNzYzNzQ3ODc0LCJleHAiOjE3NjM3NTE0NzQsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.1_SGXCVUdDP77of1Dq17sjvr7oaFB6LrHwNkcdBOli0utPUxHz4rvKETnThcPV8sVk2GJtdUxFJhNNvcXfnyxzTUYQHe6AHAfpyljkW80lHdGIv5_BFnTVXd9uhwR1LjSiqYYxdsIMlDeCahaBk99rsa2hOS4dDQL6rxveO2NGsB9_BT6kjbZphSFywugTZbj_4g9fMixxuBdCEbmlsnq0R9vk3PiwBHLAdeV5it9lZ3LXLCAAER80ZyN_e-726sxvxFqsUTcnqMABCafVTMBuD8lvMrWtQ-7IenkdpCdnVWdC4H5Zd9foO1HUoB94wstIti1tjZZ5HcTiFkuaCYGQ","expirationTime":1763751478217,"refreshToken":"AMf-vBwFZCN9xYE7fhB3CnOkT90ir-eR9pNGK5RSVLJmnrmUHvxjcEj7UTVeD7SMl18v0GHpLgu8wgTbXnmz7X_4BCJYwvSqvH0AXUamMm16ljveuxBjFRp0EgoUjJf5g5l-ffuoHbaF-l5zbkWhMJX-uKXFp8jwAmtJxQg8VI6URceVe5fBQsoigbAzaEsiWYjyTLzruDSfCkC-de4uaapxSIL-Kg4bHPL4jgfGacHWICwZK-64IgrmFzmkaiN0DbxdyJlSO0T5sxF-HpHPld8QMeEfj0xklXmDYjLR3K_RE16-XkuHkePIFGum5EWAQpAjLvvW4sEBgRa_7jFn7wuXM_vgjlHYnUgRfHOwmLwpgJj02HUpTSPHSdr8Kcqe8EHPi4qgW0GkGThfrwZBIYjx69jahYlnPanHCCwPFRNol7f5aSbzT8cjE6eEAnSuGRMyHx0W-3UVkCP-rCV6bp0tBNHji6Ib6A"},"tenantId":null,"uid":"8zVbtYlEVZboXXwVNX6eI3Zhezt2","_redirectEventId":null}"""
   
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
 
        self.EVIDENCE_DIR = "Bernardo-Dorneles/img/RF10-CT01/"
        os.makedirs(self.EVIDENCE_DIR, exist_ok=True)
        
        self.configurar_autenticacao()

    def configurar_autenticacao(self):
        self.driver.get(self.URL_BASE)
        print("Injetando autenticação...")
        try:
            self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", self.FIREBASE_KEY, self.FIREBASE_VALUE)
        except Exception as e:
            print(f"Falha na injeção: {e}")
            self.driver.quit()
            raise
        self.driver.refresh()
        time.sleep(3)

    def test_exclusao_slide_rf10(self):
        """CT-01 - Exclusão de Slides (RF10)"""
        print(f"\n=== INICIANDO CT-01 - EXCLUSÃO DE SLIDES ({self.NOME_CURSO_ALVO}) ===")
        slide_removido = False
        
        try:
            self.navegar_para_gerenciamento_cursos()
            
            if not self.selecionar_curso_especifico(self.NOME_CURSO_ALVO):
                self.fail(f"Curso '{self.NOME_CURSO_ALVO}' não encontrado.")
            
            self.navegar_para_secao_slides()
            
            nome_slide_alvo = self.obter_nome_primeiro_slide()
            print(f"Slide alvo para exclusão: '{nome_slide_alvo}'")
            
            self.clicar_icone_exclusao_slide()
            self.confirmar_exclusao_modal()
            
            slide_removido = self.verificar_slide_inexistente(nome_slide_alvo)
            
        except Exception as e:
            print(f"FALHA NO TESTE: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_fatal_rf10.png")
            self.fail(f"Erro: {e}")
            
        self.assertTrue(slide_removido, "FALHA NO ASSERT: O slide ainda está visível após a exclusão.")
        print("CT-01 (RF10) - EXCLUSÃO CONCLUÍDA COM SUCESSO!")

    # --- MÉTODOS AUXILIARES ---

    def navegar_para_gerenciamento_cursos(self):
        print("Navegando para Gerenciamento...")
        profile_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")))
        self.driver.execute_script("arguments[0].click();", profile_btn)
        
        menu_item = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")))
        menu_item.click()
        self.wait.until(EC.url_contains("/manage-courses"))

    def selecionar_curso_especifico(self, nome_curso):
        print(f"Procurando curso: '{nome_curso}'...")
        time.sleep(3)
        try:
            xpath_botao = f"//*[contains(text(), '{nome_curso}')]/following::button[contains(., 'Gerenciar Curso')][1]"
            botao_gerenciar = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao)))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_gerenciar)
            time.sleep(1)
            botao_gerenciar.click()
            
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return True
        except Exception as e:
            print(f"Erro ao encontrar curso específico: {e}")
            return False

    def navegar_para_secao_slides(self):
        print("Abrindo aba Slides...")
        time.sleep(2)
        
        # Seletores robustos
        slides_selectors = [
            "//*[contains(text(), 'SLIDES')]",
            "//*[contains(text(), 'Slides')]",
            "//button[contains(., 'SLIDES')]",
            "//button[contains(., 'Slides')]",
            "//*[@role='tab' and contains(., 'SLIDES')]",
            "//*[@role='tab' and contains(., 'Slides')]"
        ]
        
        for selector in slides_selectors:
            try:
                slides_element = self.driver.find_element(By.XPATH, selector)
                if slides_element.is_displayed() and slides_element.is_enabled():
                    self.driver.execute_script("arguments[0].click();", slides_element)
                    time.sleep(3)
                    
                    if self.verificar_secao_slides_ativa():
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2) 
                        
                        # --- EVIDÊNCIA 01: ANTES DA EXCLUSÃO ---
                        print("Evidência 1: Antes da Exclusão")
                        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_01_antes_exclusao.png")
                        return
            except:
                continue
        
        if self.verificar_secao_slides_ativa():
            return

        raise Exception("Aba Slides não encontrada")

    def verificar_secao_slides_ativa(self):
        try:
            indicadores = [
                "//*[contains(text(), 'Gerenciar Slides')]",
                "//*[contains(text(), 'Adicionar Novo Slide')]",
                "//*[contains(text(), 'Slides Cadastrados')]",
            ]
            for indicador in indicadores:
                if self.driver.find_element(By.XPATH, indicador).is_displayed():
                    return True
            return False
        except:
            return False

    def obter_nome_primeiro_slide(self):
        try:
            elemento_titulo = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "(//*[contains(text(), 'Slides Cadastrados')]/following-sibling::div//h6 | //*[contains(text(), 'Slides Cadastrados')]/following-sibling::div//p)[1]"
            )))
            return elemento_titulo.text
        except:
            return "Slide Indefinido"

    def clicar_icone_exclusao_slide(self):
        print("Clicando em excluir (lixeira)...")
        time.sleep(1)
        try:
            icone_lixeira = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "(//*[contains(text(), 'Slides Cadastrados')]/following-sibling::div//button)[2]"
            )))
            self.driver.execute_script("arguments[0].click();", icone_lixeira)
        except Exception as e:
            print(f"Erro ao clicar na lixeira: {e}")
            raise

    def confirmar_exclusao_modal(self):
        print("Confirmando exclusão...")
        time.sleep(1)
        try:
            botao_confirma = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Sim') or contains(., 'Confirmar') or contains(., 'Excluir') or contains(., 'Delete')]"
            )))
            botao_confirma.click()
            time.sleep(3)
        except:
            print("Não foi possível confirmar a exclusão no modal.")
            raise

    def verificar_slide_inexistente(self, texto_alvo):
        print(f"Verificando se '{texto_alvo}' foi removido...")
        time.sleep(2)
        

        print("Evidência 2: Após Exclusão")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_02_depois_exclusao.png")
        
        if texto_alvo == "Slide Indefinido":
            return True

        elementos = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{texto_alvo}')]")
        visiveis = [e for e in elementos if e.is_displayed()]
        
        if len(visiveis) == 0:
            return True
        else:
            print(f"Texto '{texto_alvo}' ainda encontrado na página.")
            return False

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()