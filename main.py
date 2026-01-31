
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
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from login_cadastro_principal import Login, Cadastro
from crises import RegistrarCrise, SubCrise

# ================== CONFIGURAÇÕES DE JANELA ==================
Window.size = (360, 640)
FUNDO = (0.96, 0.96, 1, 1)
Window.clearcolor = FUNDO

# ================== CORES ==================
PURPLE = (0.6, 0.4, 0.8, 1)
LIGHT_PURPLE = (0.8, 0.7, 0.9, 1)
BLACK = (0.15, 0.15, 0.2, 1)
GREY = (0.5, 0.5, 0.5, 1)
TEXTO = (0.1, 0.1, 0.2, 1)
CARTAO = (0.8, 0.7, 0.95, 1)

# ================== FONTES ==================
FONTE_BOTAO = "fonts/IndieFlower-Regular.ttf"
FONTE_TEXTO = "fonts/NotoSans-Italic-VariableFont_wdth,wght.ttf"

# ================== ARQUIVOS ==================
def carregar(arquivo):
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

ARQS = {
    "usuarios": "usuarios.json",
    "diario": "diario.json",
    "consultas": "consultas.json",
    "medicamentos": "medicamentos.json",
    "crises": "crises.json",
    "atividades": "atividades.json",
    "alimentacao": "alimentacao.json"
}

USERS_FILE = ARQS["usuarios"]
REGISTROS_FILE = ARQS["diario"]
ARQUIVO_CONSULTAS = ARQS["consultas"]
ARQUIVO_CRISES = ARQS["crises"]
MED_FILE = ARQS["medicamentos"]
ARQUIVO_ALIMENTACAO = ARQS["alimentacao"]

SESSAO = {}

CRISES = {
    "Crise Focal": [
        ("Sensorial", "Formigamento, cheiros irreais"),
        ("Motora", "Movimentos involuntários"),
        ("Autonômica", "Náusea, sudorese"),
        ("Psíquica", "Medo, déjà vu, jamais vu")
    ],
    "Crise Focal com Alteração da Consciência": [
        ("Automatismos", "Movimentos repetitivos"),
        ("Confusão", "Desorientação")
    ],
    "Crise Generalizada": [
        ("Tônico-clônica", "Rigidez e abalos"),
        ("Ausência", "Desligamento breve"),
        ("Mioclônica", "Contrações rápidas"),
        ("Atônica", "Perda de força")
    ],
    "Crise Gelástica": [
        ("Riso involuntário", "Riso sem motivo")
    ],
    "Crise Reflexa": [
        ("Fotossensível", "Luz"),
        ("Auditiva", "Som")
    ]
}

# ================= FRASES DO DIÁRIO =================
FRASES_HUMOR = {
    "bom": [
        "Hoje me senti em paz comigo mesma.",
        "Consegui aproveitar pequenas coisas do dia.",
        "Me senti mais leve emocionalmente.",
        "Tive um dia produtivo e tranquilo.",
        "Senti esperança hoje."
    ],
    "neutro": [
        "Foi um dia comum, sem grandes emoções.",
        "Nada muito bom nem muito ruim aconteceu.",
        "Me senti estável ao longo do dia.",
        "O dia passou sem grandes impactos.",
        "Fiquei no automático hoje."
    ],
    "dificil": [
        "Hoje foi emocionalmente pesado.",
        "Me senti sobrecarregada.",
        "Foi difícil lidar com os sentimentos hoje.",
        "Tive momentos de tristeza ou ansiedade.",
        "Não foi um dia fácil."
    ]
}
ALIMENTOS = {
    "Ultraprocessados": [
        "Refrigerante", "Salgadinho", "Biscoito recheado",
        "Macarrão instantâneo", "Nuggets", "Cereal açucarado",
        "Achocolatado", "Sopa instantânea"
    ],
    "Embutidos": [
        "Salsicha", "Presunto", "Mortadela",
        "Salame", "Linguiça", "Peito de peru"
    ],
    "Álcool": [
        "Cerveja", "Vinho", "Vodka",
        "Whisky", "Energético com álcool", "Drink doce"
    ]
}


# ================== FUNÇÕES DE DADOS ==================
def carregar_json(arquivo, padrao):
    if not os.path.exists(arquivo):
        return padrao
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_json(arquivo, dados, indent=2):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=indent)

def carregar_usuarios():
    return carregar_json(USERS_FILE, {})

def salvar_usuarios(dados):
    salvar_json(USERS_FILE, dados, indent=4)

def hash_senha(senha, salt=None):
    if not salt:
        salt = uuid.uuid4().hex
    return hashlib.sha256((senha + salt).encode()).hexdigest(), salt

def carregar_registros_diario():
    return carregar_json(REGISTROS_FILE, [])

def salvar_registros_diario(registro):
    registros = carregar_registros_diario()
    registros.append(registro)
    salvar_json(REGISTROS_FILE, registros)

def carregar_consultas():
    return carregar_json(ARQUIVO_CONSULTAS, [])

def salvar_consultas(dados):
    salvar_json(ARQUIVO_CONSULTAS, dados)

def carregar_crises():
    return carregar_json(ARQUIVO_CRISES, [])

