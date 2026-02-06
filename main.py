# ===================== main.py (CORRIGIDO E FUNCIONAL ANDROID) =====================

import os
import json
import uuid
import hashlib
from datetime import datetime, timedelta

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton

# ===================== ANDROID STORAGE =====================
try:
    from android.storage import app_storage_path
    BASE_DIR = app_storage_path()
except:
    BASE_DIR = os.getcwd()

# ===================== CORES =====================
FUNDO = (0.96, 0.96, 1, 1)
PURPLE = (0.6, 0.4, 0.8, 1)
LIGHT_PURPLE = (0.8, 0.7, 0.9, 1)
BLACK = (0.15, 0.15, 0.2, 1)
TEXTO = (0.1, 0.1, 0.2, 1)

# ===================== ARQUIVOS =====================
ARQS = {
    "usuarios": os.path.join(BASE_DIR, "usuarios.json"),
    "diario": os.path.join(BASE_DIR, "diario.json"),
    "consultas": os.path.join(BASE_DIR, "consultas.json"),
    "medicamentos": os.path.join(BASE_DIR, "medicamentos.json"),
    "crises": os.path.join(BASE_DIR, "crises.json"),
    "atividades": os.path.join(BASE_DIR, "atividades.json"),
    "alimentacao": os.path.join(BASE_DIR, "alimentacao.json")
}

# ===================== UTIL =====================
def carregar(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar(path, dados):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ===================== UI =====================
class BotaoBonito(ButtonBehavior, Widget):
    def __init__(self, texto="", on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, None)
        self.height = 45
        self._callback = on_release or (lambda *_: None)

        with self.canvas.before:
            Color(*LIGHT_PURPLE)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[22])

        self.lbl = Label(text=texto, color=TEXTO)
        self.add_widget(self.lbl)

        self.bind(pos=self.update, size=self.update)

    def update(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.lbl.pos = self.pos
        self.lbl.size = self.size

    def on_release(self):
        self._callback(self)

# ===================== TELAS =====================
class Login(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        box.add_widget(Label(text="Login"))
        box.add_widget(BotaoBonito("Entrar", on_release=lambda *_: setattr(self.manager, "current", "principal")))
        self.add_widget(box)

class Cadastro(Screen):
    pass

class Principal(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        box.add_widget(Label(text="Menu Principal"))
        box.add_widget(BotaoBonito("Diário", on_release=lambda *_: setattr(self.manager, "current", "diario")))
        box.add_widget(BotaoBonito("Atividades", on_release=lambda *_: setattr(self.manager, "current", "atividades")))
        box.add_widget(BotaoBonito("Análise", on_release=lambda *_: setattr(self.manager, "current", "analise")))
        self.add_widget(box)

class Diario(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.txt = TextInput(multiline=True)
        box.add_widget(self.txt)
        box.add_widget(BotaoBonito("Salvar", on_release=self.salvar))
        box.add_widget(BotaoBonito("Voltar", on_release=lambda *_: setattr(self.manager, "current", "principal")))
        self.add_widget(box)

    def salvar(self, *_):
        dados = carregar(ARQS["diario"])
        dados.append({"data": datetime.now().strftime("%d/%m/%Y"), "texto": self.txt.text})
        salvar(ARQS["diario"], dados)
        self.txt.text = ""

class Atividades(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        box.add_widget(Label(text="Atividades"))
        box.add_widget(BotaoBonito("Registrar", on_release=lambda *_: setattr(self.manager, "current", "registrar_atividade")))
        box.add_widget(BotaoBonito("Voltar", on_release=lambda *_: setattr(self.manager, "current", "principal")))
        self.add_widget(box)

class RegistrarAtividade(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.nome = TextInput(hint_text="Nome")
        box.add_widget(self.nome)
        box.add_widget(BotaoBonito("Salvar", on_release=self.salvar))
        box.add_widget(BotaoBonito("Voltar", on_release=lambda *_: setattr(self.manager, "current", "atividades")))
        self.add_widget(box)

    def salvar(self, *_):
        dados = carregar(ARQS["atividades"])
        dados.append({"nome": self.nome.text, "data": datetime.now().strftime("%d/%m/%Y")})
        salvar(ARQS["atividades"], dados)
        self.nome.text = ""

class TelaAnalise(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        box.add_widget(Label(text="Análise últimos 7 dias"))

        hoje = datetime.now()
        for i in range(7):
            dia = (hoje - timedelta(days=i)).strftime("%d/%m/%Y")
            crises = len([c for c in carregar(ARQS["crises"]) if c.get("data") == dia])
            atividades = len([a for a in carregar(ARQS["atividades"]) if a.get("data") == dia])
            box.add_widget(Label(text=f"{dia} | Crises: {crises} | Atividades: {atividades}"))

        box.add_widget(BotaoBonito("Voltar", on_release=lambda *_: setattr(self.manager, "current", "principal")))
        self.add_widget(box)

# ===================== APP =====================
class MeuApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(Login(name="login"))
        sm.add_widget(Cadastro(name="cadastro"))
        sm.add_widget(Principal(name="principal"))
        sm.add_widget(Diario(name="diario"))
        sm.add_widget(Atividades(name="atividades"))
        sm.add_widget(RegistrarAtividade(name="registrar_atividade"))
        sm.add_widget(TelaAnalise(name="analise"))
        sm.current = "login"
        return sm

if __name__ == "__main__":
    MeuApp().run()
