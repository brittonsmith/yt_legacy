from yt.frontends.gadget.data_structures import GadgetHDF5Dataset
from yt.frontends.sph.data_structures import SPHParticleIndex

class LegacyIndex(SPHParticleIndex):
    @property
    def chunksize(self):
        return 256**3

class LegacyGadgetDataset(GadgetHDF5Dataset):
    _index_class = LegacyIndex

    def _get_hvals(self):
        hvals = super()._get_hvals()
        for par in ["BoxSize", "OmegaLambda", "Omega0", "HubbleParam"]:
            hvals[par] = float(hvals[par])

        return hvals

