#!/usr/bin/env python3
import sys, math
from parse_raw import read_raw, dft_at

for path in sys.argv[1:]:
    r = read_raw(path)
    t = r["x"]
    v = [c.real if isinstance(c, complex) else c for c in r["cols"][r["vars"].index("V(out)")]]
    tone = dft_at(t, v, 20e3)
    prod = dft_at(t, v, 24e3)
    p239 = dft_at(t, v, 23.9e3)
    p241 = dft_at(t, v, 24.1e3)
    print(f"{path}: tone20={tone:.6f} prod24={prod:.6g} -> {20*math.log10(prod/tone):.2f} dBc; 23.9={20*math.log10(p239/tone):.2f}; 24.1={20*math.log10(p241/tone):.2f}")
