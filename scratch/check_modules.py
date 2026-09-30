for mod in ['PIL', 'cairosvg', 'matplotlib', 'svglib', 'reportlab']:
    try:
        __import__(mod)
        print(f"Module {mod}: available")
    except ImportError:
        print(f"Module {mod}: NOT available")