def salvar_crise(registro):
    crises = carregar_crises()
    crises.append(registro)
    salvar_json(ARQUIVO_CRISES, crises)

def carregar_meds():
    return carregar_json(MED_FILE, [])

def salvar_meds(meds):
    salvar_json(MED_FILE, meds, indent=4)

def carregar_alimentacao():
    return carregar_json(ARQUIVO_ALIMENTACAO, [])

def salvar_alimentacao(dados):
    salvar_json(ARQUIVO_ALIMENTACAO, dados)

def carregar_atividades():
    return carregar_json(ARQS["atividades"], [])

def salvar_atividades(dados):
    salvar_json(ARQS["atividades"], dados)

# ================== FUNÇÕES VISUAIS ==================
def label_central(texto, tamanho=22, cor=(0, 0, 0, 1)):
    lbl = Label(text=texto, font_size=tamanho, color=cor,
                halign="center", valign="middle")
    lbl.bind(size=lambda s, *_: setattr(s, "text_size", s.size))
    return lbl

def titulo(txt):
    return Label(
        text=txt,
        font_size=26,
        font_name=FONTE_BOTAO,
        color=BLACK,
        size_hint_y=None,
        height=50,
        halign="center",
        valign="middle"
    )

def popup_padrao(titulo_txt, mensagem):
    box = BoxLayout(orientation="vertical", padding=12, spacing=12)
    box.add_widget(Label(
        text=mensagem,
        font_name=FONTE_TEXTO,
        color=TEXTO,
        halign="center",
        valign="middle"
    ))
    btn = BotaoBonito("Fechar")
    box.add_widget(btn)

    popup = Popup(
        title=titulo_txt,
        content=box,
        size_hint=(0.7, 0.35),
        auto_dismiss=False
    )
    btn.bind(on_release=popup.dismiss)
    popup.open()

def botao_voltar(manager, tela="principal"):
    return BotaoBonito("⬅ Voltar", on_release=lambda *_: setattr(manager, "current", tela))

# ================== CLASSES BASE ==================
class TelaBase(Screen):
    def __init__(self, fundo=FUNDO, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*fundo)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._atualizar, size=self._atualizar)

    def _atualizar(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size

class BotaoBonito(ButtonBehavior, Widget):
    def __init__(self, texto="", bg_color=LIGHT_PURPLE, on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, None)
        self.height = 45
        self.radius = 22

        with self.canvas.before:
            Color(0, 0, 0, 0.15)
            self.sombra = RoundedRectangle(radius=[self.radius])
            self.bg_color = Color(*bg_color)
            self.bg = RoundedRectangle(radius=[self.radius])

        self.label = Label(
            text=texto,
            font_name=FONTE_BOTAO,
            color=TEXTO,
            halign="center",
            valign="middle"
        )
        self.label.bind(size=lambda s, *_: setattr(s, "text_size", s.size))
        self.add_widget(self.label)

        self.bind(pos=self._update, size=self._update)
        self._callback = on_release or (lambda *_: None)

    def _update(self, *_):
        self.sombra.pos = (self.x + 2, self.y - 2)
        self.sombra.size = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size

    def on_press(self):
        self.bg_color.rgba = LIGHT_PURPLE

    def on_release(self):
        self.bg_color.rgba = PURPLE
        self._callback(self)


# ================== TELAS PLACEHOLDER ==================
class TelaPrincipalAtividades(Screen): pass
class TelaRegistrarAtividade(Screen): pass
class TelaListaAtividades(Screen): pass
class TelaPrincipalAlimentos(Screen): pass
class TelaRegistrarAlimento(Screen): pass
class TelaListaAlimentos(Screen): pass
class TelaAnalise(Screen): pass
class TelaBaseMed(TelaBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# ================== UTILIDADES ==================
from datetime import datetime, timedelta

def calcular_data_termino(data_inicio, duracao_dias):
    data = datetime.strptime(data_inicio, "%d/%m/%Y")
    return (data + timedelta(days=duracao_dias)).strftime("%d/%m/%Y")

PALAVRAS_ALERTA = [
    "suicídio", "suicida", "machucar", "triste",
    "depressão", "ansioso", "desespero", "dor", "sofrimento"
]


class Principal(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        root = BoxLayout(orientation="vertical")

        scroll = ScrollView()
        box = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15,
            size_hint_y=None
        )
        box.bind(minimum_height=box.setter("height"))

        scroll.add_widget(box)
        root.add_widget(scroll)

        box.add_widget(label_central("MENU PRINCIPAL", 28))

        botoes = {
            "Registrar Crises": "registrar_crise",
            "Diário": "principal_diario",
            "Alimentação": "principal_alimentos",
            "Atividades Físicas": "atividades",
            "Consultas": "consultas",
            "Medicamentos": "principal_med",
            "Análise": "analise"
        }

        # Corrige a captura de variável para cada botão
        for txt, tela in botoes.items():
            def criar_callback(t=tela):
                return lambda btn: setattr(self.manager, "current", t)

            b = BotaoBonito(txt, on_release=criar_callback())
            box.add_widget(b)

        self.add_widget(root)


class RegistrarCrise(Screen):
    def on_enter(self):
        self.clear_widgets()

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)
        root.add_widget(titulo("REGISTRAR CRISE"))

        scroll = ScrollView()
        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )
        lista.bind(minimum_height=lista.setter("height"))

        for crise in CRISES.keys():
            b = BotaoBonito(
                crise,
                on_release=lambda btn, c=crise: self.abrir_sub(c)
            )
            lista.add_widget(b)

        scroll.add_widget(lista)
        root.add_widget(scroll)

        ver = BotaoBonito(
            "Crises Registradas",
            on_release=lambda btn: setattr(self.manager, "current", "lista_crises")
        )
        root.add_widget(ver)

        voltar = BotaoBonito(
            "Voltar ao Menu",
            on_release=lambda btn: setattr(self.manager, "current", "principal")
        )
        root.add_widget(voltar)

        self.add_widget(root)

    def abrir_sub(self, crise):
        self.manager.get_screen("sub_crise").crise = crise
        self.manager.current = "sub_crise"



