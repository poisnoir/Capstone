"""Field Jacobian + spur budget from Anser MATLAB golden model.

Port of software/anser-matlab-ref/model/spiralCoilDimensionCalc.m and
software/anser-matlab-ref/model/spiralCoilFieldCalcMatrix.m
(thesis Eq.3.17-3.18, Sonntag 2007) with geometry from
software/anser-matlab-ref/fSysSetup.m:90-105
(l=70mm, w=0.5mm, s=0.25mm, N=25, 8 centres).

Computes per-coil dBz/dx,y,z and LS allowance
  Vall = 0.15mm * ||J||,  per-tone = Vall - 10log10(7) - 9.5dB
for the SFDR budget in docs/anser-baseline-findings.md section 7.

Also scans candidate 100/150/200 mm cubes for:
  - ICNIRP linear sum at 250 mA and max current for 27 uT
  - full 8x5 Jacobian condition number / minimum singular value
  - CRLB at a reference per-tone field noise sigma_B
at 3x3x3 positions x 3 pitch x 4 azimuth (first-pass FG-05 gate).

Requires numpy. Run: python3 simulations/field_jacobian.py
"""
import numpy as np

U0 = 4 * np.pi * 1e-7


def spiral_coil_dimension_calc(N, length, width, spacing, thickness, angle):
    z_thick = thickness
    theta_rot = angle
    ll_s = width + spacing
    points_total = 4 * N + 1
    x = np.zeros(points_total)
    y = np.zeros(points_total)
    z = np.zeros(points_total)
    z[(2 * N + 1):] = -z_thick
    segs = np.zeros(4 * N)
    segs[0:3] = length
    i = 1
    for m in range(4, 2 * N + 1, 2):  # MATLAB 4:2:2N
        segs[m - 1:m + 1] = length - i * ll_s
        i += 1
    i_small = i - 1
    for m in range(2 * N, 4 * N, 2):  # MATLAB 2N:2:4N-1
        segs[m - 1:m + 1] = length - i_small * ll_s
        i += 1
        i_small -= 1
    segs[4 * N - 3:4 * N - 1] = length
    segs[4 * N - 1] = length - ll_s
    xt = np.cos([theta_rot, theta_rot + .5 * np.pi,
                 theta_rot + np.pi, theta_rot + 1.5 * np.pi])
    yt = np.sin([theta_rot, theta_rot + .5 * np.pi,
                 theta_rot + np.pi, theta_rot + 1.5 * np.pi])
    q = 0
    for p in range(1, points_total):
        x[p] = xt[q] * segs[p - 1] + x[p - 1]
        y[p] = yt[q] * segs[p - 1] + y[p - 1]
        q = (q + 1) % 4
    xn = np.zeros(points_total + 1)
    yn = np.zeros(points_total + 1)
    zn = np.zeros(points_total + 1)
    xn[0:2 * N + 1] = x[0:2 * N + 1]
    xn[2 * N + 1] = x[2 * N]
    xn[2 * N + 2:] = x[2 * N + 1:]
    yn[0:2 * N + 1] = y[0:2 * N + 1]
    yn[2 * N + 1] = y[2 * N]
    yn[2 * N + 2:] = y[2 * N + 1:]
    zn[0:2 * N + 2] = z[0:2 * N + 2]
    zn[2 * N + 2] = z[2 * N + 1]
    zn[2 * N + 3:] = z[2 * N + 2:]
    if abs(angle - np.pi / 2) < 1e-9:
        xn = xn + length / 2
        yn = yn - length / 2
    else:
        yn = yn - length / np.sqrt(2)
    return xn, yn, zn


