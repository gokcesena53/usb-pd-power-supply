"""Harici arac bulma ve dosya G/C yardimcilari (render.py, verify.py, kisch_edit.py ortak).

Windows'ta kicad-cli PATH'te olmayabilir ve poppler (pdftoppm) kurulu olmayabilir.
Bu modul araclari bulur; bulamazsa acik hata verir.

DIKKAT: KiCad'in bin dizinini PATH'in ONUNE eklemek KiCad'le gelen python'u
one cikarir (PyMuPDF yok) - araclari PATH'i degistirmeden, tam yoluyla cagir.
"""
import glob
import os
import re
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


def kicad_symbol_lib(nick):
    """KiCad'in kendi sembol kutuphanesinin (.kicad_sym) tam yolu.

    Yeni sembol (Timer_RTC:BQ32000, Device:Crystal_GND23, Transistor_FET:
    Q_NMOS_GSD...) eklerken ensure_lib_symbol/swap_lib bu dosyadan kopyalar.
    KICAD*_SYMBOL_DIR ortam degiskeni oncelikli; sonra Linux/Windows/macOS
    varsayilan kurulum dizinleri. Bulamazsa acik hata verir.
    """
    dirs = [v for k, v in sorted(os.environ.items(), reverse=True)
            if re.fullmatch(r'KICAD\d*_SYMBOL_DIR', k)]
    dirs += ['/usr/share/kicad/symbols', '/usr/local/share/kicad/symbols',
             '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols']
    dirs += sorted(glob.glob(os.path.expandvars(
        r'%LOCALAPPDATA%\Programs\KiCad\*\share\kicad\symbols')), reverse=True)
    dirs += sorted(glob.glob(r'C:\Program Files\KiCad\*\share\kicad\symbols'), reverse=True)
    for d in dirs:
        p = os.path.join(d, nick + '.kicad_sym')
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f'{nick}.kicad_sym bulunamadi; KICAD10_SYMBOL_DIR ayarla')


def project_symbol_lib(nick, table='sym-lib-table'):
    """Projenin sym-lib-table'indaki kutuphanenin yolu (${KIPRJMOD} cozulur),
    yoksa KiCad'in sistem kutuphanesi. Power_Path_Custom gibi proje kutuphaneleri
    ile Device/power gibi sistem kutuphanelerini tek yerden bulmak icin."""
    if os.path.exists(table):
        m = re.search(r'\(name "%s"\)[^\n]*?\(uri "([^"]+)"\)' % re.escape(nick),
                      open(table, encoding='utf-8').read())
        if m:
            p = m.group(1).replace('${KIPRJMOD}', os.path.dirname(os.path.abspath(table)))
            if os.path.exists(p):
                return p
    return kicad_symbol_lib(nick)


def kicad_open(project_dir='.'):
    """Proje KiCad'de acik mi: kilit dosyalari (~*.lck) + calisan kicad surecleri.

    Acikken dosyaya yazilan degisiklik KiCad kaydedince EZILIR. Bu oturumda
    kullanici KiCad'i uc kez kapatip yeniden acti; her yazmadan once kontrol et:
        assert not kicad_open(), 'KiCad acik'
    Acikken calismaya devam etmek icin projeyi scratchpad'e kopyalayip betigi
    orada dogrula (SKILL.md "KiCad acikken kuru calistirma").
    Donus: kilit dosyasi / surec satirlari listesi (bos = kapali)."""
    hits = sorted(glob.glob(os.path.join(project_dir, '~*.lck')))
    if shutil.which('pgrep'):
        import subprocess
        here = os.path.abspath(project_dir)
        r = subprocess.run(['pgrep', '-af', 'kicad'], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            parts = line.split()
            # yalniz KiCad GUI surecleri: yolunda "kicad" gecen python/bash
            # (kicad-schematic betikleri) ve kicad-cli sayilmaz
            if len(parts) < 2 or os.path.basename(parts[1]) not in ('kicad', 'eeschema', 'pcbnew'):
                continue
            # baska dizindeki projeyi acan KiCad bu projeyi kilitlemez
            files = [p for p in parts[2:] if p.endswith(('.kicad_pro', '.kicad_sch', '.kicad_pcb'))]
            if not files or any(os.path.dirname(os.path.abspath(p)) == here for p in files):
                hits.append(line)
    return hits


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