class ListaCrises(Screen):
    def on_enter(self):
        self.clear_widgets()

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)
        root.add_widget(titulo("CRISES REGISTRADAS"))

        scroll = ScrollView()
        lista = BoxLayout(orientation="vertical", size_hint_y=None, spacing=8)
        lista.bind(minimum_height=lista.setter("height"))

        crises = carregar_crises()
        if not crises:
            lista.add_widget(
                Label(
                    text="Nenhuma crise registrada",
                    font_name=FONTE_TEXTO,
                    color=BLACK
                )
            )
        else:
            for c in crises:
                txt = f"{c['data']} {c['hora']}\n{c['crise']} - {c['subtipo']}"
                lista.add_widget(
                    Label(
                        text=txt,
                        font_name=FONTE_TEXTO,
                        color=BLACK,
                        size_hint_y=None,
                        height=60
                    )
                )

        scroll.add_widget(lista)
        root.add_widget(scroll)

        voltar = BotaoBonito(
            "Voltar",
            on_release=lambda *_: setattr(self.manager, "current", "registrar_crise")
        )
        root.add_widget(voltar)

        self.add_widget(root)

# ================= TELA PRINCIPAL DO DIÁRIO =================
# ================= TELA PRINCIPAL DO DIÁRIO =================
class TelaPrincipalDiario(TelaBase):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=12,
            padding=12
        )

        layout.add_widget(Label(
            text="Diário",
            font_name=FONTE_BOTAO,
            font_size=28,
            color=TEXTO,
            size_hint_y=None,
            height=50
        ))

        layout.add_widget(BotaoBonito(
            "Novo Registro",
            on_release=lambda *_: setattr(self.manager, "current", "registro_diario")
        ))

        layout.add_widget(BotaoBonito(
            "Registros Salvos",
            on_release=lambda *_: setattr(self.manager, "current", "lista_diario")
        ))

        layout.add_widget(botao_voltar(self.manager, "principal"))

        self.add_widget(layout)


# ================= REGISTRO DO DIÁRIO =================
class TelaRegistroDiario(TelaBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.humor = None

        self.texto_input = TextInput(
            multiline=True,
            background_color=(1, 1, 1, 1),
            foreground_color=TEXTO,
            font_name=FONTE_TEXTO,
            size_hint_y=1
        )

    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=12
        )

        layout.add_widget(Label(
            text="Novo Registro",
            font_name=FONTE_BOTAO,
            font_size=26,
            color=TEXTO,
            size_hint_y=None,
            height=50
        ))

        layout.add_widget(botao_voltar(self.manager, "principal_diario"))

        humor_box = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )

        for h in ["bom", "neutro", "dificil"]:
            humor_box.add_widget(BotaoBonito(
                h.capitalize(),
                on_release=lambda *_ , val=h: self.definir_humor(val)
            ))

        layout.add_widget(humor_box)
        layout.add_widget(self.texto_input)

        layout.add_widget(BotaoBonito(
            "Não sabe por onde começar?",
            on_release=self.popup_frases
        ))

        layout.add_widget(BotaoBonito(
            "Salvar",
            on_release=self.salvar
        ))

        self.add_widget(layout)

    def definir_humor(self, valor):
        self.humor = valor

    def popup_frases(self, *_):
        if not self.humor:
            popup_padrao("Aviso", "Escolha um humor antes de ver as sugestões.")
            return

        content = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        for frase in FRASES_HUMOR.get(self.humor, []):
            content.add_widget(BotaoBonito(
                frase,
                on_release=lambda *_ , f=frase: self.usar_frase(f)
            ))

        btn_fechar = BotaoBonito("Fechar")
        content.add_widget(btn_fechar)

        popup = Popup(
            title="Sugestões",
            content=content,
            size_hint=(0.85, 0.65),
            auto_dismiss=False,
            separator_color=PURPLE
        )

        btn_fechar.bind(on_release=popup.dismiss)
        popup.open()

    def usar_frase(self, frase):
        self.texto_input.text = frase

    def salvar(self, *_):
        if not self.texto_input.text.strip():
            popup_padrao("Aviso", "Escreva algo antes de salvar.")
            return

        registro = {
            "data": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M"),
            "humor": self.humor or "",
            "texto": self.texto_input.text.strip()
        }

        salvar_registros_diario(registro)

        popup_padrao("Salvo", "Registro salvo com sucesso!")
        self.texto_input.text = ""
        self.humor = None


