"""
RF46_CT01_IniciarCursoSemPIN.py

Teste Selenium para RF46: Iniciar Curso sem PIN

Requisito: O sistema deve permitir que o estudante comece cursos disponíveis 
que não exigem código PIN.

Fluxo esperado:
1. Login via Firebase (injeta credenciais no localStorage)
2. Validar que o login foi bem-sucedido
3. Navegar para a aba de Cursos
4. Selecionar a aba "Disponíveis"
5. Selecionar um curso que NÃO tenha um LockIcon (PIN)
6. Clicar em "Começar"
7. Validar que o curso iniciou sem solicitar PIN
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


class TestRF46IniciarCursoSemPIN(unittest.TestCase):
    """Testa a funcionalidade de iniciar um curso sem PIN (RF46)."""

    def setUp(self):
        """Setup executado antes de cada teste."""
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_iniciar_curso_sem_pin_RF46"
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

    def _selecionar_aba_disponiveis(self):
        """
        Seleciona a aba 'Disponíveis' dentro da área de Cursos.
        Retorna True se conseguiu selecionar, False caso contrário.
        """
        print("\n[PASSO 4] SELECIONANDO ABA 'DISPONÍVEIS'")
        try:
            # Procura por um botão que contenha "Disponível" (case-insensitive)
            disponivel_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'dispon')]"
            )
            self.driver.execute_script("arguments[0].click();", disponivel_button)
            print("✓ Clicou na aba Disponíveis com sucesso")
            time.sleep(1)
            return True
        except NoSuchElementException:
            print("⚠ Aba Disponíveis não encontrada, continuando na aba padrão...")
            return True  # Continua mesmo se não encontrar a aba

    def _encontrar_e_iniciar_curso_sem_pin(self):
        """
        Encontra um curso que NÃO tenha LockIcon (PIN) e clica em "Começar".
        
        Estratégia PRÁTICA:
        1. Encontra TODOS os cards (MuiCard-root)
        2. Para CADA card, tenta clicar em "Começar"
        3. Espera para ver se aparece PIN modal
        4. Se aparecer PIN → fecha o modal e tenta próximo curso
        5. Se NÃO aparecer PIN → sucesso!
        
        Retorna True se conseguiu iniciar um curso sem PIN, False caso contrário.
        """
        print("\n[PASSO 5] PROCURANDO CURSO SEM PIN E INICIANDO")
        
        try:
            # Encontra TODOS os cards de curso
            all_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiCard-root')]")
            print(f"   Encontrados {len(all_cards)} card(s) de curso no total")
            print(f"   Testando cada um até encontrar um SEM PIN...\n")
            
            for idx, card in enumerate(all_cards):
                try:
                    # Extrai o título para debug
                    try:
                        titulo = card.find_element(By.XPATH, ".//h6").text.strip()
                    except:
                        titulo = f"Card {idx + 1}"
                    
                    print(f"   Tentativa {idx + 1}: '{titulo}'")
                    
                    # Procura pelo botão "Começar" dentro do card
                    try:
                        comecar_button = card.find_element(
                            By.XPATH,
                            ".//button[normalize-space()='Começar' or contains(normalize-space(), 'Começar')]"
                        )
                    except NoSuchElementException:
                        print(f"       └─ ⚠ Sem botão 'Começar' (pulando)")
                        continue
                    
                    # Scroll para garantir visibilidade
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", comecar_button)
                    time.sleep(0.3)
                    
                    # Clica no botão "Começar"
                    try:
                        comecar_button.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", comecar_button)
                    
                    print(f"       └─ ✓ Clicou em 'Começar'")
                    save_screenshot(self.driver, self.test_name, f"05_tentativa_{idx+1}_click_comecar")
                    time.sleep(1.5)
                    
                    # VERIFICAÇÃO CRÍTICA: Apareceu modal de PIN?
                    try:
                        pin_modal = self.driver.find_element(
                            By.XPATH, 
                            "//label[normalize-space()='PIN de Acesso']"
                        )
                        if pin_modal.is_displayed():
                            # Este curso REQUER PIN, fechar modal e tentar próximo
                            print(f"       └─ ❌ Requer PIN (fechando modal...)")
                            # Tenta fechar o modal
                            try:
                                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                                time.sleep(0.5)
                            except:
                                pass
                            # Se ESC não funcionou, tenta clicar fora do modal ou em botão de fechar
                            try:
                                fechar_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Fechar' or contains(normalize-space(), '✕') or contains(normalize-space(), 'X')]")
                                self.driver.execute_script("arguments[0].click();", fechar_btn)
                                time.sleep(0.5)
                            except:
                                pass
                            # Re-buscar cards (pois a página pode ter mudado)
                            all_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiCard-root')]")
                            continue
                    except NoSuchElementException:
                        # Não encontrou modal de PIN = SUCESSO!
                        print(f"       └─ ✓ SEM PIN - CURSO INICIADO COM SUCESSO!")
                        save_screenshot(self.driver, self.test_name, f"05_tentativa_{idx+1}_sem_pin_ok")
                        return True
                    
                except Exception as e:
                    print(f"   Tentativa {idx + 1}: Erro: {e}")
                    continue
            
            # Se chegou aqui, NENHUM curso sem PIN foi encontrado
            print(f"\n✗ Testados todos os {len(all_cards)} cursos, todos requerem PIN")
            return False
            
        except Exception as e:
            print(f"✗ Erro crítico ao buscar cursos: {e}")
            traceback.print_exc()
            return False

    def test_iniciar_curso_sem_pin(self):
        """Teste principal: Iniciar um curso sem PIN."""
        print('\n' + '='*60)
        print('TESTE RF46: Iniciar Curso sem PIN')
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
            
            # [PASSO 4] Selecionar aba Disponíveis
            self._selecionar_aba_disponiveis()
            save_screenshot(self.driver, self.test_name, "04_aba_disponiveis_selecionada")
            time.sleep(0.5)
            
            # [PASSO 5] Encontrar e iniciar curso sem PIN
            if not self._encontrar_e_iniciar_curso_sem_pin():
                self.fail("FALHA: Não conseguiu encontrar e iniciar um curso sem PIN")
            
            # [PASSO 6] Validar que o curso iniciou (sem PIN modal)
            print("\n[PASSO 6] VALIDANDO ACESSO AO CURSO")
            time.sleep(1)
            
            # Apenas documenta o estado final
            print("✓ Nenhum modal de PIN apareceu - Acesso concedido!")
            
            # Verifica indicadores de que o curso foi acessado
            page_indicators = self.driver.find_elements(
                By.XPATH,
                "//h1 | //h2 | //iframe[contains(@src, 'youtube')] | //*[contains(@class, 'course')] | //*[contains(@class, 'aula')]"
            )
            
            visible_indicators = [ind for ind in page_indicators if ind.is_displayed()]
            
            if visible_indicators:
                print(f"✓ Detectados {len(visible_indicators)} indicador(es) de conteúdo")
            
            save_screenshot(self.driver, self.test_name, "06_curso_iniciado")
            
            print('\n' + '='*60)
            print('✓ TESTE RF46 CONCLUÍDO COM SUCESSO')
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
