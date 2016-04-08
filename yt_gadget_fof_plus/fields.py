"""
GadgetFOFPlus-specific fields




"""

#-----------------------------------------------------------------------------
# Copyright (c) 2016, Britton Smith.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from yt.fields.field_info_container import \
    FieldInfoContainer

from yt.frontends.gadget_fof.fields import \
    _particle_fields

m_units = "code_mass"
p_units = "code_length"
v_units = "code_velocity"

class GadgetFOFPlusHaloFieldInfo(FieldInfoContainer):
    known_other_fields = (
    )

    known_particle_fields = _particle_fields + (
        ("ID",              ("", ["member_ids", "member_particle_identifier"], None)),
        ("MemberType",      ("",      ["member_particle_type"], None)),
        ("MemberMass",      (m_units, ["member_particle_mass"], None)),
        ("MemberPot",       (m_units, ["member_particle_potential"], None)),
        ("MemberPotExt",    (m_units, ["member_particle_potential_external"], None)),
        ("MemberPotPM",     (m_units, ["member_particle_potential_pm"], None)),
        ("MemberPos_0",     (p_units, ["member_particle_position_x"], None)),
        ("MemberPos_1",     (p_units, ["member_paritlce_position_y"], None)),
        ("MemberPos_2",     (p_units, ["member_particle_position_z"], None)),
        ("MemberVel_0",     (v_units, ["member_particle_velocity_x"], None)),
        ("MemberVel_1",     (v_units, ["member_paritlce_velocity_y"], None)),
        ("MemberVel_2",     (v_units, ["member_particle_velocity_z"], None)),
        ("MemberGravAcc_0", ("", ["member_particle_acceleration_x"], None)),
        ("MemberGravAcc_1", ("", ["member_paritlce_acceleration_y"], None)),
        ("MemberGravAcc_2", ("", ["member_particle_acceleration_z"], None)),
        ("MemberGravPM_0",  ("", ["member_particle_acceleration_pm_x"], None)),
        ("MemberGravPM_1",  ("", ["member_paritlce_acceleration_pm_y"], None)),
        ("MemberGravPM_2",  ("", ["member_particle_acceleration_pm_z"], None)),
        )
