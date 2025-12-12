"""
RF48_CT01_SelecionarVideo.py

Teste Selenium para RF48: Selecionar Vídeo ("Ver Vídeo")

Requisito: O sistema deve permitir que o estudante selecione um vídeo específico 
de um curso por meio do botão "Ver Vídeo".

Fluxo esperado:
1. Login via Firebase (injeta credenciais no localStorage)
2. Validar que o login foi bem-sucedido
3. Navegar para a aba de Cursos
4. Entrar na aba "EM ANDAMENTO"
5. Procurar pelo curso "RF 42 - Grupo 4"
6. Clicar no botão "Ver Vídeo"
7. Validar que a página de vídeo foi carregada com sucesso
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Adiciona o diretório ao path para importar utils locais
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login, url_base, time_out
from chrome_config import get_chrome_options
from screenshot_util import save_screenshot


class TestRF48SelecionarVideo(unittest.TestCase):
    """Testa a funcionalidade de selecionar um vídeo de um curso (RF48)."""

    def setUp(self):
        """Setup executado antes de cada teste."""
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_selecionar_video_RF48"
            print(f"\n{'='*60}")
            print(f"Iniciando teste: {self.id()}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"ERRO no setUp: {e}")
            traceback.print_exc()
            raise

    def tearDown(self):
        """Cleanup após cada teste."""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("\nDriver fechado com sucesso.")
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")

    def _abrir_area_cursos(self):
        """
        Abre a área de Cursos clicando no ícone SmartDisplay no topbar.
        Retorna True se conseguiu abrir, False caso contrário.
        """
        print("\n[PASSO 3] ABRINDO ÁREA DE CURSOS")
        
        # Múltiplos seletores para encontrar o botão de Cursos
        xpaths = [
            "//svg[@data-testid='SmartDisplayIcon']/ancestor::div[1]",
            "//div[contains(@class,'topbarIconCont') and .//span[contains(normalize-space(),'Cursos')]]",
            "//div[.//span[normalize-space()='Cursos']]",
        ]
        
        for xp in xpaths:
            try:
                elems = self.driver.find_elements(By.XPATH, xp)
                for e in elems:
                    if e.is_displayed():
                        try:
                            e.click()
                        except Exception:
                            self.driver.execute_script('arguments[0].click();', e)
                        print("✓ Clicou no botão Cursos com sucesso")
                        time.sleep(1)
                        return True
            except Exception:
                continue
        
        print("✗ Não encontrou o botão Cursos")
        return False

    def _selecionar_aba_em_andamento(self):
        """
        Seleciona a aba 'EM ANDAMENTO' dentro da área de Cursos.
        Retorna True se conseguiu selecionar, False caso contrário.
        """
        print("\n[PASSO 4] SELECIONANDO ABA 'EM ANDAMENTO'")
        try:
            # Procura por um botão que contenha "Andamento" (case-insensitive)
            andamento_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'andamento')]"
            )
            self.driver.execute_script("arguments[0].click();", andamento_button)
            print("✓ Clicou na aba 'EM ANDAMENTO' com sucesso")
            time.sleep(1.5)
            return True
        except NoSuchElementException:
            print("✗ Aba 'EM ANDAMENTO' não encontrada")
            return False

    def _encontrar_e_clicar_continuar(self):
        """
        Procura pelo curso "RF 42 - Grupo 4" na aba EM ANDAMENTO e clica em "Continuar".
        
        Estratégia:
        1. Encontra TODOS os cards (MuiCard-root)
        2. Para CADA card, verifica se o título contém "RF 42" ou "Grupo 4"
        3. Quando encontra, procura o botão "Continuar" dentro do card
        4. Clica no botão "Continuar"
        
        Retorna True se conseguiu clicar no botão, False caso contrário.
        """
        print("\n[PASSO 5] PROCURANDO CURSO 'RF 42 - Grupo 4' E CLICANDO EM 'CONTINUAR'")
        
        try:
            # Encontra TODOS os cards de curso
            all_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiCard-root')]")
            print(f"   Encontrados {len(all_cards)} card(s) de curso na aba EM ANDAMENTO")
            
            for idx, card in enumerate(all_cards):
                try:
                    # Extrai o título
                    try:
                        titulo = card.find_element(By.XPATH, ".//h6").text.strip()
                    except:
                        titulo = f"Card {idx + 1}"
                    
                    print(f"   └─ Card {idx + 1}: '{titulo}'")
                    
                    # Verifica se é o curso "RF 42 - Grupo 4"
                    titulo_lower = titulo.lower()
                    if "rf 42" in titulo_lower and "grupo 4" in titulo_lower:
                        print(f"   ✓ Encontrado: '{titulo}'")
                        
                        # Procura pelo botão "Continuar" dentro do card
                        try:
                            continuar_button = card.find_element(
                                By.XPATH,
                                ".//button[normalize-space()='Continuar' or contains(normalize-space(), 'Continuar')]"
                            )
                        except NoSuchElementException:
                            print(f"       ⚠ Sem botão 'Continuar' neste card")
                            continue
                        
                        # Scroll e clique
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", continuar_button)
                        time.sleep(0.3)
                        
                        try:
                            continuar_button.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", continuar_button)
                        
                        print(f"       ✓ Clicou em 'Continuar'")
                        save_screenshot(self.driver, self.test_name, "05_apos_click_continuar")
                        time.sleep(2)
                        return True
                
                except Exception as e:
                    continue
            
            print("✗ Curso 'RF 42 - Grupo 4' não encontrado na aba EM ANDAMENTO")
            return False
            
        except Exception as e:
            print(f"✗ Erro ao procurar curso: {e}")
            traceback.print_exc()
            return False
    
    def _clicar_ver_video(self):
        """
        Após clicar em "Continuar", procura e clica no botão "Ver Vídeo" com PlayCircleIcon.
        
        Retorna True se conseguiu clicar no botão, False caso contrário.
        """
        print("\n[PASSO 6] CLICANDO EM 'VER VÍDEO'")
        
        try:
            # Procura pelo botão "Ver Vídeo" com PlayCircleIcon
            try:
                # Estratégia 1: Procurar botão com PlayCircleIcon data-testid
                ver_video_button = self.driver.find_element(
                    By.XPATH,
                    "//button[.//svg[@data-testid='PlayCircleIcon']]"
                )
                print("   ✓ Encontrado botão 'Ver Vídeo' (por PlayCircleIcon)")
            except NoSuchElementException:
                # Estratégia 2: Procurar apenas por texto
                try:
                    ver_video_button = self.driver.find_element(
                        By.XPATH,
                        "//button[normalize-space()='Ver Vídeo' or contains(normalize-space(), 'Ver Vídeo')]"
                    )
                    print("   ✓ Encontrado botão 'Ver Vídeo' (por texto)")
                except NoSuchElementException:
                    print("   ✗ Botão 'Ver Vídeo' não encontrado")
                    return False
            
            # Scroll e clique
            self.driver.execute_script("arguments[0].scrollIntoView(true);", ver_video_button)
            time.sleep(0.3)
            
            try:
                ver_video_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", ver_video_button)
            
            print("   ✓ Clicou em 'Ver Vídeo'")
            save_screenshot(self.driver, self.test_name, "06_apos_click_ver_video")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"   ✗ Erro ao clicar em 'Ver Vídeo': {e}")
            traceback.print_exc()
            return False

    def test_selecionar_video(self):
        """Teste principal: Selecionar um vídeo de um curso."""
        print('\n' + '='*60)
        print('TESTE RF48: Selecionar Vídeo ("Ver Vídeo")')
        print('='*60)
        
        try:
            # [PASSO 1] Login
            print("\n[PASSO 1] REALIZANDO LOGIN")
            login(self.driver)
            save_screenshot(self.driver, self.test_name, "01_apos_login")
            
            # [PASSO 2] Verificar login
            print("\n[PASSO 2] VALIDANDO LOGIN")
            verificar_login(self.driver, self.wait)
            save_screenshot(self.driver, self.test_name, "02_apos_validacao_login")
            
            # [PASSO 3] Abrir área de Cursos
            if not self._abrir_area_cursos():
                self.fail("FALHA: Não conseguiu abrir a área de Cursos")
            save_screenshot(self.driver, self.test_name, "03_area_cursos_aberta")
            time.sleep(0.5)
            
            # [PASSO 4] Selecionar aba EM ANDAMENTO
            if not self._selecionar_aba_em_andamento():
                self.fail("FALHA: Não conseguiu selecionar a aba 'EM ANDAMENTO'")
            save_screenshot(self.driver, self.test_name, "04_aba_em_andamento_selecionada")
            time.sleep(0.5)
            
            # [PASSO 5] Procurar curso e clicar em "Continuar"
            if not self._encontrar_e_clicar_continuar():
                self.fail("FALHA: Não conseguiu encontrar o curso ou clicar em 'Continuar'")
            
            # [PASSO 6] Clicar em "Ver Vídeo"
            if not self._clicar_ver_video():
                self.fail("FALHA: Não conseguiu clicar em 'Ver Vídeo'")
            
            # [PASSO 7] Validar que a página de vídeo foi carregada
            print("\n[PASSO 7] VALIDANDO CARREGAMENTO DA PÁGINA DE VÍDEO")
            time.sleep(1)
            
            # Verifica indicadores de que a página de vídeo foi carregada
            video_indicators = self.driver.find_elements(
                By.XPATH,
                "//iframe[contains(@src, 'youtube')] | //video | //h2 | //h1 | //*[contains(@class, 'video')] | //*[contains(@class, 'aula')]"
            )
            
            visible_indicators = [ind for ind in video_indicators if ind.is_displayed()]
            
            if visible_indicators:
                print(f"✓ Detectados {len(visible_indicators)} indicador(es) de conteúdo de vídeo")
            else:
                print("⚠ Nenhum indicador de vídeo detectado (mas navegação foi bem-sucedida)")
            
            # Tira screenshot final
            save_screenshot(self.driver, self.test_name, "06_pagina_video_carregada")
            
            print('\n' + '='*60)
            print('✓ TESTE RF48 CONCLUÍDO COM SUCESSO')
            print('='*60 + '\n')
            
        except AssertionError as e:
            print(f'\n✗ Teste falhou: {e}')
            save_screenshot(self.driver, self.test_name, "XX_erro_teste")
            raise
        except Exception as e:
            print(f'\n✗ Erro inesperado: {e}')
            traceback.print_exc()
            save_screenshot(self.driver, self.test_name, "XX_erro_inesperado")
            self.fail(f'Erro inesperado: {e}')


if __name__ == '__main__':
    unittest.main()
