# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details

# import os
# import sys
# sys.path.append("../Utility")
# sys.path.append("../ReconstructionSystem")
# import numpy as np # todo: this is just for testing
# from global_registration import *
# from downloader import *
# from redwood_dataset_trajectory_io import *

import os
import sys
sys.path.append("../Advanced")
sys.path.append("../Utility")
import numpy as np
from common import *
from downloader import *
from fast_global_registration import *
from trajectory_io import *

do_visualization = False


def get_ply_path(dataset_name, id):
    return "%s/%s/cloud_bin_%d.ply" % (dataset_path, dataset_name, id)


def get_log_path(dataset_name):
    return f"{dataset_path}/ransac_{dataset_name}.log"


if __name__ == "__main__":
    # data preparation
    get_redwood_dataset()
    voxel_size = 0.05

    # do RANSAC based alignment
    for dataset_name in dataset_names:
        ply_file_names = get_file_list(f"{dataset_path}/{dataset_name}/", ".ply")
        n_ply_files = len(ply_file_names)

        alignment = []
        for s in range(n_ply_files):
            for t in range(s + 1, n_ply_files):

                print("%s:: matching %d-%d" % (dataset_name, s, t))
                source = read_point_cloud(get_ply_path(dataset_name, s))
                target = read_point_cloud(get_ply_path(dataset_name, t))
                source_down, source_fpfh = preprocess_point_cloud(
                        source, voxel_size)
                target_down, target_fpfh = preprocess_point_cloud(
                        target, voxel_size)

                result = execute_global_registration(
                        source_down, target_down,
                        source_fpfh, target_fpfh, voxel_size)
                success = result.transformation.trace() != 4.0
                # Note: we save inverse of result.transformation
                # to comply with http://redwood-data.org/indoor/fileformat.html
                if not success:
                    print("No resonable solution.")
                else:
                    alignment.append(CameraPose([s, t, n_ply_files],
                            np.linalg.inv(result.transformation)))
                    print(np.linalg.inv(result.transformation))

                if do_visualization:
                    draw_registration_result(source_down, target_down,
                            result.transformation)
        write_trajectory(alignment, get_log_path(dataset_name))

    # do evaluation
