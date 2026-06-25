import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "text.latex.preamble": r"\usepackage{amsmath} \usepackage{amssymb}"
})

# Pure numpy RK4 integrator for y'' = z y to get Airy Ai(z)
def get_airy_ai(z_vals):
    dz = z_vals[1] - z_vals[0]
    y = np.zeros(len(z_vals))
    yp = np.zeros(len(z_vals))
    
    # Start at large z with exponential decay asymptotic
    z_end = z_vals[-1]
    y[-1] = 1e-8
    yp[-1] = -1e-8 * np.sqrt(z_end)
    
    for i in range(len(z_vals)-2, -1, -1):
        z = z_vals[i+1]
        k1_y = yp[i+1]
        k1_yp = z * y[i+1]
        k2_y = yp[i+1] - dz/2 * k1_yp
        k2_yp = (z - dz/2) * (y[i+1] - dz/2 * k1_y)
        k3_y = yp[i+1] - dz/2 * k2_yp
        k3_yp = (z - dz/2) * (y[i+1] - dz/2 * k2_y)
        k4_y = yp[i+1] - dz * k3_yp
        k4_yp = (z - dz) * (y[i+1] - dz * k3_y)
        
        y[i] = y[i+1] - dz/6 * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        yp[i] = yp[i+1] - dz/6 * (k1_yp + 2*k2_yp + 2*k3_yp + k4_yp)
        
    return y, yp

# Domain of z from first root to positive value
z1 = -2.3381
z_vals = np.linspace(z1, 3.5, 1000)
ai_raw, ai_prime_raw = get_airy_ai(z_vals)

x_c = 1.0 # arbitrary scaling for the plot
x = x_c * (1 - z_vals / z1)
scale_factor = np.max(ai_raw)
ai_vals = ai_raw / scale_factor # normalize peak to 1
ai_prime_vals = ai_prime_raw / scale_factor * (-z1/x_c) # chain rule for dx

fig, ax = plt.subplots(figsize=(10, 6))

# Plot the density
ax.plot(x, ai_vals, color='#1f77b4', linewidth=3.5, label=r'High-Type Density $\rho(x)$')

# Emphasize the left boundary finite slope (Tangent line at x=0)
x_tan = np.linspace(0, 0.3, 10)
y_tan = ai_vals[0] + ai_prime_vals[0] * x_tan
ax.plot(x_tan, y_tan, color='#1f77b4', linestyle=':', linewidth=2, alpha=0.7)

# Emphasize the inflection point at x_c
ai_xc = np.interp(x_c, x, ai_vals)
ai_prime_xc = np.interp(x_c, x, ai_prime_vals)
x_inf_tan = np.linspace(x_c - 0.3, x_c + 0.3, 10)
y_inf_tan = ai_xc + ai_prime_xc * (x_inf_tan - x_c)
ax.plot(x_inf_tan, y_inf_tan, color='black', linestyle=':', linewidth=1.5, alpha=0.5)

# Shade the safe zone (x < x_c)
x_safe = x[x <= x_c]
ai_safe = ai_vals[x <= x_c]
ax.fill_between(x_safe, 0, ai_safe, color='#2ca02c', alpha=0.12)
ax.text(x_c * 0.45, 0.4, r'Safe Zone' + '\n' + r'($V(x) < 0$)' + '\n' + r'$\rho^{\prime\prime} < 0$ (Concave)', ha='center', va='center', fontsize=13, color='#2ca02c')

# Shade the collapse zone (x > x_c)
x_collapse = x[x > x_c]
ai_collapse = ai_vals[x > x_c]
ax.fill_between(x_collapse, 0, ai_collapse, color='#d62728', alpha=0.12)
ax.text(x_c * 1.35, 0.15, r'Collapse Zone' + '\n' + r'($V(x) > 0$)' + '\n' + r'$\rho^{\prime\prime} > 0$ (Convex)', ha='center', va='center', fontsize=13, color='#d62728')

# Add vertical line for the turning point
ax.axvline(x_c, color='black', linestyle='--', linewidth=1.5, zorder=0)

# Annotations for key points
ax.annotate(r'Inflection Point ($\rho^{\prime\prime}=0$)' + '\n' + r'Turning Point $x_c \equiv q_{IC}$', 
            xy=(x_c, ai_xc), xytext=(x_c * 1.05, ai_xc * 1.4),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=13)

ax.text(x_c, -0.02, r'$x_c$', ha='center', va='top', fontsize=14)
ax.text(0, -0.02, r'$0$', ha='center', va='top', fontsize=14)

ax.annotate('Exponential Vacuum\n(Evanescent Tail)', xy=(x_c * 1.6, ai_vals[-1]), xytext=(x_c * 1.8, 0.2),
            arrowprops=dict(facecolor='#d62728', shrink=0.05, width=1.5, headwidth=8),
            fontsize=13, color='#d62728')

ax.annotate(r'Finite slope $\rho^\prime(0) > 0$' + '\n' + r'Boundary at first Airy root' + '\n' + r'($\lambda=0$ critical condition)', 
            xy=(0, 0), xytext=(x_c * 0.1, 0.15),
            arrowprops=dict(facecolor='#1f77b4', shrink=0.05, width=1.5, headwidth=8),
            fontsize=13, color='#1f77b4', ha='left')

peak_idx = np.argmax(ai_vals)
ax.annotate('Single Hump\n(No internal zeros)', xy=(x[peak_idx], ai_vals[peak_idx]), xytext=(x[peak_idx]*0.8, ai_vals[peak_idx]*1.05),
            arrowprops=dict(facecolor='#1f77b4', shrink=0.05, width=1.5, headwidth=8),
            fontsize=13, color='#1f77b4')

# Styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.set_xticks([])
ax.set_yticks([])

ax.set_xlim(-0.05, np.max(x))
ax.set_ylim(0, 1.2)

ax.set_xlabel(r'Proximity to Power / Scrutiny $x$', fontsize=15, loc='right')
ax.set_ylabel(r'$\rho(x)$', fontsize=15, rotation=0, loc='top', labelpad=-20)

# Add title indicating the phase
plt.title(r'Critical Snapshot ($q = q^*$ or $\lambda = 0$): The Onset of Top-Down Collapse', fontsize=16, pad=20)

plt.tight_layout()
plt.savefig('/Users/ostensible_paradox/Documents/spence-signal/figures/airy_density_inflection.pdf', bbox_inches='tight')
plt.savefig('/Users/ostensible_paradox/Documents/spence-signal/figures/airy_density_inflection.png', dpi=300, bbox_inches='tight')
print("Successfully generated airy_density_inflection.png")