# ================= LISTA DE REGISTROS DO DIÁRIO =================
class TelaListaDiario(TelaBase):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=12
        )

        layout.add_widget(Label(
            text="Registros Salvos",
            font_name=FONTE_BOTAO,
            font_size=26,
            color=TEXTO,
            size_hint_y=None,
            height=50
        ))

        registros = carregar_registros_diario()

        scroll = ScrollView(size_hint=(1, 1))
        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )
        lista.bind(minimum_height=lista.setter("height"))

        if not registros:
            lista.add_widget(Label(
                text="Nenhum registro salvo.",
                font_name=FONTE_TEXTO,
                color=BLACK,
                size_hint_y=None,
                height=40
            ))
        else:
            for r in registros:
                texto = (
                    f"{r.get('data', '')} {r.get('hora', '')}\n"
                    f"Humor: {r.get('humor', '')}\n"
                    f"{r.get('texto', '')}"
                )

                lista.add_widget(Label(
                    text=texto,
                    font_name=FONTE_TEXTO,
                    color=BLACK,
                    size_hint_y=None,
                    height=90,
                    halign="left",
                    valign="top"
                ))

        scroll.add_widget(lista)
        layout.add_widget(scroll)

        layout.add_widget(botao_voltar(self.manager, "principal_diario"))

        self.add_widget(layout)


# =================== TELAS DE MEDICAMENTOS ===================

class TelaPrincipalMed(TelaBaseMed):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=12, padding=12)
        self.add_widget(layout)

        layout.add_widget(
            Label(
                text="Medicamentos",
                font_name=FONTE_TEXTO,
                font_size=26,
                color=TEXTO,
                size_hint_y=None,
                height=50
            )
        )

        layout.add_widget(
            BotaoBonito(
                "📋 Medicamentos Registrados",
                on_release=lambda *_: setattr(self.manager, "current", "lista_med")
            )
        )

        layout.add_widget(
            BotaoBonito(
                "➕ Registrar Medicamento",
                on_release=lambda *_: setattr(self.manager, "current", "adicionar_med")
            )
        )

        layout.add_widget(
            BotaoBonito(
                "📅 Datas",
                on_release=lambda *_: setattr(self.manager, "current", "datas_med")
            )
        )

        layout.add_widget(botao_voltar(self.manager))


class TelaAdicionarMed(TelaBaseMed):
    editar_modo = False
    med_editando = None

    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=12)
        self.add_widget(layout)

        layout.add_widget(
            Label(
                text="Registrar Medicamento",
                font_name=FONTE_TEXTO,
                font_size=22,
                color=TEXTO,
                size_hint_y=None,
                height=50
            )
        )

        self.nome_input = TextInput(hint_text="Nome", multiline=False)
        self.dose_input = TextInput(hint_text="Dose", multiline=False)
        self.quant_input = TextInput(hint_text="Quantidade", multiline=False)
        self.freq_input = TextInput(hint_text="Vezes ao dia", multiline=False)
        self.compra_input = TextInput(hint_text="Data de compra (dd/mm/yyyy)", multiline=False)

        for w in [
            self.nome_input,
            self.dose_input,
            self.quant_input,
            self.freq_input,
            self.compra_input
        ]:
            layout.add_widget(w)

        layout.add_widget(BotaoBonito("💾 Salvar", on_release=self.salvar_med))
        layout.add_widget(botao_voltar(self.manager))

        if self.editar_modo and self.med_editando:
            self.nome_input.text = self.med_editando.get("nome", "")
            self.dose_input.text = self.med_editando.get("dose", "")
            self.quant_input.text = self.med_editando.get("quantidade", "")
            self.freq_input.text = self.med_editando.get("vezes_ao_dia", "")
            self.compra_input.text = self.med_editando.get("data_compra", "")
        else:
            self.editar_modo = False
            self.med_editando = None

    def salvar_med(self, *_):
        if not self.nome_input.text.strip():
            popup_padrao("Aviso", "Informe o nome do medicamento.")
            return

        meds = carregar_meds()

        med = {
            "nome": self.nome_input.text.strip(),
            "dose": self.dose_input.text.strip(),
            "quantidade": self.quant_input.text.strip(),
            "vezes_ao_dia": self.freq_input.text.strip(),
            "data_compra": self.compra_input.text.strip()
        }

        if self.editar_modo and self.med_editando in meds:
            index = meds.index(self.med_editando)
            meds[index] = med
        else:
            meds.append(med)

        salvar_meds(meds)

        self.editar_modo = False
        self.med_editando = None
        self.manager.current = "principal_med"


