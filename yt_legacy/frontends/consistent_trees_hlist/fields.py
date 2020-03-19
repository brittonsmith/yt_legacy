from yt.fields.field_info_container import \
    FieldInfoContainer

m_units = "code_mass"
p_units = "code_length"
v_units = "code_velocity"
r_units = "kpc/h"

class ConsistentTreesHListFieldInfo(FieldInfoContainer):
    known_other_fields = (
    )

    known_particle_fields = (
        ("id", ("", ["particle_identifier"], None)),
        ("x", (p_units, ["particle_position_x"], None)),
        ("y", (p_units, ["particle_position_y"], None)),
        ("z", (p_units, ["particle_position_z"], None)),
        ("vx", (v_units, ["particle_velocity_x"], None)),
        ("vy", (v_units, ["particle_velocity_y"], None)),
        ("vz", (v_units, ["particle_velocity_z"], None)),
        ("Mvir", (m_units, ["particle_mass"], None)),
        ("Rvir", (r_units, ["virial_radius"], None)),
    )
