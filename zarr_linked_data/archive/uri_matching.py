import json
import zarr

# ----------------------------------------------
###### ARCHIVE COMMENT
# ----------------------------------------------
# Code at the heart of URI matching using zarr
# ----------------------------------------------

def open_metadata_store(path_metadata_store):
    """Open a zarr metadata store and returns it in a dictionary format.
    Parameters:
    path_metadata_store (str): path to the metadata store
    Returns:
    dict_metadata (dict): dictionary containing the metadata store's content
    """
    with open(path_metadata_store) as all_metadata:
        dict_metadata = json.load(all_metadata)
        dict_metadata = dict_metadata["metadata"]
        return dict_metadata


def match_uri(uri, dict_metadata):
    """Match a URI to an @id in a dictionary and extract the associated key i.e. store path.
    Parameters:
    uri (str): URI to be matched
    dict_metadata (dict): dictionary containing the metadata store's content
    Returns:
    key_uri (str): key (path in metastore) associated to the @id matching the URI
    """
    for key, value in dict_metadata.items():
        if "@id" in value.keys():
            if uri == value["@id"]:
                key_uri = key
                return key_uri


def extract_dataset(metadata_path, path_store):
    """Extract the dataset attached to the metadata path/key.
    Parameters:
    metadata_path (str): path to to the dataset specified in the metadata
    store (zarr store): store where to search for the dataset
    Returns:
    data (zarr dataset): dataset
    """
    # the path coming in will be in the format "path/.zattrs" so we strip this last part
    path = metadata_path.split("/.zattrs")[0]
    # all Datasets will be stored as a subentity of their group with the prefix "Dataset"
    uri_data = path + "/" + path.split("/")[-1] + "Dataset"

    # two options: path or store
    # option 1
    # data = zarr.open(path_store + "/" + uri_data,
    #                 mode='r',
    #                 #shape=(9000, 10000),
    #                 #chunks=(900, 1000),
    #                 dtype='float64')
    # option 2
    data = zarr.open(
        path_store,
        mode="r",
        # ho to handle chunking ?
        # shape=(9000, 10000),
        # chunks=(900, 1000),
        dtype="float64",
        path=uri_data,
    )
    return data
