import pcbnew
import subprocess
import json

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
stackup = board.GetStackupDescriptor()

print("Current Stackup:")
for item in stackup.GetStackupItems():
    print(f"  Name: {item.GetLayerName()}, Type: {item.GetType()}, Thickness: {item.GetThickness()/1e6:.4f} mm, Er: {item.GetEpsilonR():.2f}")