def filament_field(xp, yp, zp, px, py, pz, I=1.0):
    ax, ay, az = xp[1:] - xp[:-1], yp[1:] - yp[:-1], zp[1:] - zp[:-1]
    bx, by, bz = xp[1:] - px, yp[1:] - py, zp[1:] - pz
    cx, cy, cz = xp[:-1] - px, yp[:-1] - py, zp[:-1] - pz
    mb = np.sqrt(bx**2 + by**2 + bz**2)
    mc = np.sqrt(cx**2 + cy**2 + cz**2)
    adb = ax * bx + ay * by + az * bz
    adc = ax * cx + ay * cy + az * cz
    qx, qy, qz = az * cy - ay * cz, ax * cz - az * cx, cx * ay - cy * ax
    m2 = np.where(qx**2 + qy**2 + qz**2 == 0, 1e-30,
                  qx**2 + qy**2 + qz**2)
    s = ((adc / mc) - (adb / mb)) / m2
    k = I / (4 * np.pi)
    return (np.sum(k * qx * s), np.sum(k * qy * s), np.sum(k * qz * s))


def build_coils():
    l, w, s, th, n = 70e-3, 0.5e-3, 0.25e-3, 1.6e-3, 25
    xa, ya, za = spiral_coil_dimension_calc(n, l, w, s, th, np.pi / 4)
    xv, yv, zv = spiral_coil_dimension_calc(n, l, w, s, th, np.pi / 2)
    xc = np.array([-93.543, 0, 93.543, -68.55, 68.55,
                   -93.543, 0, 93.543]) * 1e-3
    yc = np.array([93.543, 68.55, 93.543, 0, 0,
                   -93.543, -68.55, -93.543]) * 1e-3
    coils = []
    for k in range(8):
        if k in (1, 3, 4, 6):
            coils.append((xa + xc[k], ya + yc[k], za))
        else:
            coils.append((xv + xc[k], yv + yc[k], zv))
    return coils


COILS = build_coils()


def b_field(px, py, pz):
    out = np.zeros((8, 3))
    for i, (xp, yp, zp) in enumerate(COILS):
        hx, hy, hz = filament_field(xp, yp, zp, px, py, pz)
        out[i] = np.array([hx, hy, hz]) * U0
    return out


