import cloudComPy as cc  # import the CloudComPy module
import os

"""
    Filters the point clouds in the current working directory using the SOR filter.

    This function loads each .txt file in the working directory as a point cloud,
    applies the SOR filter to the point cloud, and saves the filtered point cloud
    with the same name.

    Raises:
        RuntimeError: If the partialClone operation fails.

    Returns:
        None
"""

working_directory = os.path.dirname(os.path.abspath(__file__))
txt_files = [f for f in os.listdir(working_directory) if f.endswith(".txt")]
for count, txt_file in enumerate(txt_files, start=1):
    cloud = cc.loadPointCloud(os.path.join(working_directory, txt_file))
    refCloud = cc.CloudSamplingTools.sorFilter(cloud) # apply the SOR filter and return a reference to the filtered cloud
    (sorCloud, res) = cloud.partialClone(refCloud) # get the actual filtered cloud
    if res != 0:
        raise RuntimeError 
    sorCloud.setName("sorCloud")
    save = cc.SavePointCloud(sorCloud, os.path.join(working_directory, txt_file))
    if count % 10 == 0:
        percentage = (count / len(txt_files)) * 100
        os.path.dirname(os.path.abspath(__file__))
        print(f"Filtered {percentage:.2f}% of the files in {working_directory.split(os.sep)[-4]}.")
print("Filtered 100% the files.")
print("Task completed!")
os.remove(os.path.abspath(__file__)) # remove the script after completion
