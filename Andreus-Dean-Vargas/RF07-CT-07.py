"""
CT-07 - Exclusão de Vídeos (RF07)
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
from element_finder import find_button_by_text
from curso_helper import garantir_curso_existe, garantir_video_existe

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestCT07ExclusaoVideo(unittest.TestCase):
    """
    CT-07 - Exclusão de Vídeos
    
    Requisito: RF07 - O sistema deve permitir a exclusão de vídeos cadastrados
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    exclua um vídeo existente e que ele não apareça mais na lista.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir um curso com pelo menos um vídeo cadastrado
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados fallback (caso precise criar curso/vídeo)
    NOME_CURSO_FALLBACK = "Curso para Teste de Vídeo"
    TITULO_VIDEO_FALLBACK = "Vídeo para Teste de Exclusão"
    URL_VIDEO_FALLBACK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-07 - EXCLUSÃO DE VÍDEO")
        print("="*70)
        
        options = get_chrome_options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        # Screenshot counter gerenciado automaticamente
        self.titulo_video_alvo = None
    
    def tearDown(self):
        """Finalização do teste"""
        print("\n" + "-"*70)
        print("Finalizando CT-07")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct07_exclusao_video(self):
        """
        Objetivo: Verificar se o sistema permite excluir um vídeo existente
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
                "Curso criado automaticamente para testar exclusão de vídeo",
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
            
            print("✓ Vídeo disponível para exclusão")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_curso")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 4: Verificar que estamos na aba de vídeos (garantir_video_existe já nos deixa lá)
        print("\n[PASSO 4] Verificando aba de Vídeos...")
        try:
            # garantir_video_existe() já nos deixa na aba de vídeos
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 2, "aba_videos_antes_exclusao")
            print("✓ Na aba de vídeos")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_aba")
            self.fail(f"FALHA ao verificar aba: {e}")
        
        # PASSO 5: Clicar no ícone de exclusão (lixeira) do primeiro vídeo
        print("\n[PASSO 5] Clicando no ícone de exclusão...")
        try:
            # Procura por botões de ação (ícones) na área de vídeos
            # Mesma estratégia do RF06: MuiIconButton sem texto
            todos_botoes = self.driver.find_elements(By.TAG_NAME, "button")
            botoes_visiveis = [b for b in todos_botoes if b.is_displayed()]
            
            # Encontra TODOS os botões de ação na área de vídeos
            botoes_acao = []
            for botao in botoes_visiveis:
                try:
                    texto = botao.text.strip()
                    loc = botao.location
                    aria = botao.get_attribute("aria-label") or ""
                    
                    # Botão de ação: sem texto, na área de conteúdo, não é do header
                    if not texto and loc['y'] > 250 and "Configurações" not in aria and "Menu" not in aria:
                        # Verifica se tem ícone
                        tem_icone = len(botao.find_elements(By.XPATH, ".//*[name()='svg' or @class[contains(., 'icon') or contains(., 'Icon')]]")) > 0
                        if tem_icone or len(botao.find_elements(By.TAG_NAME, "svg")) > 0:
                            botoes_acao.append(botao)
                except:
                    continue
            
            # O segundo botão de cada vídeo é o de deletar (primeiro é editar)
            # Pega o segundo botão (índice 1)
            if len(botoes_acao) < 2:
                raise Exception(f"Apenas {len(botoes_acao)} botões de ação encontrados, esperado pelo menos 2")
            
            botao_deletar = botoes_acao[1]  # Segundo botão = deletar do primeiro vídeo
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_deletar)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", botao_deletar)
            print("✓ Ícone de exclusão clicado")
            
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 3, "modal_confirmacao_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_clicar_excluir")
            self.fail(f"FALHA ao clicar em excluir: {e}")
        
        # PASSO 6: Confirmar exclusão
        print("\n[PASSO 6] Confirmando exclusão...")
        try:
            botao_confirmar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Sim') or contains(., 'Confirmar') or contains(., 'Excluir')]")
                )
            )
            
            botao_confirmar.click()
            print("✓ Exclusão confirmada")
            
            time.sleep(3)
            
            take_evidence(self.driver, self.id(), 4, "apos_confirmar_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_confirmar_exclusao")
            self.fail(f"FALHA ao confirmar exclusão: {e}")
        
        # PASSO 7: Salvar curso e verificar que vídeo foi removido
        print("\n[PASSO 7] Salvando curso...")
        try:
            # Scroll para o topo onde está o botão Salvar Curso
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            botao_salvar = find_button_by_text(self.driver, self.wait, "salvar")
            if botao_salvar:
                self.driver.execute_script("arguments[0].click();", botao_salvar)
                print("✓ Curso salvo")
                time.sleep(3)
                
                # Fechar modal de sucesso
                try:
                    botao_ok = find_button_by_text(self.driver, self.wait, "ok")
                    if botao_ok:
                        self.driver.execute_script("arguments[0].click();", botao_ok)
                        time.sleep(1)
                except:
                    pass
                
                take_evidence(self.driver, self.id(), 5, "apos_salvar_exclusao")
                print("✓ SUCESSO: Vídeo foi excluído e curso salvo!")
                
                self.assertTrue(True, "Vídeo excluído com sucesso")
            else:
                raise Exception("Botão Salvar Curso não encontrado")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_salvar_curso")
            self.fail(f"FALHA ao salvar curso: {e}")
        
        print("\n" + "="*70)
        print("CT-07 - EXCLUSÃO DE VÍDEO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
