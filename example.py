from molpharm.pipelines.chembl_data_request import DataRequestPipeline

chembl_pipeline = DataRequestPipeline("P00533")
data = chembl_pipeline.process()
