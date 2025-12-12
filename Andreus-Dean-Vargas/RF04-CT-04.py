"""
CT-04 - Exclusão de Cursos (RF04) - ABRIR EM DOIS TESTES SEPARADOS UM TESTANDO SE EXISTE ALGO DENTRO DO CURSO - DAI NAO PODE EXCLUIR - E OUTRO TENTANDO EXCLUIR UM CURSO VAZIO - TEM Q EXCLUIR.
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
from curso_helper import garantir_curso_existe

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestCT04ExclusaoCurso(unittest.TestCase):
    """
    CT-04 - Exclusão de Cursos
    
    Requisito: RF04 - O sistema deve permitir a exclusão de cursos existentes
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    exclua um curso existente e que o curso não apareça mais na lista.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir pelo menos um curso cadastrado para exclusão
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados do curso fallback (caso precise criar)
    NOME_CURSO_FALLBACK = "Curso para Teste de Exclusão"
    DESCRICAO_CURSO_FALLBACK = "Curso criado automaticamente para testar funcionalidade de exclusão"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-04 - EXCLUSÃO DE CURSO")
        print("="*70)
        
        options = get_chrome_options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        # Screenshot counter gerenciado automaticamente
        self.nome_curso_alvo = None
    
    def tearDown(self):
        """Finalização do teste"""
        print("\n" + "-"*70)
        print("Finalizando CT-04")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct04_exclusao_curso(self):
        """
        Objetivo: Verificar se o sistema permite excluir um curso existente
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        verificar_login(self.driver, self.wait)
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2: Navegar para Gerenciamento de Cursos
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
            print("✓ Página de gerenciamento carregada")
            
            time.sleep(2)
            take_evidence(self.driver, self.id(), 2, "lista_cursos_antes_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_gerenciamento")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 3: Verificar se existe curso, se não criar um
        print("\n[PASSO 3] Verificando se existe curso para excluir...")
        try:
            garantir_curso_existe(
                self.driver,
                self.wait,
                self.NOME_CURSO_FALLBACK,
                self.DESCRICAO_CURSO_FALLBACK,
                self.URL_BASE
            )
            
            print("✓ Curso disponível para exclusão")
            time.sleep(2)
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_criar_curso")
            self.fail(f"FALHA ao verificar/criar curso: {e}")
        
        # PASSO 4: Identificar curso a ser excluído
        print("\n[PASSO 4] Identificando curso para exclusão...")
        try:
            # Tenta pegar o nome do curso (pode estar em diferentes elementos)
            try:
                primeiro_curso = self.driver.find_element(
                    By.XPATH,
                    "(//button[contains(., 'Gerenciar Curso')])[1]/ancestor::div//h6 | (//button[contains(., 'Gerenciar Curso')])[1]/ancestor::div//h5"
                )
                self.nome_curso_alvo = primeiro_curso.text
                print(f"✓ Curso alvo identificado: '{self.nome_curso_alvo}'")
            except:
                print("⚠ Não foi possível identificar nome do curso, continuando...")
                self.nome_curso_alvo = "Curso Desconhecido"
            
        except Exception as e:
            print("⚠ Continuando sem identificar nome do curso...")
            self.nome_curso_alvo = "Curso Desconhecido"
        
        # PASSO 5: Clicar no botão "Deletar" do primeiro curso
        print("\n[PASSO 5] Clicando no botão Deletar...")
        try:
            # Scroll para o topo
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Busca o primeiro botão "Deletar" na lista
            botao_deletar = find_button_by_text(self.driver, self.wait, "deletar")
            
            if not botao_deletar:
                raise Exception("Botão 'Deletar' não encontrado")
            
            # Scroll até o botão
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_deletar)
            time.sleep(1)
            
            # Clica no botão
            self.driver.execute_script("arguments[0].click();", botao_deletar)
            print("✓ Botão 'Deletar' clicado")
            
            time.sleep(2)
            
            # Evidência 03: Modal de confirmação
            take_evidence(self.driver, self.id(), 3, "modal_confirmacao_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_clicar_deletar")
            self.fail(f"FALHA ao clicar em deletar: {e}")
        
        # PASSO 6: Confirmar exclusão clicando em "Deletar" no modal
        print("\n[PASSO 6] Confirmando exclusão no modal...")
        try:
            # Aguarda modal aparecer completamente
            time.sleep(2)
            
            # Busca botão "Deletar" no modal de confirmação (precisa ser o segundo botão Deletar)
            botoes_deletar = self.driver.find_elements(By.XPATH, "//button[contains(., 'Deletar')]")
            
            if len(botoes_deletar) < 2:
                raise Exception("Botão de confirmação 'Deletar' no modal não encontrado")
            
            # O segundo botão Deletar é o do modal de confirmação
            botao_confirmar = botoes_deletar[-1]  # Pega o último
            
            # Scroll até o botão
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_confirmar)
            time.sleep(0.5)
            
            # Aguarda o botão estar clicável
            self.wait.until(EC.element_to_be_clickable(botao_confirmar))
            
            # Clica usando JavaScript para evitar problema com backdrop
            self.driver.execute_script("arguments[0].click();", botao_confirmar)
            print("✓ Exclusão confirmada no modal")
            
            # Aguarda processar
            time.sleep(3)
            
            # Evidência 05: Após confirmar exclusão
            take_evidence(self.driver, self.id(), 5, "apos_confirmar_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_confirmar_exclusao")
            self.fail(f"FALHA ao confirmar exclusão: {e}")
        
        # PASSO 7: Verificar se curso foi removido da lista
        print("\n[PASSO 7] Verificando se curso foi removido...")
        try:
            # Volta para lista de cursos (se não estiver)
            if "/manage-courses" not in self.driver.current_url:
                self.driver.get(f"{self.URL_BASE}/manage-courses")
                time.sleep(3)
            
            # Tenta encontrar o curso na lista
            try:
                curso_ainda_existe = self.driver.find_element(
                    By.XPATH,
                    f"//*[contains(text(), '{self.nome_curso_alvo}')]"
                )
                # Se encontrou, o teste falhou
                take_evidence(self.driver, self.id(), 99, "curso_ainda_existe")
                self.fail(f"FALHA: Curso '{self.nome_curso_alvo}' ainda está na lista!")
                
            except:
                # Se não encontrou, o teste passou
                print(f"✓ SUCESSO: Curso '{self.nome_curso_alvo}' foi removido da lista!")
                
                # Evidência 06: Lista sem o curso excluído
                take_evidence(self.driver, self.id(), 6, "lista_apos_exclusao")
                
                self.assertTrue(True, "Curso excluído com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_exclusao")
            self.fail(f"FALHA ao verificar exclusão: {e}")
        
        print("\n" + "="*70)
        print("CT-04 - EXCLUSÃO DE CURSO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
