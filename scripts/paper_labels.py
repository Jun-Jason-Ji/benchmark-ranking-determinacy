"""Reader-facing condition labels; internal record and configuration keys stay unchanged.

All multipliers are relative to the nominal setting. Gain scaling multiplies
the arm's stiffness and damping together; the torque limit is the arm joint
drive limit, not an applied external force or the gripper-force limit.
The strings use math syntax shared by LaTeX and Matplotlib.
"""

CONDITION_LABELS = {
    "nominal": "Nominal",
    "iso_x0.25": r"Gain scale $\times0.25$",
    "iso_x4.0": r"Gain scale $\times4$",
    "force_x0.5": r"Torque limit $\times0.5$",
    "fric_x0.4": r"Friction $\times0.4$",
    "dens_x0.5": r"Density $\times0.5$",
}


def condition_label(key):
    """Return a display label for a documented six-condition comparison."""
    return CONDITION_LABELS[key]
