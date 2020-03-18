import numpy as np

from yt.utilities.io_handler import \
    BaseIOHandler

def f_text_block(f, block_size=32768, file_size=None, sep="\n"):
    """
    Read lines from a file faster than f.readlines().
    """
    start = f.tell()
    if file_size is None:
        f.seek(0, 2)
        file_size = f.tell() - start
        f.seek(start)

    nblocks = np.ceil(float(file_size) /
                      block_size).astype(np.int64)
    read_size = file_size + start
    lbuff = ""
    for ib in range(nblocks):
        offset = f.tell()
        my_block = min(block_size, read_size-offset)
        if my_block <= 0: break
        buff = f.read(my_block)
        linl = -1
        for ih in range(buff.count(sep)):
            inl = buff.find(sep, linl+1)
            if inl < 0:
                lbuff += buff[linl+1:]
                continue
            else:
                line = lbuff + buff[linl+1:inl]
                loc = offset - len(lbuff) + linl + 1
                lbuff = ""
                linl = inl
                yield line, loc
        lbuff += buff[linl+1:]
    if lbuff:
        loc = f.tell() - len(lbuff)
        yield lbuff, loc

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

    def _yield_coordinates(self, data_file):
        pos = data_file._get_particle_positions('halos')
        yield 'halos', pos
