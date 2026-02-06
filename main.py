# main.py
import json, os, uuid, hashlib, datetime, re
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem

# =========================
# ARQUIVOS
# =========================
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

def alerta_palavras(texto):
    palavras = [
        "suicidio","morte","morrer","matar","tirar a vida","acabar com tudo",
        "desistir","sem sentido","inutil","foda-se","não aguento","cortar",
        "ferir","machucar","ódio","raiva","desespero","sofrimento","fim",
        "vontade de morrer","não quero viver","acabou","nada importa",
        "perder a vida","sofrer","desamparo","sem saída","angustia","desolado",
        "desesperado","sem esperança"
    ]
    texto = texto.lower()
    return any(p in texto for p in palavras)

def dias_ate(data_str):
    try:
        data = datetime.date.fromisoformat(data_str)
        return (data - datetime.date.today()).days
    except:
        return None

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

    # -------------------
    # LOGIN
    # -------------------
    def login(self):
        u = self.root.ids.login_user.text.strip()
        p = self.root.ids.login_pwd.text.strip()

        if u == "adm" and p == "adm":
            self.root.ids.screen_manager.current = "admin"
            return

        if u not in self.usuarios:
            self.root.ids.login_msg.text = "Usuário não encontrado"
            return

        h, salt = self.usuarios[u]["senha"], self.usuarios[u]["salt"]
        if hash_senha(p, salt)[0] != h:
            self.root.ids.login_msg.text = "Senha incorreta"
            return

        self.user = u
        self.root.ids.login_msg.text = ""
        self.root.ids.screen_manager.current = "principal"
        self.atualizar_menu()
        self.check_alertas()

    # -------------------
    # CADASTRO
    # -------------------
    def cadastrar(self):
        nome = self.root.ids.cad_nome.text.strip()
        idade = self.root.ids.cad_idade.text.strip()
        sexo = self.root.ids.cad_sexo.text.strip()
        motivo = self.root.ids.cad_motivo.text.strip()

        if not nome or not idade or not motivo:
            self.root.ids.cad_msg.text = "Preencha todos os campos obrigatórios"
            return

        if nome in self.usuarios:
            self.root.ids.cad_msg.text = "Usuário já existe"
            return

        h, salt = hash_senha(self.root.ids.cad_pwd.text)
        self.usuarios[nome] = {
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "senha": h,
            "salt": salt,
            "motivo": motivo
        }
        save_json(USERS_FILE, self.usuarios)
        self.root.ids.screen_manager.current = "login"
        self.root.ids.cad_msg.text = ""

    # -------------------
    # MENU PRINCIPAL
    # -------------------
    def atualizar_menu(self):
        motivo = self.usuarios[self.user]["motivo"]
        if motivo in ["Epilepsia", "Ambos"]:
            self.root.ids.btn_crises.opacity = 1
            self.root.ids.btn_crises.disabled = False
        else:
            self.root.ids.btn_crises.opacity = 0
            self.root.ids.btn_crises.disabled = True

    # -------------------
    # ALERTAS
    # -------------------
    def check_alertas(self):
        # medicamentos
        meds = self.registros.get(self.user, {}).get("medicamentos", [])
        avisos = []
        for m in meds:
            dias = dias_ate(m.get("prox_compra", m.get("compra", "")))
            if dias is not None and dias <= 5:
                avisos.append(f"{m['nome']} acaba em {dias} dias")

        # consultas (1 dia antes)
        cons = self.registros.get(self.user, {}).get("consultas", [])
        for c in cons:
            dias = dias_ate(c.get("data", ""))
            if dias is not None and dias == 1:
                avisos.append(f"Consulta amanhã: {c['nome']}")

        if avisos:
            MDDialog(
                title="Alertas",
                text="\n".join(avisos),
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            ).open()

    # -------------------
    # CRISES
    # -------------------
    def abrir_crises(self):
        self.root.ids.screen_manager.current = "crises"
        self.root.ids.crises_box.clear_widgets()

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

        for crise, subs in CRISES.items():
            self.root.ids.crises_box.add_widget(
                MDRaisedButton(
                    text=crise,
                    md_bg_color=(0.72,0.65,1,1),
                    on_release=lambda inst, c=crise, s=subs: self.abrir_subcrises(c, s)
                )
            )

    def abrir_subcrises(self, crise, subs):
        self.root.ids.screen_manager.current = "subcrises"
        self.root.ids.subcrises_title.text = crise
        self.root.ids.subcrises_box.clear_widgets()

        for nome, desc in subs:
            self.root.ids.subcrises_box.add_widget(
                MDRaisedButton(
                    text=nome,
                    md_bg_color=(0.81,0.88,1,1),
                    on_release=lambda inst, n=nome: self.registrar_crise(crise, n)
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
        Snackbar(text="Crise registrada!").open()

    def ver_crises_registradas(self):
        self.root.ids.screen_manager.current = "crises_reg"
        self.root.ids.crises_reg_box.clear_widgets()
        registros = self.registros.get(self.user, {}).get("crises", [])
        for r in registros:
            self.root.ids.crises_reg_box.add_widget(
                OneLineListItem(text=f"{r['data']} {r['hora']} - {r['crise']} ({r['subcrise']})")
            )

    # -------------------
    # DIÁRIO
    # -------------------
    def gerar_frases(self):
        frases = {
            "Bom": [
                "Hoje foi um dia leve e tranquilo.",
                "Me senti bem e com energia.",
                "Consegui fazer coisas que gosto.",
                "Tive momentos de alegria hoje.",
                "Me senti em paz comigo mesmo.",
                "Aproveitei bem o dia.",
                "Me senti orgulhoso de mim.",
                "Foi um dia produtivo e positivo.",
                "Senti conexão com pessoas queridas.",
                "Hoje eu me senti confortável em ser eu."
            ],
            "Neutro": [
                "Hoje foi um dia normal, sem grandes emoções.",
                "Não foi ruim, mas também não foi ótimo.",
                "Me senti no automático hoje.",
                "Tive momentos bons e outros não tão bons.",
                "Meu humor ficou estável.",
                "Senti que o dia passou devagar.",
                "Fiquei mais observando do que sentindo.",
                "Foi um dia comum, sem surpresas.",
                "Me senti meio indiferente hoje.",
                "Hoje foi um dia de rotina."
            ],
            "Ruim": [
                "Hoje eu me senti cansado e sem forças.",
                "Tive dificuldade para fazer coisas simples.",
                "Me senti sobrecarregado com tudo.",
                "Tive medo de não dar conta.",
                "Senti que nada fazia sentido.",
                "Me senti sozinho mesmo estando com gente.",
                "Meu corpo parecia pesado hoje.",
                "Senti tristeza sem motivo aparente.",
                "Tive vontade de desaparecer.",
                "Meu coração parecia apertado o dia todo.",
                "Senti raiva de mim mesmo.",
                "Tive dificuldade para respirar e me acalmar.",
                "Me senti inútil hoje.",
                "Senti que ninguém me entende.",
                "Tive pensamentos negativos repetidos.",
                "Senti que não tenho saída.",
                "Me senti muito ansioso o dia todo.",
                "Tive dificuldade para dormir por causa da mente.",
                "Senti que o mundo estava pesado demais."
            ]
        }

        humor = self.root.ids.diario_humor.text.strip().title()
        if humor not in ["Bom", "Neutro", "Ruim"]:
            Snackbar(text="Marque o humor primeiro: Bom / Neutro / Ruim").open()
            return

        frases_list = frases[humor]
        texto = "\n".join([f"{i+1}. {f}" for i, f in enumerate(frases_list)])

        self.dialog = MDDialog(
            title="Frases para te ajudar",
            text=texto,
            size_hint=(0.9, 0.8),
            buttons=[
                MDFlatButton(text="Fechar", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def salvar_diario(self):
        humor = self.root.ids.diario_humor.text.strip().title()
        texto = self.root.ids.diario_text.text.strip()

        if humor not in ["Bom", "Neutro", "Ruim"]:
            Snackbar(text="Marque o humor: Bom / Neutro / Ruim").open()
            return

        if alerta_palavras(texto):
            self.dialog_alerta()

        registro = {
            "data": str(datetime.date.today()),
            "humor": humor,
            "texto": texto
        }
        self.registros.setdefault(self.user, {}).setdefault("diario", []).append(registro)
        save_json(REG_FILE, self.registros)
        Snackbar(text="Diário salvo!").open()

    def dialog_alerta(self):
        self.dialog = MDDialog(
            title="Olá, você não parece tão bem hoje...",
            text="Você merece cuidado. Se estiver em risco, ligue para:\n\n📞 188 (CVV Brasil)\n📞 192 / 193",
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    # -------------------
    # MEDICAMENTOS
    # -------------------
    def abrir_meds(self):
        self.root.ids.screen_manager.current = "meds"
        self.atualiza_lista_meds()

    def atualiza_lista_meds(self):
        self.root.ids.meds_box.clear_widgets()
        meds = self.registros.get(self.user, {}).get("medicamentos", [])
        for i, m in enumerate(meds):
            item = OneLineListItem(text=f"{m['nome']} - {m['mg']}mg - {m['freq']}x/dia - compra: {m['compra']}")
            item.bind(on_release=lambda inst, idx=i: self.dialog_edita_med(idx))
            self.root.ids.meds_box.add_widget(item)

    def registrar_med(self):
        nome = self.root.ids.med_nome.text.strip()
        mg = self.root.ids.med_mg.text.strip()
        freq = self.root.ids.med_freq.text.strip()
        compra = self.root.ids.med_compra.text.strip()

        if not nome or not mg or not freq or not compra:
            Snackbar(text="Preencha todos os campos").open()
            return

        try:
            datetime.date.fromisoformat(compra)
        except:
            Snackbar(text="Data inválida (AAAA-MM-DD)").open()
            return

        prox = datetime.date.fromisoformat(compra) + datetime.timedelta(days=30)
        registro = {"nome": nome, "mg": mg, "freq": freq, "compra": compra, "prox_compra": str(prox)}

        self.registros.setdefault(self.user, {}).setdefault("medicamentos", []).append(registro)
        save_json(REG_FILE, self.registros)
        self.atualiza_lista_meds()
        Snackbar(text="Medicamento registrado!").open()

    def dialog_edita_med(self, idx):
        med = self.registros[self.user]["medicamentos"][idx]

        self.dialog = MDDialog(
            title="Editar / Excluir",
            text=f"{med['nome']} - {med['mg']}mg",
            buttons=[
                MDFlatButton(text="Excluir", on_release=lambda x: self.excluir_med(idx)),
                MDFlatButton(text="Fechar", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def excluir_med(self, idx):
        self.registros[self.user]["medicamentos"].pop(idx)
        save_json(REG_FILE, self.registros)
        self.dialog.dismiss()
        self.atualiza_lista_meds()
        Snackbar(text="Medicamento excluído").open()

    # -------------------
    # CONSULTAS
    # -------------------
    def registrar_consulta(self):
        nome = self.root.ids.cons_nome.text.strip()
        esp = self.root.ids.cons_esp.text.strip()
        data = self.root.ids.cons_data.text.strip()
        hora = self.root.ids.cons_hora.text.strip()

        if not nome or not esp or not data or not hora:
            Snackbar(text="Preencha todos os campos").open()
            return

        try:
            datetime.date.fromisoformat(data)
        except:
            Snackbar(text="Data inválida (AAAA-MM-DD)").open()
            return

        registro = {"nome": nome, "esp": esp, "data": data, "hora": hora}
        self.registros.setdefault(self.user, {}).setdefault("consultas", []).append(registro)
        save_json(REG_FILE, self.registros)
        Snackbar(text="Consulta registrada!").open()

    # -------------------
    # ATIVIDADES
    # -------------------
    def registrar_atividade(self):
        nome = self.root.ids.ativ_nome.text.strip()
        tempo = self.root.ids.ativ_tempo.text.strip()
        intensidade = self.root.ids.ativ_int.text.strip()

        if not nome or not tempo or not intensidade:
            Snackbar(text="Preencha todos os campos").open()
            return

        registro = {"nome": nome, "tempo": tempo, "intensidade": intensidade}
        self.registros.setdefault(self.user, {}).setdefault("atividades", []).append(registro)
        save_json(REG_FILE, self.registros)
        Snackbar(text="Atividade registrada!").open()

    # -------------------
    # ALIMENTAÇÃO
    # -------------------
    def abrir_alimentacao(self):
        self.root.ids.screen_manager.current = "alimentacao"
        self.root.ids.alim_box.clear_widgets()

        TIPOS = {
            "Frutas": ["Maçã", "Banana", "Laranja", "Abacate", "Uva", "Melancia", "Pera", "Manga", "Kiwi", "Morango"],
            "Legumes": ["Cenoura", "Batata", "Abóbora", "Brócolis", "Couve", "Espinafre", "Pepino", "Tomate", "Beterraba", "Rabanete"],
            "Proteínas": ["Frango", "Carne", "Peixe", "Ovo", "Tofu", "Feijão", "Grão-de-bico", "Lentilha", "Queijo", "Iogurte"],
            "Carboidratos": ["Arroz", "Macarrão", "Pão", "Batata", "Aveia", "Quinoa", "Milho", "Cuscuz", "Mandioca", "Pão integral"],
            "Laticínios": ["Leite", "Queijo", "Iogurte", "Manteiga", "Requeijão", "Creme de leite", "Kefir", "Ricota", "Coalhada", "Sorvete"],
            "Gorduras": ["Azeite", "Abacate", "Castanhas", "Manteiga", "Óleo de coco", "Margarina", "Sementes", "Nozes", "Amendoim", "Avelã"],
            "Doces": ["Chocolate", "Bolo", "Sorvete", "Balas", "Pudim", "Cookie", "Doce de leite", "Brigadeiro", "Guloseimas", "Churros"],
            "Bebidas": ["Água", "Suco", "Refrigerante", "Café", "Chá", "Leite", "Smoothie", "Vitamina", "Energético", "Água de coco"],
            "Lanches": ["Sanduíche", "Pizza", "Salgadinho", "Pipoca", "Torrada", "Wrap", "Hambúrguer", "Hot dog", "Sushi", "Tapioca"],
            "Sopas": ["Sopa de legumes", "Caldo verde", "Sopa de frango", "Sopa de carne", "Canja", "Creme de milho", "Sopa de abóbora", "Sopa de lentilha", "Sopa de feijão", "Sopa de batata"]
        }

        for tipo, subs in TIPOS.items():
            self.root.ids.alim_box.add_widget(
                MDRaisedButton(
                    text=tipo,
                    md_bg_color=(0.72,0.65,1,1),
                    on_release=lambda inst, t=tipo, s=subs: self.abrir_sub_alim(t, s)
                )
            )

    def abrir_sub_alim(self, tipo, subs):
        self.root.ids.screen_manager.current = "sub_alim"
        self.root.ids.sub_alim_title.text = tipo
        self.root.ids.sub_alim_box.clear_widgets()

        for s in subs:
            self.root.ids.sub_alim_box.add_widget(
                MDRaisedButton(
                    text=s,
                    md_bg_color=(0.81,0.88,1,1),
                    on_release=lambda inst, sub=s: self.registrar_alim(tipo, sub)
                )
            )

    def registrar_alim(self, tipo, sub):
        registro = {"data": str(datetime.date.today()), "tipo": tipo, "sub": sub}
        self.registros.setdefault(self.user, {}).setdefault("alimentacao", []).append(registro)
        save_json(REG_FILE, self.registros)
        Snackbar(text="Alimentação registrada!").open()

    # -------------------
    # ANALISE
    # -------------------
    def abrir_analise(self, dias=7):
        self.root.ids.screen_manager.current = "analise"
        self.root.ids.analise_box.clear_widgets()

        data_fim = datetime.date.today()
        data_ini = data_fim - datetime.timedelta(days=dias)

        registros = self.registros.get(self.user, {})
        diario = registros.get("diario", [])
        crises = registros.get("crises", [])

        resumo = f"Resumo últimos {dias} dias:\n"
        resumo += f"Diário: {len([d for d in diario if data_ini <= datetime.date.fromisoformat(d['data']) <= data_fim])}\n"
        resumo += f"Crises: {len([c for c in crises if data_ini <= datetime.date.fromisoformat(c['data']) <= data_fim])}\n"

        self.root.ids.analise_box.add_widget(
            MDLabel(text=resumo, theme_text_color="Primary")
        )

        self.root.ids.analise_box.add_widget(
            MDRaisedButton(
                text="Ver últimos 30 dias",
                md_bg_color=(0.72,0.65,1,1),
                on_release=lambda x: self.abrir_analise(30)
            )
        )

    # -------------------
    # ADMIN
    # -------------------
    def abrir_admin(self):
        self.root.ids.screen_manager.current = "admin"

    def ver_dados(self):
        self.root.ids.admin_box.clear_widgets()
        for u, info in self.usuarios.items():
            if u == "adm": continue
            self.root.ids.admin_box.add_widget(
                OneLineListItem(text=f"{u} | idade: {info['idade']} | motivo: {info['motivo']}")
            )

    def sair(self):
        self.root.ids.screen_manager.current = "login"
        self.user = None

if __name__ == "__main__":
    SynapseApp().run()
