from metaflow import FlowSpec, step, current, Parameter, schedule, kubernetes

@schedule(daily=True)
class MetadataConsolidateFlow(FlowSpec):

    @kubernetes(secrets='argo-artifacts', service_account='argo')
    @step
    def start(self):
        """Download the store."""
        import os
        import s3fs
        #future enhancement, have the path store in the s3 system a parameter
        s3 = s3fs.S3FileSystem(
                endpoint_url=os.environ["AWS_S3_ENDPOINT"],
                key=os.environ["AWS_ACCESS_KEY_ID"],
                secret=os.environ["AWS_SECRET_ACCESS_KEY"])
        self.store = s3fs.S3Map(root='argobucket/zarr_linked_data/data/test_store.zarr', s3=s3, check=False)
        self.next(self.consolidate)

    @kubernetes(secrets='argo-artifacts', service_account='argo')
    @step
    def consolidate(self):
        """Consolidate metadata."""
        import zarr
        zarr.convenience.consolidate_metadata(
            store=self.store,
            metadata_key=".all_metadata"
        )
        self.next(self.end)

    @step
    def end(self):
        """End the consolidation flow."""
        pass


if __name__ == "__main__":
# ----------------------------------------------
    ###### CONSOLIDATE METADATA FLOW
    # ----------------------------------------------
    # call with: 
    # python zarr_linked_data/consolidate_metadata_flow.py run 
    # make an Argo DAG with: 
    # python zarr_linked_data/consolidate_metadata_flow.py --with retry argo-workflows

    MetadataConsolidateFlow()