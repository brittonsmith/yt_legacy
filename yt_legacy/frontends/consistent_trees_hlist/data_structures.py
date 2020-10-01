import numpy as np
import re
import stat
import os

from unyt.exceptions import \
    UnitParseError

from yt.data_objects.static_output import \
    Dataset
from yt.frontends.halo_catalog.data_structures import \
    HaloCatalogFile
from yt.funcs import \
    setdefaultattr
from yt.geometry.particle_geometry_handler import \
    ParticleIndex
from yt.utilities.cosmology import \
    Cosmology

from yt_legacy.frontends.consistent_trees_hlist.fields import \
    ConsistentTreesHListFieldInfo
from yt_legacy.frontends.consistent_trees_hlist.io import \
    f_text_block

class CTHLMiniFile(object):
    def __init__(self, ds, filename):
        self.ds = ds
        self.filename = filename

        self.field_info = {}
        self.parameters = {}
        fields = []
        fi = {}
        fdb = {}
        rems = ["%s%s%s" % (s[0], t, s[1])
                for s in [("(", ")"), ("", "")]
                for t in ["physical, peculiar",
                          "comoving", "physical"]]

        fn = os.path.basename(self.filename)
        scale = float(fn[len("hlist_"):-len(".list")])
        self.parameters['current_redshift'] = 1 / scale - 1

        f = open(self.filename, "r")
        # Read the first line as a list of all fields.
        # Do some footwork to remove awkard characters.
        rfl = f.readline()[1:].strip().split()
        reg = re.compile(r"\(\d+\)$")
        for pf in rfl:
            match = reg.search(pf)
            if match is None:
                field_name = pf
            else:
                field_name = pf[:match.start()]
            field_name = field_name.replace('/', '_')
            fields.append(field_name)

        # Now grab a bunch of things from the header.
        while True:
            line = f.readline()
            if line is None:
                raise IOError(
                    "Encountered enexpected EOF reading %s." %
                    self.filename)
            elif not line.startswith("#"):
                self._hoffset = f.tell() - len(line)
                break

            # cosmological parameters
            if "Omega_M" in line:
                pars = line[1:].split(";")
                for j, par in enumerate(["omega_matter",
                                         "omega_lambda",
                                         "hubble_constant"]):
                    v = float(pars[j].split(" = ")[1])
                    self.parameters[par] = v
                self.ds._arr = None
                self.ds._quan = None
                self.ds.unit_registry.modify(
                    "h", self.parameters['hubble_constant'])

            # box size
            elif "Full box size" in line:
                pars = line.split("=")[1].strip().split()
                box = pars
                self.parameters['box_size'] = box

            # These are lines describing the various fields.
            # Pull them apart and look for units.
            elif ":" in line:
                tfields, desc = line[1:].strip().split(":", 1)

                # Units are enclosed in parentheses.
                # Pull out what's enclosed and remove things like
                # "comoving" and "physical".
                if "(" in line and ")" in line:
                    punits = desc[desc.find("(")+1:desc.rfind(")")]
                    for rem in rems:
                        while rem in punits:
                            pre, mid, pos = punits.partition(rem)
                            punits = pre + pos
                    try:
                        self.ds.quan(1, punits)
                    except UnitParseError:
                        punits = ""
                else:
                    punits = ""

                # Multiple fields together on the same line.
                for sep in ["/", ","]:
                    if sep in tfields:
                        tfields = tfields.split(sep)
                        break
                if not isinstance(tfields, list):
                    tfields = [tfields]

                # Assign units and description.
                for tfield in tfields:
                    fdb[tfield.lower()] = {"description": desc.strip(),
                                           "units": punits}

        f.close()

        # Fill the field info with the units found above.
        for i, field in enumerate(fields):
            if "(" in field and ")" in field:
                cfield = field[:field.find("(")]
            else:
                cfield = field
            fi[field] = fdb.get(cfield.lower(),
                                {"description": "",
                                 "units": ""})
            fi[field]["column"] = i

        self.field_list = fields
        self.field_info.update(fi)

    _data_lines = None
    def _count_data_lines(self):
        f = open(self.filename, "r")
        f.seek(self._hoffset)

        sep = "\n"
        block_size = 32768
        start = f.tell()

        f.seek(0, 2)
        file_size = f.tell() - start
        f.seek(start)

        nblocks = np.ceil(float(file_size) /
                          block_size).astype(np.int64)
        read_size = file_size + start

        nsep = 0
        for ib in range(nblocks):
            offset = f.tell()
            my_block = min(block_size, read_size-offset)
            if my_block <= 0: break
            buff = f.read(my_block)
            nsep += buff.count(sep)        
        f.close()

        self.file_size = file_size
        self._data_lines = nsep

