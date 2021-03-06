"""
Data structures for GadgetFOFPlus frontend.




"""

#-----------------------------------------------------------------------------
# Copyright (c) 2016, Britton Smith.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from yt.utilities.on_demand_imports import _h5py as h5py

from yt.frontends.gadget_fof.data_structures import \
    GadgetFOFDataset, \
    GadgetFOFParticleIndex, \
    GadgetFOFHDF5File, \
    GadgetFOFHaloDataset, \
    GadgetFOFHaloParticleIndex

from yt.frontends.gadget_fof.fields import \
    GadgetFOFFieldInfo

from .fields import \
    GadgetFOFPlusHaloFieldInfo

class GadgetFOFPlusDataset(GadgetFOFDataset):
    _index_class = GadgetFOFParticleIndex
    _file_class = GadgetFOFHDF5File
    _field_info_class = GadgetFOFFieldInfo

    _instantiated_halo_ds = None
    @property
    def _halos_ds(self):
        if self._instantiated_halo_ds is None:
            self._instantiated_halo_ds = GadgetFOFPlusHaloDataset(self)
        return self._instantiated_halo_ds

    @classmethod
    def _is_valid(self, *args, **kwargs):
        need_groups = ['Group', 'Header', 'Subhalo', 'IDs/MemberMass']
        veto_groups = ['FOF']
        valid = True
        try:
            fh = h5py.File(args[0], mode='r')
            valid = all(ng in fh["/"] for ng in need_groups) and \
              not any(vg in fh["/"] for vg in veto_groups)
            fh.close()
        except:
            valid = False
            pass
        return valid

class GadgetFOFPlusHaloDataset(GadgetFOFHaloDataset):
    _index_class = GadgetFOFHaloParticleIndex
    _file_class = GadgetFOFHDF5File
    _field_info_class = GadgetFOFPlusHaloFieldInfo

    def __init__(self, ds, dataset_type="gadget_fof_plus_halo_hdf5"):
        super(GadgetFOFPlusHaloDataset, self).__init__(
            ds, dataset_type)