class TelaListaMed(TelaBaseMed):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=12)
        self.add_widget(layout)

        layout.add_widget(
            Label(
                text="Medicamentos Registrados",
                font_name=FONTE_TEXTO,
                font_size=24,
                color=TEXTO,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()
        self.meds_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=12,
            padding=5
        )
        self.meds_box.bind(minimum_height=self.meds_box.setter('height'))

        scroll.add_widget(self.meds_box)
        layout.add_widget(scroll)

        layout.add_widget(botao_voltar(self.manager))
        self.carregar_cartoes()

    def carregar_cartoes(self):
        self.meds_box.clear_widgets()

        for med in carregar_meds():
            self.meds_box.add_widget(
                Label(
                    text=f"{med.get('nome','')} - {med.get('dose','')}",
                    color=TEXTO,
                    size_hint_y=None,
                    height=40
                )
            )


class TelaDatas(TelaBaseMed):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=12)
        self.add_widget(layout)

        layout.add_widget(
            Label(
                text="Datas de Medicamentos",
                font_name=FONTE_TEXTO,
                font_size=24,
                color=TEXTO,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()
        self.datas_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=12,
            padding=5
        )
        self.datas_box.bind(minimum_height=self.datas_box.setter('height'))

        scroll.add_widget(self.datas_box)
        layout.add_widget(scroll)

        layout.add_widget(botao_voltar(self.manager))
        self.carregar_datas()

    def carregar_datas(self):
        self.datas_box.clear_widgets()

        for med in carregar_meds():
            termino = calcular_data_termino(med)
            termino_str = termino.strftime("%d/%m/%Y") if termino else "Indefinido"

            self.datas_box.add_widget(
                Label(
                    text=f"{med.get('nome','')} - Termina em: {termino_str}",
                    color=TEXTO,
                    size_hint_y=None,
                    height=40
                )
            )


# =================== CONSULTAS ===================

# =================== CONSULTAS ===================

ARQUIVO_CONSULTAS = "consultas.json"

def carregar_consultas():
    if not os.path.exists(ARQUIVO_CONSULTAS):
        return []
    with open(ARQUIVO_CONSULTAS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_consultas(dados):
    with open(ARQUIVO_CONSULTAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


class Consultas(TelaBase):
    popup_mostrado = False

    def on_enter(self):
        self.clear_widgets()

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)
        root.add_widget(titulo("Consultas"))

        root.add_widget(
            BotaoBonito(
                "Registrar consulta",
                on_release=lambda *_: setattr(self.manager, "current", "registrar_consulta")
            )
        )

        root.add_widget(
            BotaoBonito(
                "Consultas registradas",
                on_release=lambda *_: setattr(self.manager, "current", "consultas_registradas")
            )
        )

        root.add_widget(botao_voltar(self.manager))
        self.add_widget(root)

        if self.popup_mostrado:
            return

        hoje = datetime.now()
        pendentes = []

        for c in carregar_consultas():
            try:
                data = datetime.strptime(c["data"], "%d/%m/%Y")
                if 0 <= (data - hoje).days <= 2:
                    pendentes.append(
                        f"{c['nome']} em {c['data']} às {c['horario']}"
                    )
            except Exception:
                pass

        if pendentes:
            Popup(
                title="Próximas consultas",
                content=Label(text="\n".join(pendentes)),
                size_hint=(0.7, 0.3)
            ).open()
            self.popup_mostrado = True


class RegistrarConsulta(TelaBase):
    def on_enter(self):
        self.clear_widgets()

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        self.nome = TextInput(
            hint_text="Nome do profissional",
            size_hint_y=None,
            height=45
        )
        self.especialidade = TextInput(
            hint_text="Especialidade",
            size_hint_y=None,
            height=45
        )
        self.data = TextInput(
            hint_text="Data (DD/MM/AAAA)",
            size_hint_y=None,
            height=45
        )
        self.horario = TextInput(
            hint_text="Horário (HH:MM)",
            size_hint_y=None,
            height=45
        )
        self.obs = TextInput(
            hint_text="Observações",
            size_hint_y=None,
            height=60
        )

        scroll = ScrollView()
        container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=12,
            padding=12
        )
        container.bind(minimum_height=container.setter("height"))

        for w in [
            self.nome,
            self.especialidade,
            self.data,
            self.horario,
            self.obs
        ]:
            container.add_widget(w)

        container.add_widget(
            BotaoBonito("Salvar", on_release=self.salvar)
        )
        container.add_widget(botao_voltar(self.manager))

        scroll.add_widget(container)
        root.add_widget(scroll)
        self.add_widget(root)

    def salvar(self, *_):
        dados = carregar_consultas()

        dados.append({
            "nome": self.nome.text.strip(),
            "especialidade": self.especialidade.text.strip(),
            "data": self.data.text.strip(),
            "horario": self.horario.text.strip(),
            "obs": self.obs.text.strip()
        })

        salvar_consultas(dados)
        self.manager.current = "consultas"


class ConsultasRegistradas(TelaBase):
    def on_enter(self):
        self.clear_widgets()

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)
        root.add_widget(titulo("Consultas registradas"))

        scroll = ScrollView()
        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )
        lista.bind(minimum_height=lista.setter("height"))

        dados = carregar_consultas()

        if not dados:
            lista.add_widget(
                Label(
                    text="Nenhuma consulta registrada",
                    font_name=FONTE_TEXTO,
                    color=BLACK,
                    size_hint_y=None,
                    height=40
                )
            )
        else:
            for idx, c in enumerate(dados):
                bloco = BoxLayout(
                    orientation="vertical",
                    size_hint_y=None,
                    spacing=8,
                    padding=8
                )
                bloco.bind(minimum_height=bloco.setter("height"))

                bloco.add_widget(Label(
                    text=f"Nome: {c['nome']}",
                    color=BLACK,
                    size_hint_y=None,
                    height=25
                ))
                bloco.add_widget(Label(
                    text=f"Especialidade: {c['especialidade']}",
                    color=BLACK,
                    size_hint_y=None,
                    height=25
                ))
                bloco.add_widget(Label(
                    text=f"Data: {c['data']}",
                    color=BLACK,
                    size_hint_y=None,
                    height=25
                ))
                bloco.add_widget(Label(
                    text=f"Horário: {c['horario']}",
                    color=BLACK,
                    size_hint_y=None,
                    height=25
                ))
                bloco.add_widget(Label(
                    text=f"Observações: {c['obs']}",
                    color=BLACK,
                    size_hint_y=None,
                    height=40
                ))

                excluir = BotaoBonito("Excluir consulta")
                excluir.bind(
                    on_release=lambda _, i=idx: self.excluir(i)
                )
                bloco.add_widget(excluir)

                lista.add_widget(bloco)

        scroll.add_widget(lista)
        root.add_widget(scroll)
        root.add_widget(botao_voltar(self.manager))
        self.add_widget(root)

    def excluir(self, idx):
        dados = carregar_consultas()
        if 0 <= idx < len(dados):
            dados.pop(idx)
            salvar_consultas(dados)
        self.on_enter()

