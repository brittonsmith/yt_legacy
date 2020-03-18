from yt.fields.field_info_container import \
    FieldInfoContainer

m_units = "code_mass"
p_units = "code_length"
v_units = "code_velocity"
e_units = "code_mass * code_velocity**2"
a_units = "code_velocity / code_time"

class ConsistentTreesHListFieldInfo(FieldInfoContainer):
    known_other_fields = (
    )

    known_particle_fields = (
    )
