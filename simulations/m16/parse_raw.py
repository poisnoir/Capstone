#!/usr/bin/env python3
"""Minimal LTspice ASCII .raw reader + DFT for the M16 simulations."""
import sys, math, cmath

def read_raw(path):
    lines = open(path, errors="replace").read().splitlines()
    plot = ""
    flags = ""
    nvar = npts = 0
    vars_ = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("Plotname:"):
            plot = s.split(":", 1)[1].strip()
        elif s.startswith("Flags:"):
            flags = s.split(":", 1)[1].strip()
        elif s.startswith("No. Variables:"):
            nvar = int(s.split(":", 1)[1])
        elif s.startswith("No. Points:"):
            npts = int(s.split(":", 1)[1])
        elif s.startswith("Variables:"):
            for j in range(nvar):
                i += 1
                parts = lines[i].split()
                vars_.append(parts[1] if len(parts) > 1 else parts[0])
        elif s.startswith("Values:"):
            break
        i += 1
    i += 1
    complex_data = "complex" in flags
    xs = []
    cols = [[] for _ in range(nvar)]
    while i < len(lines) and len(xs) < npts:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        parts = s.split()
        # point line starts with an integer index
        if not parts[0].isdigit():
            i += 1
            continue
        xstr = parts[1] if len(parts) > 1 else ""
        def parse(tok):
            if complex_data:
                re, im = tok.split(",")
                return complex(float(re), float(im))
            return float(tok)
        x = parse(xstr)
        xs.append(x)
        cols[0].append(x)
        for k in range(1, nvar):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            cols[k].append(parse(lines[i].strip().split()[0]))
        i += 1
    return {"plot": plot, "flags": flags, "vars": vars_, "x": xs, "cols": cols}

def dft_at(t, v, f, start_frac=0.2):
    n0 = int(len(t) * start_frac)
    n1 = len(t)
    N = n1 - n0
    re = im = 0.0
    for n in range(n0, n1):
        w = 0.5 - 0.5 * math.cos(2 * math.pi * (n - n0) / (N - 1))
        ph = 2 * math.pi * f * t[n]
        re += v[n] * w * math.cos(ph)
        im -= v[n] * w * math.sin(ph)
    return 2 * math.hypot(re, im) / N

if __name__ == "__main__":
    path = sys.argv[1]
    r = read_raw(path)
    print(r["plot"], r["flags"], r["vars"], len(r["x"]))
    if r["plot"].startswith("AC"):
        x = r["x"]; y = r["cols"][r["vars"].index("V(out)")]
        for f in [20e3, 34e3, 60e3, 165.8e3]:
            # nearest
            k = min(range(len(x)), key=lambda j: abs(x[j] - f))
            print(f"{f/1e3:.1f} kHz: {20*math.log10(abs(y[k])):.2f} dB, {math.degrees(cmath.phase(y[k])):.1f} deg")
    else:
        t = r["x"]; y = [c.real if isinstance(c, complex) else c for c in r["cols"][r["vars"].index("V(out)")]]
        for f in [24e3, 23.9e3, 24.1e3]:
            print(f"{f/1e3:.1f} kHz: {20*math.log10(dft_at(t,y,f)/0.15):.2f} dBc")