class Atividades(TelaBase):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        root.add_widget(titulo("ATIVIDADES DO DIA"))

        root.add_widget(
            BotaoBonito(
                "Registrar Atividade",
                on_release=lambda *_: setattr(self.manager, "current", "registrar")
            )
        )
        root.add_widget(
            BotaoBonito(
                "Histórico de Atividades",
                on_release=lambda *_: setattr(self.manager, "current", "historico")
            )
        )

        # Mostrar atividades do dia
        hoje = datetime.now().strftime("%d/%m/%Y")
        pendentes = [a for a in carregar_atividades() if a["data"] == hoje]

        if not pendentes:
            root.add_widget(
                Label(
                    text="Nenhuma atividade registrada hoje!",
                    font_name=FONTE_TEXTO,
                    color=BLACK,
                    size_hint_y=None,
                    height=40
                )
            )

        # botão voltar ao menu principal
        root.add_widget(botao_voltar(self.manager))

        self.add_widget(root)



class Registrar(TelaBase):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        self.nome = TextInput(hint_text="Nome da atividade", size_hint_y=None, height=40)
        self.duracao = TextInput(hint_text="Duração (minutos)", size_hint_y=None, height=40)
        self.intensidade = Spinner(
            text="Intensidade",
            values=["Leve", "Moderada", "Intensa"],
            size_hint_y=None,
            height=40
        )
        self.data = TextInput(
            hint_text="Data (DD/MM/AAAA)",
            size_hint_y=None,
            height=40,
            text=datetime.now().strftime("%d/%m/%Y")
        )
        self.obs = TextInput(hint_text="Observações", size_hint_y=None, height=60)

        scroll = ScrollView()
        container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        container.bind(minimum_height=container.setter("height"))

        for w in [self.nome, self.duracao, self.intensidade, self.data, self.obs]:
            container.add_widget(w)

        # Botões dentro do scroll
        container.add_widget(BotaoBonito("Salvar", on_release=self.salvar))
        container.add_widget(botao_voltar(self.manager))  # volta ao menu principal

        scroll.add_widget(container)
        root.add_widget(scroll)
        self.add_widget(root)

    def salvar(self, *_):
        dados = carregar_atividades()
        dados.append({
            "nome": self.nome.text,
            "duracao": self.duracao.text,
            "intensidade": self.intensidade.text,
            "data": self.data.text,
            "obs": self.obs.text
        })
        salvar_atividades(dados)
        self.manager.current = "atividades"

class Historico(TelaBase):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        root.add_widget(titulo("HISTÓRICO DE ATIVIDADES"))

        scroll = ScrollView()
        lista = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        lista.bind(minimum_height=lista.setter("height"))

        dados = carregar_atividades()

        if not dados:
            lista.add_widget(
                Label(
                    text="Nenhuma atividade registrada",
                    font_name=FONTE_TEXTO,
                    color=BLACK,
                    size_hint_y=None,
                    height=40
                )
            )
        else:
            for idx, a in enumerate(dados):
                bloco = BoxLayout(
                    orientation="vertical",
                    size_hint_y=None,
                    spacing=5,
                    padding=5
                )
                bloco.bind(minimum_height=bloco.setter("height"))

                bloco.add_widget(Label(text=f"Atividade: {a['nome']}", height=25, color=BLACK))
                bloco.add_widget(Label(text=f"Duração: {a['duracao']} min", height=25, color=BLACK))
                bloco.add_widget(Label(text=f"Intensidade: {a['intensidade']}", height=25, color=BLACK))
                bloco.add_widget(Label(text=f"Data: {a['data']}", height=25, color=BLACK))
                bloco.add_widget(Label(text=f"Observações: {a['obs']}", height=40, color=BLACK))

                excluir = BotaoBonito(
                    "Excluir atividade",
                    on_release=lambda _, i=idx: self.excluir(i)
                )
                bloco.add_widget(excluir)

                lista.add_widget(bloco)

        scroll.add_widget(lista)
        root.add_widget(scroll)
        root.add_widget(botao_voltar(self.manager))
        self.add_widget(root)

    def excluir(self, idx):
        dados = carregar_atividades()
        dados.pop(idx)
        salvar_atividades(dados)
        self.on_enter()

