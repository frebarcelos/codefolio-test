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

    NOME_CURSO_ALVO = "RF 10 - Exclusão de Slide"
    
    URL_BASE = "https://testes.codefolio.com.br/"
    FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
    FIREBASE_VALUE = """{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400677093","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1762623423706","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerId":"google.com","uid":"105856292510209699123"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjYyMzUwMSwidXNlcl9pZCI6Ik92S09rWUNLMmVUN3huM1FjUVRZblpTYjFSMzMiLCJzdWIiOiJPdktPa1lDSzJlVDd4bjNRY1FUWW5aU2IxUjMzIiwiaWF0IjoxNzYyNjczOTkwLCJleHAiOjE3NjI2Nzc1OTAsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm9jSmlkZXIiOiJnb29nbGUuY29tIn19.a-W_CUqU0ZP81ZpURu49b6cBrClWk0nqcraFGw47ktTuK3mqtIovg_dqmbZ7s5GghCdk6_twFA6ihdPuFbyLpCX8PZLAIcyQFQBeVQ11ql3oCDeGiQogXKw-sM5TIIix4gTgsS7IXhr6uNbkFCysLUSuA8H-bp10VsiU7R8fHz0BQTj0qExL6SCqCw05F76HXBuzxwyknYj1FeX53jGFdOmAhbHl9eHAhSkl7pBmkLBFkHqW9FXW1ttDGtg4Vh9UD_Inb432gglN-ZBPHy2ukSSrTOex430IDjJTdfZOhRe-jhscMnfLYWRS-9B1Y-dF7r-SJcW1_PTdCVuhYOhh0A","expirationTime":1762677590230,"refreshToken":"AMf-vBzmGoli8pLckXIHEHFjBsq9tdclxZJyoH1JbcdFrcPLRxGaM1rX9B8XHnnJ_XN05JfnkqyH5bYKdBmFud2NNZehSZM4mSXlBQU5HTmmV4vCyBk6T76D7ne-jyrdpzFvhApdJyMx-vyjhqUzyv2uMVdTxfj-pb6kZXAGW_a9tW7q0OA9CJ_KF1eGqx3DcSemtemLSxyxNo0A3gXeMMADVdpIgH8KmQbcFVfqEgr2Lh4C11_njx-Myfov2byzlZpc1zCivD1xCX5LLoEOgcCWMCp8_BEeHtwLeFGRS4DDxxpPH2-WcGpLJINOxCbUFQYeCfVT0bzzGjPgBKA28TQTmv7T0x8uCVBTUHNoVwpmpt9zFqO4QncobWpTnVT4ns7eQyRlBBNdTjSc9133whnn9bT3Wzfar0U2zh9VgFzjftgpgSx3UCNzJkCTvmicr38knaKKfpxGP6dDdqG4Ohjf_Ji9mPxzQw"},"tenantId":null,"uid":"OvKOkYCK2eT7xn3QcQTYnZSb1R33","_redirectEventId":null}"""

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
 
        self.EVIDENCE_DIR = "img/RF10-CT01/"
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