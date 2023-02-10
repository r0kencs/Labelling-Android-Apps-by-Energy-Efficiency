from Decompiler import Decompiler

from Earmo import Earmo

decompiler = Decompiler('apks/stopthefire.apk')
decompiler.decompile()

earmo = Earmo('apks/stopthefire.apk')
earmo.analyze()