# ==============================
# Base das telas de alimentação
# ==============================
# ==============================
# BASE
# ==============================

class TelaBaseAlimentacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*FUNDO)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


def botao_voltar_menu_alimentos(manager):
    return BotaoBonito(
        "⬅ Voltar ao Menu",
        on_release=lambda *_: setattr(manager, "current", "principal_alimentos")
    )

# ==============================
# TELA PRINCIPAL
# ==============================

class AlimentacaoPrincipal(TelaBaseAlimentacao):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        layout.add_widget(Label(text="Alimentação", font_size=22))

        layout.add_widget(
            BotaoBonito(
                "Registrar Alimentação",
                on_release=lambda *_: setattr(self.manager, "current", "alimentacao_registro")
            )
        )

        layout.add_widget(
            BotaoBonito(
                "Registros Salvos",
                on_release=lambda *_: setattr(self.manager, "current", "alimentacao_lista")
            )
        )

        layout.add_widget(botao_voltar(self.manager))
        self.add_widget(layout)

# ==============================
# REGISTRO
# ==============================

class AlimentacaoRegistro(TelaBaseAlimentacao):
    def on_enter(self):
        self.clear_widgets()
        self.selecionados = set()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(Label(text="Registrar Alimentação", font_size=20))

        self.area = BoxLayout(
            orientation="vertical",
            spacing=8
        )
        layout.add_widget(self.area)

        self.mostrar_categorias()

        layout.add_widget(
            BotaoBonito("Salvar", on_release=self.salvar)
        )

        layout.add_widget(botao_voltar_menu_alimentos(self.manager))
        self.add_widget(layout)

    def mostrar_categorias(self):
        self.area.clear_widgets()

        for categoria in ALIMENTOS:
            self.area.add_widget(
                BotaoBonito(
                    categoria,
                  on_release=lambda _, c=categoria: self.mostrar_alimentos(c)

                )
            )

    def mostrar_alimentos(self, categoria):
        self.area.clear_widgets()

        for alimento in ALIMENTOS[categoria]:
            btn = ToggleButton(
                text=alimento,
                size_hint_y=None,
                height=40
            )
            btn.bind(on_state=self.marcar)
            self.area.add_widget(btn)

        self.area.add_widget(
            BotaoBonito(
                "⬅ Voltar",
                on_release=lambda *_: self.mostrar_categorias()
            )
        )

    def marcar(self, btn, estado):
        if estado == "down":
            self.selecionados.add(btn.text)
        else:
            self.selecionados.discard(btn.text)

    def salvar(self, *_):
        if not self.selecionados:
            return

        dados = carregar_alimentacao()
        agora = datetime.now()

        dados.append({
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M"),
            "alimentos": list(self.selecionados)
        })

        salvar_alimentacao(dados)
        self.manager.current = "principal_alimentos"

# ==============================
# LISTAGEM
# ==============================

class AlimentacaoLista(TelaBaseAlimentacao):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(Label(text="Registros de Alimentação", font_size=20))

        scroll = ScrollView()
        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=8
        )
        lista.bind(minimum_height=lista.setter("height"))

        dados = carregar_alimentacao()

        if not dados:
            lista.add_widget(
                Label(
                    text="Nenhum registro encontrado",
                    size_hint_y=None,
                    height=40
                )
            )
        else:
            for r in dados:
                texto = (
                    f"{r['data']} {r['hora']}\n"
                    + "\n".join(f"- {a}" for a in r["alimentos"])
                )

                lista.add_widget(
                    Label(
                        text=texto,
                        size_hint_y=None,
                        height=80
                    )
                )

        scroll.add_widget(lista)
        layout.add_widget(scroll)

        layout.add_widget(botao_voltar_menu_alimentos(self.manager))
        self.add_widget(layout)

