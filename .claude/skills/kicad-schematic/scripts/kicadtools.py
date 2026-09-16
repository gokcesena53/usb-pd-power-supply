"""Harici arac bulma ve dosya G/C yardimcilari (render.py, verify.py, kisch_edit.py ortak).

Windows'ta kicad-cli PATH'te olmayabilir ve poppler (pdftoppm) kurulu olmayabilir.
Bu modul araclari bulur; bulamazsa acik hata verir.

DIKKAT: KiCad'in bin dizinini PATH'in ONUNE eklemek KiCad'le gelen python'u
one cikarir (PyMuPDF yok) - araclari PATH'i degistirmeden, tam yoluyla cagir.
"""
import glob
import os
import shutil


def kicad_cli():
    """kicad-cli'nin tam yolu. KICAD_CLI ortam degiskeni oncelikli."""
    env = os.environ.get('KICAD_CLI')
    if env and os.path.exists(env):
        return env
    p = shutil.which('kicad-cli')
    if p:
        return p
    pats = [
        os.path.expandvars(r'%LOCALAPPDATA%\Programs\KiCad\*\bin\kicad-cli.exe'),
        r'C:\Program Files\KiCad\*\bin\kicad-cli.exe',
        '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli',
        '/usr/bin/kicad-cli', '/usr/local/bin/kicad-cli',
    ]
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]          # en yeni surum
    raise FileNotFoundError('kicad-cli bulunamadi; KICAD_CLI ortam degiskenini ayarla')


def read_sheet(path):
    """Metni LF olarak okur; (metin, crlf_mi) dondurur."""
    raw = open(path, 'rb').read()
    return raw.decode('utf-8').replace('\r\n', '\n'), b'\r\n' in raw


def write_sheet(path, text, crlf):
    """Dosyayi okundugu satir sonuyla geri yazar. Bu depodaki dosyalar CRLF;
    LF yazarsan git her satiri degismis gosterir."""
    data = text.replace('\r\n', '\n')
    if crlf:
        data = data.replace('\n', '\r\n')
    open(path, 'wb').write(data.encode('utf-8'))


class keep_file:
    """kicad-cli ERC/export .kicad_pro'yu (yalniz satir sonlarini) yeniden yazar.
    Bu baglam yoneticisi dosyayi cagri sonrasi bayt bayt geri koyar."""

    def __init__(self, path):
        self.path = path
        self.data = None

    def __enter__(self):
        if self.path and os.path.exists(self.path):
            self.data = open(self.path, 'rb').read()
        return self

    def __exit__(self, *exc):
        if self.data is not None and open(self.path, 'rb').read() != self.data:
            open(self.path, 'wb').write(self.data)
        return False


def project_file(sch):
    pro = os.path.splitext(sch)[0] + '.kicad_pro'
    return pro if os.path.exists(pro) else None
