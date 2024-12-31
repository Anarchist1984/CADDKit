from molpharm.pipelines.chembl_data_request import DataRequestPipeline

chembl_pipeline = DataRequestPipeline("P00533")
chembl_id = chembl_pipeline.get_chembl_id()
print(chembl_id)
