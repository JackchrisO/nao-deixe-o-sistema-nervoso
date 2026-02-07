[app]
title = Synapse
package.name = synapse
package.domain = org.synapse
source.dir = .
source.include_exts = py,kv,json

version = 0.1

requirements = python3,kivy==2.1.0,kivymd==1.1.1

orientation = portrait

fullscreen = 0

# ---------- ANDROID ----------
android.api = 29
android.minapi = 21

# NDK estável e compatível
android.ndk = 23b

# Permissões básicas
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Arquiteturas
android.archs = arm64-v8a, armeabi-v7a

# Otimizações
android.enable_androidx = True
android.allow_backup = True

# Log (ajuda MUITO a debugar)
log_level = 2
