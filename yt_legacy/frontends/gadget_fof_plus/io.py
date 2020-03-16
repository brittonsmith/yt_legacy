"""
GadgetFOFPlus data-file handling function.




"""

#-----------------------------------------------------------------------------
# Copyright (c) 2016, Britton Smith.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from yt.utilities.on_demand_imports import _h5py as h5py

from yt.frontends.gadget_fof.io import \
    IOHandlerGadgetFOFHaloHDF5, \
    subfind_field_list

class IOHandlerGadgetFOFPlusHaloHDF5(IOHandlerGadgetFOFHaloHDF5):
    _dataset_type = "gadget_fof_plus_halo_hdf5"

    def _identify_fields(self, data_file):
        fields = []
        scalar_fields = []
        id_fields = {}
        with h5py.File(data_file.filename, "r") as f:
            for ptype in self.ds.particle_types_raw:
                fields.append((ptype, "particle_identifier"))
                scalar_fields.append((ptype, "particle_identifier"))
                my_fields, my_offset_fields = \
                  subfind_field_list(f[ptype], ptype, data_file.total_particles)
                fields.extend(my_fields)
                scalar_fields.extend(my_fields)

                if "IDs" not in f: continue
                id_fields = []
                for field in f["IDs"]:
                    field_shape = f["IDs"][field].shape
                    if len(field_shape) == 1:
                        id_fields.append((ptype, field))
                    else:
                        id_fields.extend([(ptype, "%s_%d" % (field, i))
                                          for i in range(field_shape[1])])
                fields.extend(id_fields)
        return fields, scalar_fields, id_fields, {}
