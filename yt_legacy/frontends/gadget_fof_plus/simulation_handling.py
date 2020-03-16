"""
Simulation class for GadgetFOFPlus frontend.




"""

#-----------------------------------------------------------------------------
# Copyright (c) 2017, Britton Smith.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import glob
import os

from yt.frontends.gadget.simulation_handling import \
    GadgetSimulation
from yt.convenience import \
    load
from yt.funcs import \
    only_on_root
from yt.utilities.exceptions import \
    YTOutputNotIdentified
from yt.utilities.logger import ytLogger as \
    mylog
from yt.utilities.parallel_tools.parallel_analysis_interface import \
    parallel_objects

class GadgetFOFPlusSimulation(GadgetSimulation):

    def _get_all_outputs(self, find_outputs=False):
        """
        Get all potential datasets and combine into a time-sorted list.
        """

        # Find the data directory where the outputs are
        self._find_data_dir()

        # Create the set of outputs from which further selection will be done.
        if find_outputs:
            self._find_outputs()
        else:
            if self.parameters["OutputListOn"]:
                fn = self.parameters["OutputListFilename"]
                if os.path.exists(fn):
                    a_values = [float(a) for a in 
                                open(fn, "r").readlines()]
                else:
                    a_values = []
            else:
                a_values = [float(self.parameters["TimeOfFirstFOF"])]
                time_max = float(self.parameters["TimeMax"])
                while a_values[-1] < time_max:
                    if self.cosmological_simulation:
                        a_values.append(
                            a_values[-1] * self.parameters["TimeBetFOF"])
                    else:
                        a_values.append(
                            a_values[-1] + self.parameters["TimeBetFOF"])
                if a_values[-1] > time_max:
                    a_values[-1] = time_max

            if self.cosmological_simulation:
                self.all_outputs = \
                  [{"filename": self._snapshot_format(i),
                    "redshift": (1. / a - 1)}
                   for i, a in enumerate(a_values)]
                
                # Calculate times for redshift outputs.
                for output in self.all_outputs:
                    output["time"] = self.cosmology.t_from_z(output["redshift"])
            else:
                self.all_outputs = \
                  [{"filename": self._snapshot_format(i),
                    "time": self.quan(a, "code_time")}
                   for i, a in enumerate(a_values)]

            self.all_outputs.sort(key=lambda obj:obj["time"].to_ndarray())

    def _find_outputs(self):
        """
        Search for directories matching the data dump keywords.
        If found, get dataset times py opening the ds.
        """
        potential_outputs = glob.glob(self._snapshot_format())
        self.all_outputs = self._check_for_outputs(potential_outputs)
        self.all_outputs.sort(key=lambda obj: obj["time"])
        only_on_root(mylog.info, "Located %d total outputs.", len(self.all_outputs))

        # manually set final time and redshift with last output
        if self.all_outputs:
            self.final_time = self.all_outputs[-1]["time"]
            if self.cosmological_simulation:
                self.final_redshift = self.all_outputs[-1]["redshift"]

    def _snapshot_format(self, index=None):
        """
        The snapshot filename for a given index.  Modify this for different 
        naming conventions.
        """

        return os.path.join(
            self.data_dir, "groups_*/fof_subhalo_tab_*.0.hdf5")

    def _check_for_outputs(self, potential_outputs):
        r"""
        Check a list of files to see if they are valid datasets.
        """

        only_on_root(mylog.info, "Checking %d potential outputs.", 
                     len(potential_outputs))

        my_outputs = {}
        llevel = mylog.level
        # suppress logging as we load every dataset, unless set to debug
        if llevel > 10 and llevel < 40:
            mylog.setLevel(40)
        for my_storage, output in parallel_objects(potential_outputs, 
                                                   storage=my_outputs):
            if os.path.exists(output):
                try:
                    ds = load(output)
                    if ds is not None:
                        my_storage.result = {"filename": output,
                                             "time": ds.current_time.in_units("s")}
                        if ds.cosmological_simulation:
                            my_storage.result["redshift"] = ds.current_redshift
                except YTOutputNotIdentified:
                    mylog.error("Failed to load %s", output)
        mylog.setLevel(llevel)
        my_outputs = [my_output for my_output in my_outputs.values() \
                      if my_output is not None]
        return my_outputs
