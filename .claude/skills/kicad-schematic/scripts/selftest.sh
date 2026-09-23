#!/bin/sh
# Ortam oz-testi: kicad-schematic + kicad-footprint araclari bu makinede
# (Linux / Windows Git Bash) calisiyor mu. Yazma yapmaz; ciktilar gecici dizine.
#   sh .claude/skills/kicad-schematic/scripts/selftest.sh     (depo kokunden)
# Her adim OK/HATA yazar; sonda ozet. Ciktiyi oldugu gibi paylas.
cd "$(dirname "$0")/../../../.." || exit 1          # depo koku
SK=.claude/skills/kicad-schematic/scripts
FK=.claude/skills/kicad-footprint/scripts
OUT=$(mktemp -d 2>/dev/null || echo /tmp/kicad-selftest.$$); mkdir -p "$OUT"
fail=0
step() {  # step "ad" komut...
    name=$1; shift
    echo "== $name"
    if "$@" > "$OUT/log" 2>&1; then echo "OK"; tail -n 6 "$OUT/log"
    else echo "HATA ($?)"; tail -n 25 "$OUT/log"; fail=$((fail + 1)); fi
}
echo "OS: $(uname -a)"; echo "cikti: $OUT"
step "kpy yorumlayici" sh $SK/kpy -c "import sys; print(sys.executable, sys.version.split()[0])"
step "ortam katmani" sh $SK/kpy -c "
import sys; sys.path.insert(0, '$SK'); import kicadtools as K
print('kicad-cli', K.kicad_cli())
for k in ('symbols', 'footprints', '3dmodels', 'template'): print(k, K.kicad_share(k))
print('pcbnew python', K.kicad_python())
print('Device sembol', K.kicad_symbol_lib('Device'))
print('kilit', K.kicad_open('hardware'))"
step "PyMuPDF var mi (yoksa yedek kullanilir)" sh $SK/kpy -c "
try:
    import fitz; print('fitz', fitz.__doc__.split()[1] if fitz.__doc__ else 'var')
except ImportError: print('fitz YOK -> pdftoppm/pdftotext')
import shutil; print('pdftoppm', shutil.which('pdftoppm'), 'pdftotext', shutil.which('pdftotext'))"
step "view.py metin" sh $SK/kpy $SK/view.py hardware/datasheets/CH9121DS1.PDF --text --pages 10
step "view.py render" sh $SK/kpy $SK/view.py hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf --page 1 --dpi 100 -o "$OUT/sch.png"
if ! command -v pdftoppm >/dev/null 2>&1; then echo "== view.py pdftoppm yedegi: ATLANDI (pdftoppm yok; Windows'ta beklenen)"; else
step "view.py pdftoppm/pdftotext yedegi" env VIEW_NO_FITZ=1 sh -c "sh $SK/kpy $SK/view.py hardware/datasheets/CH9121DS1.PDF --text --pages 10 | head -5 && sh $SK/kpy $SK/view.py hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf --page 1 --dpi 100 -o '$OUT/sch2.png'"
fi
step "render.py sayfa listesi" sh -c "cd hardware && sh ../$SK/kpy ../$SK/render.py gopo.kicad_sch --list -o '$OUT/r'"
step "verify.py ERC + netlist" sh -c "cd hardware && sh ../$SK/kpy ../$SK/verify.py gopo.kicad_sch --save '$OUT/base.net'"
step "update_pcb.py --dry-run (pcbnew)" sh -c "cd hardware && sh ../$SK/kpy ../$SK/update_pcb.py gopo.kicad_pcb --dry-run; echo cikis=\$?"
step "fp_check.py --3d" sh $SK/kpy $FK/fp_check.py hardware/libraries/Module_Custom.pretty Waveshare_2-CH_UART_TO_ETH -o "$OUT/fp" --3d
step "ornek yeniden uretim = depodaki dosya" sh -c "sh $SK/kpy .claude/skills/kicad-footprint/examples/waveshare_2ch_uart_to_eth.py --root '$OUT/lib' >/dev/null &&
    cmp '$OUT/lib/Module_Custom.pretty/Waveshare_2-CH_UART_TO_ETH.kicad_mod' hardware/libraries/Module_Custom.pretty/Waveshare_2-CH_UART_TO_ETH.kicad_mod &&
    cmp '$OUT/lib/Module_Custom.3dshapes/Waveshare_2-CH_UART_TO_ETH.step' hardware/libraries/Module_Custom.3dshapes/Waveshare_2-CH_UART_TO_ETH.step && echo ayni"
step "backlog hook komutu" sh -c "CLAUDE_PROJECT_DIR=\$PWD sh $SK/kpy software/backlog_ascii.py"
step "git calisma kopyasi temiz mi (kicad-cli yan etkisi)" sh -c "git status --short hardware/ | grep -v '^??' ; true"
echo "== OZET: $fail hata"
exit $fail
