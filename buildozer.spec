[app]
# (str) Title of your app
title = Não deixe o sistema nervoso

# (str) Package name
package.name = naodeixeosistemanervoso

# (str) Package domain (needed for android/ios packaging)
package.domain = com.jack.neuroapp

# (str) Source directory
source.dir = .

# (str) Version
version = 0.1

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Supported android architectures
android.archs = armeabi-v7a

# (int) Android min API to use
android.minapi = 21

# (int) Android target API
android.api = 30

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use (>= 25)
android.ndk = 25b

# (str) Path to the Android SDK
android.sdk_path = /home/runner/android-sdk

# (str) Path to the Android NDK
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653

# (str) Release type (debug or release)
android.release = debug

# (str) Permissions
android.permissions = INTERNET

[requirements]
# (list) Application requirements
requirements = python3,kivy,cython

[presplash]
# (file) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png
# (RGBA) Presplash color
presplash.color = 0x000000

[icon]
# (file) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

[buildozer]
# (int) Log level (0 = error only, 1 = warning, 2 = info, 3 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
