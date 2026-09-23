"""Ortam katmani: KiCad araclarini ve dizinlerini Windows/Linux/macOS'ta bulur,
dosya G/C yardimcilari (render.py, verify.py, update_pcb.py, kisch_edit.py ve
kicad-footprint betikleri ortak kullanir).

Tum OS farklari BURADA cozulur; betiklere yol, `python`/`python3` veya
`/usr/share/kicad` yazma. Betikleri `sh $SK/kpy betik.py` ile calistir (dogru
python'u secer, PYTHONIOENCODING=utf-8). Ortam degiskeniyle ezilebilir:
    KICAD_CLI, KICAD_PYTHON, KICAD10_SYMBOL_DIR, KICAD10_FOOTPRINT_DIR,
    KICAD10_3DMODEL_DIR, KICAD10_TEMPLATE_DIR

DIKKAT: KiCad'in bin dizinini PATH'in ONUNE eklemek KiCad'le gelen python'u
one cikarir (PyMuPDF yok) - araclari PATH'i degistirmeden, tam yoluyla cagir.
pcbnew gereken betik `ensure_pcbnew()` ile kendini KiCad python'unda yeniden
baslatir.
"""
import glob
import os
import re
import shutil
import subprocess
import sys

# KiCad kurulum kokleri (en yeni surum once). share/ ve bin/ bunlarin altinda.
_WIN_ROOTS = [os.path.expandvars(r'%LOCALAPPDATA%\Programs\KiCad\*'), r'C:\Program Files\KiCad\*']
_SHARE = {  # tur -> (ortam degiskeni, Linux/macOS dizinleri)
    'symbols': ('KICAD10_SYMBOL_DIR', ['/usr/share/kicad/symbols', '/usr/local/share/kicad/symbols',
                                       '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols']),
    'footprints': ('KICAD10_FOOTPRINT_DIR', ['/usr/share/kicad/footprints', '/usr/local/share/kicad/footprints',
                                             '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints']),
    '3dmodels': ('KICAD10_3DMODEL_DIR', ['/usr/share/kicad/3dmodels', '/usr/local/share/kicad/3dmodels',
                                         '/Applications/KiCad/KiCad.app/Contents/SharedSupport/3dmodels']),
    'template': ('KICAD10_TEMPLATE_DIR', ['/usr/share/kicad/template', '/usr/local/share/kicad/template',
                                          '/Applications/KiCad/KiCad.app/Contents/SharedSupport/template']),
}


def _win_hits(rel):
    out = []
    for root in _WIN_ROOTS:
        out += sorted(glob.glob(os.path.join(root, rel)), reverse=True)
    return out


def kicad_cli():
    """kicad-cli'nin tam yolu. KICAD_CLI ortam degiskeni oncelikli."""
    env = os.environ.get('KICAD_CLI')
    if env and os.path.exists(env):
        return env
    p = shutil.which('kicad-cli')
    if p:
        return p
    for p in _win_hits(r'bin\kicad-cli.exe') + ['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli',
                                                 '/usr/bin/kicad-cli', '/usr/local/bin/kicad-cli']:
        if os.path.exists(p):
            return p
    raise FileNotFoundError('kicad-cli bulunamadi; KICAD_CLI ortam degiskenini ayarla')


def kicad_share(kind):
    """KiCad'in paylasilan dizini: 'symbols' | 'footprints' | '3dmodels' | 'template'.

    Linux /usr/share/kicad/<tur>, Windows <kurulum>\\share\\kicad\\<tur>.
    KICAD10_*_DIR ortam degiskeni (ve KICAD9_... gibi eski surum adlari) oncelikli.
    Footprint/3D model yolunu betige elle yazma: update_pcb.py Linux yolu sabit
    oldugu icin Windows'ta calismiyordu."""
    var, unix = _SHARE[kind]
    stem = var.split('_', 1)[1]                       # SYMBOL_DIR ...
    dirs = [v for k, v in sorted(os.environ.items(), reverse=True)
            if re.fullmatch(r'KICAD\d*_' + stem, k)]
    dirs += unix + _win_hits(os.path.join('share', 'kicad', kind))
    for d in dirs:
        if d and os.path.isdir(d):
            return d
    raise FileNotFoundError(f'KiCad {kind} dizini bulunamadi; {var} ayarla')


