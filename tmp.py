# def rename_csv_files(directory):
#     # Get list of files in directory
#     files = os.listdir(directory)

#     # Filter only csv files
#     csv_files = [file for file in files if file.endswith(".csv")]

#     for filename in csv_files:
#         # Remove the first 20 characters from filename
#         new_filename = filename[1:]

#         # Rename the file
#         os.rename(
#             os.path.join(directory, filename), os.path.join(directory, new_filename)
#         )
#         print(f"Renamed {filename} to {new_filename}")


# if __name__ == "__main__":
#     # Specify the directory
#     directory = "."  # Change this to your directory

#     # Rename csv files
#     rename_csv_files(directory)
