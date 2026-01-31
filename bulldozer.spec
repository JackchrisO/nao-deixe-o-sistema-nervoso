[app]
title = Não Deixe o Sistema Nervoso
package.name = ndsn
package.domain = com.ndsn
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec

[requirements]
python3,kivy

[android]
presplash.filename = %(source.dir)s/icon.png
icon.filename = %(source.dir)s/icon.png
android.arch = armeabi-v7a
android.permissions = INTERNET
