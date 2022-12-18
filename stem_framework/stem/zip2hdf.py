import zipfile
import h5py
import numpy as np

def read_zip_print_hdf5(input_path, output_path, header_size=24, size_of_innermost_array=1024, dtype='float32', dataset_name='_'):
    with zipfile.ZipFile(input_path) as input_file:

        nstreams = len(input_file.namelist())
        subfile_size = input_file.filelist[0].file_size
        entry_size = size_of_innermost_array * np.dtype(dtype).itemsize
        N_entries = subfile_size // (entry_size + header_size)
        assert N_entries * (entry_size + header_size) == subfile_size

        with h5py.File(output_path, 'w') as output_file:
            dataset = output_file.create_dataset(dataset_name, (N_entries, nstreams, size_of_innermost_array), dtype)
            for channel_no, filename in enumerate(input_file.namelist()):
                with input_file.open(filename) as subfile:
                    for entry_no in range(N_entries):
                        subfile.seek(header_size, 1)
                        entry = np.frombuffer(subfile.read(entry_size), dtype)
                        dataset[entry_no, channel_no, :] = entry