from yt.utilities.io_handler import \
    BaseIOHandler

class IOHandlerConsistentTreesHList(BaseIOHandler):
    _dataset_type = "consistent_trees_hlist"

    def _count_particles(self, data_file):
        if data_file._data_lines is None:
            data_file._count_data_lines()
        return {'halos': data_file._data_lines}

    def _identify_fields(self, data_file):
        fi = data_file.field_info
        units = dict([(field, fi[field].get('units', ''))
                      for field in fi])
        fields = [('halos', field)
                  for field in data_file.field_list]
        return fields, units
