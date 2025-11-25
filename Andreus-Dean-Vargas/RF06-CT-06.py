"""
CT-06 - Edição de Vídeos (RF06)
Autor: Andreus Dean Ferreira Almeida Rodrigues Vargas
Data: 23/11/2024
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chrome_config import get_chrome_options
from login_util import login, verificar_login
from screenshot_util import take_evidence
from element_finder import find_input_by_label, find_button_by_text
from curso_helper import garantir_curso_existe, garantir_video_existe

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestCT06EdicaoVideo(unittest.TestCase):
    """
    CT-06 - Edição de Vídeos
    
    Requisito: RF06 - O sistema deve permitir a edição de vídeos cadastrados
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    edite as informações de um vídeo existente em um curso.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir um curso com pelo menos um vídeo cadastrado
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados para edição
    NOVO_TITULO = "Vídeo Editado Automaticamente"
    NOVA_URL = "https://www.youtube.com/watch?v=9bZkp7q19f0"
    
    # Dados fallback (caso precise criar curso/vídeo)
    NOME_CURSO_FALLBACK = "Curso para Teste de Vídeo"
    TITULO_VIDEO_FALLBACK = "Vídeo Inicial para Teste"
    URL_VIDEO_FALLBACK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-06 - EDIÇÃO DE VÍDEO")
        print("="*70)
        
        options = get_chrome_options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        # Screenshot counter gerenciado automaticamente
    
    def tearDown(self):
        """Finalização do teste"""
        print("\n" + "-"*70)
        print("Finalizando CT-06")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct06_edicao_video(self):
        """
        Objetivo: Verificar se o sistema permite editar um vídeo existente
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        verificar_login(self.driver, self.wait)
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2: Navegar para Gerenciamento
        print("\n[PASSO 2] Navegando para Gerenciamento de Cursos...")
        try:
            profile_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
                )
            )
            self.driver.execute_script("arguments[0].click();", profile_button)
            time.sleep(1)
            
            gerenciamento_item = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")
                )
            )
            gerenciamento_item.click()
            self.wait.until(EC.url_contains("/manage-courses"))
            time.sleep(2)
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_gerenciamento")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 3: Verificar se existe curso, se não criar um
        print("\n[PASSO 3] Verificando se existe curso...")
        try:
            garantir_curso_existe(
                self.driver,
                self.wait,
                self.NOME_CURSO_FALLBACK,
                "Curso criado automaticamente para testar edição de vídeo",
                self.URL_BASE
            )
            
            print("\n[PASSO 3.1] Selecionando curso...")
            botao_gerenciar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[contains(., 'Gerenciar Curso')])[1]")
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_gerenciar)
            time.sleep(1)
            botao_gerenciar.click()
            time.sleep(3)
            
            print("✓ Curso acessado")
            
            # PASSO 3.2: Verificar se existe vídeo, se não criar um
            print("\n[PASSO 3.2] Verificando se existe vídeo...")
            garantir_video_existe(
                self.driver,
                self.wait,
                self.TITULO_VIDEO_FALLBACK,
                self.URL_VIDEO_FALLBACK
            )
            
            print("✓ Vídeo disponível para edição")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_curso")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 4: Garantir que estamos na aba de vídeos (se necessário)
        print("\n[PASSO 4] Verificando aba de Vídeos...")
        try:
            # garantir_video_existe() já nos deixa na aba de vídeos
            # Apenas scroll e screenshot
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 2, "aba_videos_antes_edicao")
            print("✓ Na aba de vídeos")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_aba")
            self.fail(f"FALHA ao verificar aba: {e}")
        
        # PASSO 5: Clicar no ícone de edição do primeiro vídeo
        print("\n[PASSO 5] Clicando no ícone de edição...")
        try:
            # Procura por botões de ação (ícones) na área de vídeos
            # Os botões de editar/deletar são MuiIconButton sem texto
            todos_botoes = self.driver.find_elements(By.TAG_NAME, "button")
            botoes_visiveis = [b for b in todos_botoes if b.is_displayed()]
            
            botao_editar = None
            
            # Procura botões vazios (ícones) que estão na área de vídeos (Y > 250)
            for botao in botoes_visiveis:
                try:
                    texto = botao.text.strip()
                    loc = botao.location
                    aria = botao.get_attribute("aria-label") or ""
                    
                    # Botão de ação: sem texto, na área de conteúdo, não é do header
                    if not texto and loc['y'] > 250 and "Configurações" not in aria and "Menu" not in aria:
                        # Verifica se tem algum ícone filho (svg, ou classe com ícone)
                        tem_icone = len(botao.find_elements(By.XPATH, ".//*[name()='svg' or @class[contains(., 'icon') or contains(., 'Icon')]]")) > 0
                        if tem_icone or len(botao.find_elements(By.TAG_NAME, "svg")) > 0:
                            botao_editar = botao
                            break
                except:
                    continue
            
            if not botao_editar:
                raise Exception("Nenhum ícone de edição encontrado")
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_editar)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", botao_editar)
            print("✓ Ícone de edição clicado")
            
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 3, "modal_edicao_video_aberto")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_abrir_edicao")
            self.fail(f"FALHA ao abrir edição: {e}")
        
        # PASSO 6: Editar título do vídeo
        print("\n[PASSO 6] Editando título do vídeo...")
        try:
            # Scroll para o topo
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Busca pelo label exato "Título do Vídeo"
            campo_titulo = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[contains(text(), 'Título do Vídeo')]/following-sibling::div//input")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_titulo)
            time.sleep(1)
            campo_titulo.click()
            time.sleep(0.5)
            campo_titulo.clear()
            time.sleep(0.5)
            campo_titulo.send_keys(self.NOVO_TITULO)
            time.sleep(1)
            
            print(f"✓ Título alterado para: '{self.NOVO_TITULO}'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_editar_titulo")
            self.fail(f"FALHA ao editar título: {e}")
        
        # PASSO 7: Editar URL do vídeo
        print("\n[PASSO 7] Editando URL do vídeo...")
        try:
            # Busca pelo label exato "URL do Vídeo"
            campo_url = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[contains(text(), 'URL do Vídeo')]/following-sibling::div//input")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_url)
            time.sleep(1)
            campo_url.click()
            time.sleep(0.5)
            campo_url.clear()
            time.sleep(0.5)
            campo_url.send_keys(self.NOVA_URL)
            time.sleep(1)
            
            print("✓ URL atualizada")
            
            take_evidence(self.driver, self.id(), 4, "formulario_video_editado")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_editar_url")
            self.fail(f"FALHA ao editar URL: {e}")
        
        # PASSO 8: Clicar em "Editar Vídeo"
        print("\n[PASSO 8] Clicando em 'Editar Vídeo'...")
        try:
            botao_editar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Editar Vídeo')]")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_editar)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", botao_editar)
            print("✓ Botão 'Editar Vídeo' clicado")
            
            time.sleep(2)
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_clicar_editar_video")
            self.fail(f"FALHA ao clicar em 'Editar Vídeo': {e}")
        
        # PASSO 9: Clicar em "Salvar Curso"
        print("\n[PASSO 9] Salvando curso...")
        try:
            # Scroll para o topo onde geralmente fica o botão Salvar Curso
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            botao_salvar_curso = find_button_by_text(self.driver, self.wait, "salvar")
            
            if not botao_salvar_curso:
                raise Exception("Botão 'Salvar Curso' não encontrado")
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_salvar_curso)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", botao_salvar_curso)
            print("✓ Botão 'Salvar Curso' clicado")
            
            time.sleep(3)
            
            # Fechar modal de sucesso se aparecer
            try:
                botao_ok = find_button_by_text(self.driver, self.wait, "ok")
                if botao_ok:
                    self.driver.execute_script("arguments[0].click();", botao_ok)
                    time.sleep(1)
            except:
                pass
            
            take_evidence(self.driver, self.id(), 5, "apos_salvar_curso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_salvar_curso")
            self.fail(f"FALHA ao salvar curso: {e}")
        
        # PASSO 10: Verificar se alterações foram salvas
        print("\n[PASSO 10] Verificando se vídeo foi editado...")
        try:
            time.sleep(2)
            
            video_editado = self.driver.find_element(
                By.XPATH,
                f"//*[contains(text(), '{self.NOVO_TITULO}')]"
            )
            
            if video_editado:
                print(f"✓ SUCESSO: Vídeo editado encontrado com título '{self.NOVO_TITULO}'!")
                
                take_evidence(self.driver, self.id(), 6, "video_editado_verificado")
                
                self.assertTrue(True, "Vídeo editado com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_edicao")
            self.fail(f"FALHA: Alterações não foram salvas: {e}")
        
        print("\n" + "="*70)
        print("CT-06 - EDIÇÃO DE VÍDEO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
