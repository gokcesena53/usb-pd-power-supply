"""backlog/ altındaki dosya adlarını ASCII'ye çevirir.

Backlog.md görev/milestone başlığını dosya adına dönüştürürken Türkçe
karakterleri korur. Görev ID'si dosya adının başında olduğu için Backlog.md
yeniden adlandırılmış dosyayı bulmaya devam eder; başlık (dosya içindeki
`title:`) Türkçe kalır.

Kullanım: python software/backlog_ascii.py   (depo kökünden veya herhangi bir yerden)
"""
import pathlib
import unicodedata

TR = str.maketrans("çğıöşüÇĞİÖŞÜâîûÂÎÛ", "cgiosuCGIOSUaiuAIU")
ROOT = pathlib.Path(__file__).resolve().parent.parent / "backlog"


def ascii_name(name: str) -> str:
    name = unicodedata.normalize("NFC", name).translate(TR)
    return unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()


def main() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name.isascii():
            continue
        target = path.with_name(ascii_name(path.name))
        if target.exists():
            raise SystemExit(f"hedef zaten var: {target}")
        path.rename(target)
        print(f"-> {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
