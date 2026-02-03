[app]
title = Não deixe o sistema nervoso
package.name = naodeixeosistemanervoso
package.domain = com.jack.neuroapp
source.dir = .
version = 0.1
source.include_exts = py,png,jpg,kv,atlas

# Recomendo testar primeiro apenas com arm64-v8a para ser mais rápido
android.archs = arm64-v8a

# Configurações de API atualizadas para 2024/2025
android.minapi = 21
android.api = 34
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET

requirements = python3,kivy,cython

[presplash]
presplash.color = 000000

[buildozer]
log_level = 2
warn_on_root = 1