def kicad_python():
    """pcbnew modulunu yukleyebilen python yorumlayicisi.

    Linux: sistem python3'u (paket /usr/lib/python3/dist-packages/pcbnew.py kurar).
    Windows: KiCad'in kendi python.exe'si (<kurulum>\\bin\\python.exe); C:\\PythonXY
    pcbnew'i goremez. KICAD_PYTHON ortam degiskeni oncelikli."""
    env = os.environ.get('KICAD_PYTHON')
    if env and os.path.exists(env):
        return env
    for p in _win_hits(r'bin\python.exe') + ['/Applications/KiCad/KiCad.app/Contents/Frameworks/'
                                              'Python.framework/Versions/Current/bin/python3']:
        if os.path.exists(p):
            return p
    for name in ('python3', 'python'):
        p = shutil.which(name)
        if p and subprocess.run([p, '-c', 'import pcbnew'], capture_output=True).returncode == 0:
            return p
    raise FileNotFoundError('pcbnew yukleyen python bulunamadi; KICAD_PYTHON ayarla')


def ensure_pcbnew():
    """pcbnew'i yukler; bu yorumlayicida yoksa betigi KiCad python'unda YENIDEN
    BASLATIR (ayni argumanlarla) ve cikis kodunu dondurur. Betigin en basinda:
        from kicadtools import ensure_pcbnew; pcbnew = ensure_pcbnew()
    Boylece `sh kpy update_pcb.py ...` her iki OS'ta da calisir. KiCad
    python'unda PyMuPDF olmadigi icin render isini bu betiklere koyma."""
    try:
        import pcbnew
        return pcbnew
    except ImportError:
        if os.environ.get('_KICADTOOLS_REEXEC'):
            raise
        env = dict(os.environ, _KICADTOOLS_REEXEC='1', PYTHONIOENCODING='utf-8')
        r = subprocess.run([kicad_python(), os.path.abspath(sys.argv[0])] + sys.argv[1:], env=env)
        sys.exit(r.returncode)


def run_cli(args, keep=None, check=True):
    """kicad-cli'yi tam yoluyla calistirir. `keep`: kicad-cli'nin yeniden yazdigi
    .kicad_pro'yu korumak icin girdi dosyasi (.kicad_sch/.kicad_pcb) veya
    dogrudan .kicad_pro yolu. Donus: CompletedProcess (stdout/stderr metin)."""
    pro = project_file(keep) if keep else None
    with keep_file(pro):
        return subprocess.run([kicad_cli()] + list(args), check=check, capture_output=True,
                              text=True, encoding='utf-8', errors='replace')


def kicad_symbol_lib(nick):
    """KiCad'in kendi sembol kutuphanesinin (.kicad_sym) tam yolu.

    Yeni sembol (Timer_RTC:BQ32000, Device:Crystal_GND23, Transistor_FET:
    Q_NMOS_GSD...) eklerken ensure_lib_symbol/swap_lib bu dosyadan kopyalar.
    Dizin `kicad_share('symbols')`; bulamazsa acik hata verir.
    """
    p = os.path.join(kicad_share('symbols'), nick + '.kicad_sym')
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


def kicad_open(project_dir='.', editors_only=False):
    """Proje KiCad'de acik mi: kilit dosyalari (~*.lck) + calisan kicad surecleri.

    Acikken dosyaya yazilan degisiklik KiCad kaydedince EZILIR. Bu oturumda
    kullanici KiCad'i uc kez kapatip yeniden acti; her yazmadan once kontrol et:
        assert not kicad_open(), 'KiCad acik'
    Kilitler: `~gopo.kicad_pro.lck` = yalniz proje yoneticisi acik;
    `~<ad>.kicad_sch.lck` / `~<ad>.kicad_pcb.lck` = o editor acik (Windows'ta
    pgrep yok, kilit dosyasi tek kanit). editors_only=True proje yoneticisi
    kilidini ve surec satirlarini saymaz: yonetici acikken sema/PCB'ye yazmak
    guvenli (editor acilinca diskten okur; 23.09 J8 3D model eklemesi).
    Acikken calismaya devam etmek icin projeyi scratchpad'e kopyalayip betigi
    orada dogrula (SKILL.md "KiCad acikken kuru calistirma").
    Donus: kilit dosyasi / surec satirlari listesi (bos = kapali)."""
    hits = sorted(glob.glob(os.path.join(project_dir, '~*.lck')))
    if editors_only:
        return [h for h in hits if not h.endswith('.kicad_pro.lck')]
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


def project_file(path):
    """.kicad_sch/.kicad_pcb/.kicad_pro yolundan ayni adli .kicad_pro (yoksa None)."""
    pro = os.path.splitext(path)[0] + '.kicad_pro'
    return pro if os.path.exists(pro) else None
