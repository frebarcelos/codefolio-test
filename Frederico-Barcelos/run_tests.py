import tkinter as tk
from tkinter import ttk, scrolledtext
import unittest
import sys
import os
import re
import threading
from io import StringIO

class TextRedirector(StringIO):
    """Um objeto 'file-like' para redirecionar o output para um widget de texto do Tkinter."""
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def write(self, string):
        # Garante que a atualização do widget seja feita na thread principal do Tkinter
        self.widget.after(0, self._insert_text, string)

    def _insert_text(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

class TestRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Executor de Testes")
        self.root.geometry("800x600")

        # Adiciona o diretório atual ao path para encontrar módulos locais
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

        # --- Widgets ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para os controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        ttk.Label(controls_frame, text="Selecionar Teste:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.test_combobox = ttk.Combobox(controls_frame, state="readonly", width=50)
        self.test_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.run_selected_button = ttk.Button(controls_frame, text="Rodar Selecionado", command=self.on_run_selected)
        self.run_selected_button.pack(side=tk.LEFT, padx=5)

        self.run_all_button = ttk.Button(controls_frame, text="Rodar Todos", command=self.on_run_all)
        self.run_all_button.pack(side=tk.LEFT, padx=5)

        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(controls_frame, text="Rodar em modo Headless", variable=self.headless_var)
        headless_check.pack(side=tk.LEFT, padx=15)

        # Terminal
        self.terminal = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, bg="black", fg="white", font=("Consolas", 20))
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=5)

        self.load_tests()

    def _get_test_map(self, suite):
        """Extrai um mapa de {nome_exibicao: id_completo} de uma TestSuite."""
        test_map = {}
        if hasattr(suite, '__iter__'):
            for test in suite:
                test_map.update(self._get_test_map(test))
        else:
            full_id = suite.id()
            method_name = full_id.split('.')[-1]
            
            # Cria o nome de exibição formatado
            display_name = re.sub(r'^test_\d+_', '', method_name).replace('_', ' ').capitalize()
            
            # Adiciona o mapeamento do nome amigável para o ID completo
            test_map[display_name] = full_id
        return test_map

    def load_tests(self):
        """Descobre e carrega os testes, criando um mapa de nomes amigáveis."""
        loader = unittest.TestLoader()
        self.full_suite = loader.discover('.')
        
        self.test_map = self._get_test_map(self.full_suite)
        test_names = sorted(self.test_map.keys()) # Ordena para uma exibição consistente
        
        if test_names:
            self.test_combobox['values'] = test_names
            self.test_combobox.current(0)
        else:
            self.test_combobox['values'] = ["Nenhum teste encontrado"]
            self.test_combobox.current(0)
            self.run_selected_button.config(state=tk.DISABLED)
            self.run_all_button.config(state=tk.DISABLED)

    def run_tests_in_thread(self, suite):
        """Inicia a execução dos testes em uma nova thread para não bloquear a GUI."""
        self.run_selected_button.config(state=tk.DISABLED)
        self.run_all_button.config(state=tk.DISABLED)
        self.terminal.delete('1.0', tk.END)

        thread = threading.Thread(target=self.execute_tests, args=(suite,))
        thread.start()
        self.check_thread(thread)

    def check_thread(self, thread):
        """Verifica se a thread de testes terminou e reativa os botões."""
        if thread.is_alive():
            self.root.after(100, lambda: self.check_thread(thread))
        else:
            self.run_selected_button.config(state=tk.NORMAL)
            self.run_all_button.config(state=tk.NORMAL)

    def execute_tests(self, suite):
        """Executa a suíte de testes e redireciona o output para o terminal da GUI."""
        if self.headless_var.get():
            os.environ['HEADLESS_MODE'] = '1'
        elif 'HEADLESS_MODE' in os.environ:
            del os.environ['HEADLESS_MODE']

        redirector = TextRedirector(self.terminal)
        
        # Salva o stdout e stderr originais
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Redireciona
        sys.stdout = redirector
        sys.stderr = redirector
        
        try:
            runner = unittest.TextTestRunner(stream=redirector, verbosity=2)
            runner.run(suite)
        finally:
            # Restaura o stdout e stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def on_run_selected(self):
        """Callback para o botão 'Rodar Selecionado'."""
        display_name = self.test_combobox.get()
        if display_name and display_name != "Nenhum teste encontrado":
            # Usa o mapa para encontrar o ID completo do teste a partir do nome de exibição
            full_id = self.test_map[display_name]
            
            suite = unittest.TestSuite()
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(full_id))
            self.run_tests_in_thread(suite)

    def on_run_all(self):
        """Callback para o botão 'Rodar Todos'."""
        self.run_tests_in_thread(self.full_suite)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestRunnerApp(root)
    root.mainloop()