from datetime import datetime, timedelta
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from datetime import datetime, timedelta
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class TelaAnalise(Screen):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=10, spacing=5)

        root.add_widget(Label(
            text="Análise últimos 7 dias (resumida)",
            font_name=FONTE_TEXTO,
            font_size=22,
            color=TEXTO,
            size_hint_y=None,
            height=40
        ))

        dados = self.coletar_dados_7_dias()
        dias = list(dados.keys())

        cabecalho = BoxLayout(size_hint_y=None, height=25)
        for t in ["Dia","Crises","Humor Neg.","Alimentos","Medicamentos","Atividades","Consultas","Detalhes"]:
            cabecalho.add_widget(Label(text=t, color=TEXTO))
        root.add_widget(cabecalho)

        for dia in dias:
            resumo = dados[dia]
            linha = BoxLayout(size_hint_y=None, height=30, spacing=2)

            linha.add_widget(Label(text=dia, color=TEXTO))
            linha.add_widget(Label(text=str(resumo["crises"]), color=TEXTO))
            linha.add_widget(Label(text=str(resumo["humor_negativo"]), color=TEXTO))
            linha.add_widget(Label(text=str(resumo["alimentos"]), color=TEXTO))
            linha.add_widget(Label(text=str(resumo["medicamentos"]), color=TEXTO))
            linha.add_widget(Label(text=str(resumo["atividades"]), color=TEXTO))
            linha.add_widget(Label(text=str(resumo["consultas"]), color=TEXTO))

            linha.add_widget(
                BotaoBonito(
                    "Ver",
                    on_release=lambda _, d=dia: self.mostrar_detalhes(d)
                )
            )

            root.add_widget(linha)

        root.add_widget(
            BotaoBonito(
                "⬅ Voltar",
                on_release=lambda *_: setattr(self.manager, "current", "principal")
            )
        )

        self.add_widget(root)

def coletar_dados_7_dias(self):
    hoje = datetime.now()
    dados = {}

    dados["diario"] = carregar(ARQS.get("diario", "diario.json"))
    dados["crises"] = carregar(ARQS.get("crises", "crises.json"))
    dados["alimentacao"] = carregar(ARQS.get("alimentacao", "alimentacao.json"))
    dados["medicamentos"] = carregar(ARQS.get("medicamentos", "medicamentos.json"))
    dados["atividades"] = carregar(ARQS.get("atividades", "atividades.json"))
    dados["consultas"] = carregar(ARQS.get("consultas", "consultas.json"))

    return dados



    def mostrar_detalhes(self, dia):
        diario = [d for d in carregar(ARQS["diario"]) if d.get("data") == dia]
        crises = [c for c in carregar(ARQS["crises"]) if c.get("data") == dia]
        alimentacao = [a for a in carregar(ARQS["alimentacao"]) if a.get("data") == dia]
        atividades = [a for a in carregar(ARQS["atividades"]) if a.get("data") == dia]
        consultas = [c for c in carregar(ARQS["consultas"]) if c.get("data") == dia]
        medicamentos = [m for m in carregar(ARQS["medicamentos"]) if dia in m.get("tomado", {})]

        texto = f"Dia: {dia}\n\n"
        texto += f"Crises: {len(crises)}\n"
        texto += f"Humor negativo: {len([d for d in diario if d.get('humor')=='Difícil'])}\n"
        texto += f"Alimentos ingeridos: {len(alimentacao)}\n"
        texto += f"Medicamentos tomados: {len(medicamentos)}\n"
        texto += f"Atividades: {len(atividades)}\n"
        texto += f"Consultas: {len(consultas)}\n\n"

        if alimentacao:
            texto += "Alimentos:\n"
            for a in alimentacao:
                for item in a.get("alimentos", []):
                    texto += f"- {item}\n"

        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=texto, halign="left", valign="top"))
        btn = BotaoBonito("Fechar")

        popup = Popup(
            title="Detalhes do dia",
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )

        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

# =================== MEU APP ===================
class MeuApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        # =====================
        # Login / Cadastro / Principal
        # =====================
        sm.add_widget(Login(name="login"))
        sm.add_widget(Cadastro(name="cadastro"))
        sm.add_widget(Principal(name="principal"))

        # =====================
        # Crises
        # =====================
        sm.add_widget(RegistrarCrise(name="registrar_crise"))
        sm.add_widget(SubCrise(name="sub_crise"))
        sm.add_widget(ListaCrises(name="lista_crises"))

        # =====================
        # Diário
        # =====================
        sm.add_widget(TelaPrincipalDiario(name="principal_diario"))
        sm.add_widget(TelaRegistroDiario(name="registro_diario"))
        sm.add_widget(TelaListaDiario(name="lista_diario"))

        # =====================
        # Medicamentos
        # =====================
        sm.add_widget(TelaPrincipalMed(name="principal_med"))
        sm.add_widget(TelaAdicionarMed(name="adicionar_med"))
        sm.add_widget(TelaListaMed(name="lista_med"))
        sm.add_widget(TelaDatas(name="datas_med"))

        # =====================
        # Consultas
        # =====================
        sm.add_widget(Consultas(name="consultas"))
        sm.add_widget(RegistrarConsulta(name="registrar_consulta"))
        sm.add_widget(ConsultasRegistradas(name="consultas_registradas"))

        # =====================
        # Atividades
        # =====================
        sm.add_widget(Atividades(name="atividades"))
        sm.add_widget(Registrar(name="registrar_atividade"))
        sm.add_widget(Historico(name="historico"))

        # =====================
        # Alimentação
        # =====================
        sm.add_widget(AlimentacaoPrincipal(name="principal_alimentos"))
        sm.add_widget(AlimentacaoRegistro(name="alimentacao_registro"))
        sm.add_widget(AlimentacaoLista(name="alimentacao_lista"))

        # =====================
        # Análise
        # =====================
        sm.add_widget(TelaAnalise(name="analise"))

        sm.current = "login"
        return sm


if __name__ == "__main__":
    MeuApp().run()