def unit_vector(theta, phi):
    """Point-sensor normal n = [sin(theta)cos(phi), sin(theta)sin(phi), cos(theta)]."""
    return np.array([np.sin(theta) * np.cos(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(theta)])


def jacobian_5dof(px, py, pz, theta, phi, dx=0.2e-3):
    """8x5 Jacobian of V_i = B_i . n wrt (x,y,z,theta,phi).

    Position derivatives are central differences; orientation derivatives are
    analytic. Rows are the eight coils/tones; units are T/A per metre or per radian.
    """
    b = b_field(px, py, pz)
    n = unit_vector(theta, phi)
    j = np.zeros((8, 5))
    for k, d in enumerate((np.array([dx, 0.0, 0.0]),
                           np.array([0.0, dx, 0.0]),
                           np.array([0.0, 0.0, dx]))):
        bp = b_field(px + d[0], py + d[1], pz + d[2])
        bm = b_field(px - d[0], py - d[1], pz - d[2])
        j[:, k] = ((bp - bm) @ n) / (2.0 * dx)
    dn_dtheta = np.array([np.cos(theta) * np.cos(phi),
                          np.cos(theta) * np.sin(phi),
                          -np.sin(theta)])
    dn_dphi = np.array([-np.sin(theta) * np.sin(phi),
                        np.sin(theta) * np.cos(phi),
                        0.0])
    j[:, 3] = b @ dn_dtheta
    j[:, 4] = b @ dn_dphi
    return j


def conditioning_report(z_bottom, z_top, current=0.25, nxy=3, nz=3,
                        half_xy=0.05,
                        theta_deg=(0.0, 22.5, 45.0),
                        phi_deg=(0.0, 90.0, 180.0, 270.0)):
    """Scan a cube: ICNIRP linear sum, max current, 8x5 conditioning."""
    xs = np.linspace(-half_xy, half_xy, nxy)
    ys = np.linspace(-half_xy, half_xy, nxy)
    zs = np.linspace(z_bottom, z_top, nz)
    thetas = np.deg2rad(theta_deg)
    phis = np.deg2rad(phi_deg)

    max_sum_per_a = 0.0
    min_norm = np.inf
    max_norm = 0.0
    kappas = []
    smins = []
    rank_fail = 0
    worst = None

    for x in xs:
        for y in ys:
            for z in zs:
                b = b_field(x, y, z)
                norms = np.linalg.norm(b, axis=1)
                s = float(np.sum(norms))
                if s > max_sum_per_a:
                    max_sum_per_a = s
                min_norm = min(min_norm, float(np.min(norms)))
                max_norm = max(max_norm, float(np.max(norms)))
                for th in thetas:
                    for ph in phis:
                        j = jacobian_5dof(x, y, z, th, ph)
                        # Scale: position in 100 mm units, angle in radians.
                        js = j * np.array([0.1, 0.1, 0.1, 1.0, 1.0])
                        sv = np.linalg.svd(js, compute_uv=False)
                        if np.linalg.matrix_rank(js) < 5 or sv[-1] <= 1e-18:
                            rank_fail += 1
                            continue
                        kappa = float(sv[0] / sv[-1])
                        smin = float(sv[-1])
                        kappas.append(kappa)
                        smins.append(smin)
                        if worst is None or kappa > worst[0]:
                            worst = (kappa, x, y, z, th, ph, smin)

    kappas = np.array(kappas)
    smins = np.array(smins)
    icnirp = current * max_sum_per_a
    i_max = 27e-6 / max_sum_per_a
    print(f"\ncube {2*half_xy*1e3:.0f} mm side, z={z_bottom*1e3:.1f}-{z_top*1e3:.1f} mm, "
          f"I={current*1e3:.0f} mA, grid {nxy}x{nxy}x{nz} x {len(thetas)}x{len(phis)}")
    print(f"  ICNIRP linear sum @{current*1e3:.0f} mA: {icnirp*1e6:.2f} uT "
          f"(max current for 27 uT: {i_max*1e3:.1f} mA)")
    print(f"  |B_i| per tone @{current*1e3:.0f} mA: min {min_norm*current*1e6:.2f} uT, "
          f"max {max_norm*current*1e6:.2f} uT")
    if kappas.size:
        print(f"  8x5 condition: median {np.median(kappas):.1f}, "
              f"95th {np.percentile(kappas, 95):.1f}, max {np.max(kappas):.1f}")
        print(f"  min singular value: {np.min(smins):.3e} T/A per 0.1 m/rad")
        print(f"  rank<5 poses: {rank_fail} (theta=0 spherical singularity, "
              f"phi undefined; not a field null)")
        if worst is not None:
            k, x, y, z, th, ph, sm = worst
            print(f"  worst pose: kappa={k:.1f} at "
                  f"({x*1e3:.0f},{y*1e3:.0f},{z*1e3:.0f}) mm, "
                  f"theta={np.rad2deg(th):.0f} deg, phi={np.rad2deg(ph):.0f} deg")
    else:
        print("  no full-rank poses")


def crlb_report(z_bottom, z_top, current=0.25, half_xy=0.075, nxy=3, nz=3,
                theta_deg=(0.0, 22.5, 45.0),
                phi_deg=(0.0, 90.0, 180.0, 270.0),
                sigma_b=1e-9, target_pos=0.15e-3, target_ori_deg=0.1):
    """CRLB at a reference per-tone field noise sigma_b (T).

    Reports position/orientation jitter at sigma_b, the sigma_b required for
    the target at the 95th percentile, and the weakest-tone SNR at sigma_b.
    """
    xs = np.linspace(-half_xy, half_xy, nxy)
    ys = np.linspace(-half_xy, half_xy, nxy)
    zs = np.linspace(z_bottom, z_top, nz)
    thetas = np.deg2rad(theta_deg)
    phis = np.deg2rad(phi_deg)

    pos_sig = []
    ori_sig_deg = []
    rank_fail = 0
    min_norm = np.inf

    for x in xs:
        for y in ys:
            for z in zs:
                b = b_field(x, y, z)
                min_norm = min(min_norm, float(np.min(np.linalg.norm(b, axis=1))))
                for th in thetas:
                    for ph in phis:
                        j = jacobian_5dof(x, y, z, th, ph) * current
                        if np.linalg.matrix_rank(j) < 5:
                            rank_fail += 1
                            continue
                        fim = j.T @ j
                        cov = np.linalg.inv(fim) * sigma_b**2
                        pos_sig.append(float(np.sqrt(np.trace(cov[:3, :3]))))
                        ori_sig_deg.append(float(np.rad2deg(
                            np.sqrt(np.trace(cov[3:, 3:])))))

    pos_sig = np.array(pos_sig)
    ori_sig_deg = np.array(ori_sig_deg)
    print(f"\nCRLB {2*half_xy*1e3:.0f} mm side, z={z_bottom*1e3:.1f}-{z_top*1e3:.1f} mm, "
          f"I={current*1e3:.0f} mA, sigma_B={sigma_b*1e9:.2f} nT, "
          f"grid {nxy}x{nxy}x{nz} x {len(thetas)}x{len(phis)}")
    if pos_sig.size == 0:
        print("  no full-rank poses")
        return
    p50, p95, pmax = np.percentile(pos_sig, [50, 95, 100]) * 1e3
    o50, o95, omax = np.percentile(ori_sig_deg, [50, 95, 100])
    print(f"  position 3D jitter: median {p50:.3f} mm, 95th {p95:.3f} mm, max {pmax:.3f} mm")
    print(f"  orientation 3D jitter: median {o50:.3f} deg, 95th {o95:.3f} deg, max {omax:.3f} deg")
    # sigma_B needed to put the 95th percentile at the target
    req_pos = sigma_b * target_pos / (p95 * 1e-3)
    req_ori = sigma_b * target_ori_deg / o95
    req = min(req_pos, req_ori)
    print(f"  required sigma_B for 0.15 mm / 0.1 deg at 95th: "
          f"pos {req_pos*1e9:.3f} nT, ori {req_ori*1e9:.3f} nT, binding {req*1e9:.3f} nT")
    snr_db = 20 * np.log10(min_norm * current / sigma_b)
    print(f"  weakest tone: {min_norm*current*1e6:.3f} uT at {current*1e3:.0f} mA, "
          f"SNR at sigma_B = {snr_db:.1f} dB")
    print(f"  rank<5 poses: {rank_fail} (theta=0 spherical singularity)")


def main():
    dx = 0.2e-3
    for z in (0.066, 0.10, 0.15, 0.20):
        for cx, cy, tag in ((0, 0, "center"), (0.05, 0.05, "off50")):
            p0 = np.array([cx, cy, z])
            b0 = b_field(*p0)
            brms = float(np.sqrt(np.mean(b0[:, 2]**2)))
            J = {}
            for ax, d in (("x", np.array([dx, 0, 0])),
                          ("y", np.array([0, dx, 0])),
                          ("z", np.array([0, 0, dx]))):
                J[ax] = np.array([(b_field(*(p0 + d))[i, 2] -
                                   b_field(*(p0 - d))[i, 2]) / (2 * dx)
                                  for i in range(8)])
            print(f"z={z*1000:.0f}mm {tag} Brms={brms:.3e}")
            for ax in "xyz":
                n = float(np.linalg.norm(J[ax]))
                vall = 0.15e-3 * n
                print(f"  {ax}: |J|={n:.3e} "
                      f"Vall={20*np.log10(vall/brms):+.1f}dB re Brms "
                      f"per-tone={20*np.log10(vall/brms)-18:+.1f}dB")

    conditioning_report(0.050, 0.150, half_xy=0.05)
    for zb in (0.066, 0.0856):
        for size in (0.100, 0.150, 0.200):
            conditioning_report(zb, zb + size, half_xy=size / 2.0)

    for zb, size in ((0.0856, 0.100), (0.0856, 0.150),
                     (0.066, 0.150), (0.0856, 0.200)):
        crlb_report(zb, zb + size, half_xy=size / 2.0)


if __name__ == "__main__":
    main()
