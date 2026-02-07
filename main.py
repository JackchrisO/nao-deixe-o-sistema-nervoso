# main.py
import json, os, uuid, hashlib, datetime
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder

USERS_FILE = "data/usuarios.json"
REG_FILE = "data/registros.json"


# =========================
# UTILS
# =========================
def ensure_data_dir():
    os.makedirs("data", exist_ok=True)

def load_json(path):
    ensure_data_dir()
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_senha(senha, salt=None):
    if not salt:
        salt = uuid.uuid4().hex
    return hashlib.sha256((senha + salt).encode()).hexdigest(), salt


# =========================
# APP
# =========================
class SynapseApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Light"

        self.usuarios = load_json(USERS_FILE)
        self.registros = load_json(REG_FILE)

        return Builder.load_file("synapse.kv")

    # =====================
    # HELPERS
    # =====================
    def sm(self):
        return self.root.ids.screen_manager

    def tela(self, nome):
        return self.sm().get_screen(nome)

    # =====================
    # LOGIN
    # =====================
    def login(self):
        tela = self.tela("login")
        u = tela.ids.login_user.text.strip()
        p = tela.ids.login_pwd.text.strip()

        if u == "adm" and p == "adm":
            self.sm().current = "admin"
            return

        if u not in self.usuarios:
            tela.ids.login_msg.text = "Usuário não encontrado"
            return

        h = self.usuarios[u]["senha"]
        salt = self.usuarios[u]["salt"]

        if hash_senha(p, salt)[0] != h:
            tela.ids.login_msg.text = "Senha incorreta"
            return

        self.user = u
        tela.ids.login_msg.text = ""
        self.sm().current = "principal"
        self.atualizar_menu()

    # =====================
    # CADASTRO
    # =====================
    def cadastrar(self):
        tela = self.tela("cadastro")

        nome = tela.ids.cad_nome.text.strip()
        idade = tela.ids.cad_idade.text.strip()
        sexo = tela.ids.cad_sexo.text.strip()
        motivo = tela.ids.cad_motivo.text.strip()
        senha = tela.ids.cad_pwd.text.strip()

        if not nome or not idade or not motivo or not senha:
            tela.ids.cad_msg.text = "Preencha os campos obrigatórios"
            return

        if nome in self.usuarios:
            tela.ids.cad_msg.text = "Usuário já existe"
            return

        h, salt = hash_senha(senha)
        self.usuarios[nome] = {
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "motivo": motivo,
            "senha": h,
            "salt": salt
        }
        save_json(USERS_FILE, self.usuarios)

        tela.ids.cad_msg.text = ""
        self.sm().current = "login"

    # =====================
    # MENU PRINCIPAL
    # =====================
    def atualizar_menu(self):
        tela = self.tela("principal")
        motivo = self.usuarios[self.user]["motivo"]

        if motivo in ["Epilepsia", "Ambos"]:
            tela.ids.btn_crises.opacity = 1
            tela.ids.btn_crises.disabled = False
        else:
            tela.ids.btn_crises.opacity = 0
            tela.ids.btn_crises.disabled = True

    # =====================
    # CRISES
    # =====================
    def abrir_crises(self):
        tela = self.tela("crises")
        self.sm().current = "crises"
        tela.ids.crises_box.clear_widgets()

        CRISES = {
            "Crise Focal": ["Sensorial", "Motora", "Autonômica", "Psíquica"],
            "Crise Generalizada": ["Tônico-clônica", "Ausência", "Mioclônica"]
        }

        for crise, subs in CRISES.items():
            tela.ids.crises_box.add_widget(
                MDRaisedButton(
                    text=crise,
                    on_release=lambda x, c=crise, s=subs: self.abrir_subcrises(c, s)
                )
            )

    def abrir_subcrises(self, crise, subs):
        tela = self.tela("subcrises")
        self.sm().current = "subcrises"
        tela.ids.subcrises_title.text = crise
        tela.ids.subcrises_box.clear_widgets()

        for s in subs:
            tela.ids.subcrises_box.add_widget(
                MDRaisedButton(
                    text=s,
                    on_release=lambda x, sub=s: self.registrar_crise(crise, sub)
                )
            )

    def registrar_crise(self, crise, sub):
        registro = {
            "data": str(datetime.date.today()),
            "hora": str(datetime.datetime.now().time())[:8],
            "crise": crise,
            "subcrise": sub
        }
        self.registros.setdefault(self.user, {}).setdefault("crises", []).append(registro)
        save_json(REG_FILE, self.registros)
        Snackbar(text="Crise registrada").open()

    # =====================
    # SAIR
    # =====================
    def sair(self):
        self.user = None
        self.sm().current = "login"


if __name__ == "__main__":
    SynapseApp().run()