class ConsistentTreesHListFile(HaloCatalogFile, CTHLMiniFile):
    def __init__(self, ds, io, filename, file_id, frange):

        CTHLMiniFile.__init__(self, ds, filename)
        HaloCatalogFile.__init__(self,
            ds, io, filename, file_id, frange)

    def _read_fields(self, rfields):
        if not rfields:
            return {}

        fi = self.field_info
        field_data = dict((field, np.empty(self.total_particles['halos']))
                          for field in rfields)

        f = open(self.filename, 'r')
        f.seek(self._hoffset)
        for i, (line, offset) in enumerate(
                f_text_block(f, file_size=self.file_size)):
            sline = line.split()
            for field in rfields:
                field_data[field][i] = float(sline[fi[field]["column"]])
        f.close()

        return field_data

    def _read_particle_positions(self, ptype, f=None):
        field_data = self._read_fields(['x', 'y', 'z'])
        pos = np.vstack([field_data[f] for f in 'xyz']).T
        return pos

class ConsistentTreesHListIndex(ParticleIndex):
    def _setup_filenames(self):
        cls = self.dataset._file_class
        self.data_files = \
          [cls(self.dataset, self.io,
               self.dataset.parameter_filename, 0, None)]
        self.total_particles = sum(
            sum(d.total_particles.values()) for d in self.data_files)

class ConsistentTreesHListDataset(Dataset):
    _index_class = ConsistentTreesHListIndex
    _file_class = ConsistentTreesHListFile
    _field_info_class = ConsistentTreesHListFieldInfo

    def __init__(self, filename, dataset_type="consistent_trees_hlist", **kwargs):
        super(ConsistentTreesHListDataset, self).__init__(filename, dataset_type, **kwargs)

    def _parse_parameter_file(self):
        self.dimensionality = 3
        self.periodicity = (True, True, True)
        self.refine_by = 2
        self.unique_identifier = \
            int(os.stat(self.parameter_filename)[stat.ST_CTIME])
        self.file_count = 1

        ct_file = CTHLMiniFile(self, self.parameter_filename)
        self.parameters.update(ct_file.parameters)

        for par in ['hubble_constant', 'omega_matter',
                    'omega_lambda', 'current_redshift']:
            setattr(self, par, self.parameters.get(par))

        self.cosmological_simulation = 1
        co = Cosmology(hubble_constant=self.hubble_constant,
                       omega_matter=self.omega_matter,
                       omega_lambda=self.omega_lambda)
        self.current_time = co.t_from_z(self.current_redshift)
        self.domain_left_edge = np.zeros(self.dimensionality)
        self.domain_right_edge = float(self.parameters['box_size'][0]) * \
          np.ones(self.dimensionality)
        self.domain_dimensions = np.ones(self.dimensionality, "int32")

    def _set_code_unit_attributes(self):
        setdefaultattr(self, 'length_unit', self.quan(1.0, "Mpc / h"))
        setdefaultattr(self, 'mass_unit', self.quan(1.0, "Msun / h"))
        setdefaultattr(self, 'velocity_unit', self.quan(1.0, "km / s"))
        setdefaultattr(self, 'time_unit', self.length_unit / self.velocity_unit)

    @classmethod
    def _is_valid(self, *args, **kwargs):
        fn = args[0]
        if not os.path.basename(fn).startswith("hlist_") or \
          not fn.endswith(".list"):
            return False
        return True
