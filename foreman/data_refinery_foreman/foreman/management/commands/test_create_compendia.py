from django.test import TransactionTestCase
from django.utils import timezone
from django.core.management import call_command

from data_refinery_common.job_lookup import ProcessorPipeline
from data_refinery_common.models import (ComputationalResult,
                                         ComputedFile,
                                         Dataset,
                                         Experiment,
                                         ExperimentSampleAssociation,
                                         Organism,
                                         ProcessorJob,
                                         ProcessorJobDatasetAssociation,
                                         Sample,
                                         SampleComputedFileAssociation,
                                         SampleResultAssociation,
                                         ExperimentOrganismAssociation)
from data_refinery_foreman.surveyor.test_end_to_end import wait_for_job

from .create_compendia import create_job_for_organism


class CompendiaCommandTestCase(TransactionTestCase):
    def test_quantpendia_command(self):
        self.make_test_data()

        try:
            call_command('create_compendia', organisms='HOMO_SAPIENS', quant_sf_only=True)
        except SystemExit as e:  # this is okay!
            pass

        processor_job = ProcessorJob.objects\
            .filter(pipeline_applied='CREATE_QUANTPENDIA')\
            .order_by('-created_at')\
            .first()

        # check that the processor job was created correctly
        self.assertIsNotNone(processor_job)
        self.assertEquals(processor_job.datasets.first().data, {'GSE51088': ['GSM1237818']})


    def make_test_data(self):
        homo_sapiens = Organism.get_object_for_name("HOMO_SAPIENS")

        experiment = Experiment()
        experiment.accession_code = "GSE51088"
        experiment.save()

        xoa = ExperimentOrganismAssociation()
        xoa.experiment=experiment
        xoa.organism=homo_sapiens
        xoa.save()

        result = ComputationalResult()
        result.save()

        sample = Sample()
        sample.accession_code = 'GSM1237818'
        sample.title = 'GSM1237818'
        sample.organism = homo_sapiens
        sample.save()

        sra = SampleResultAssociation()
        sra.sample = sample
        sra.result = result
        sra.save()

        esa = ExperimentSampleAssociation()
        esa.experiment = experiment
        esa.sample = sample
        esa.save()

        computed_file = ComputedFile()
        computed_file.s3_key = "smasher-test-quant.sf"
        computed_file.s3_bucket = "data-refinery-test-assets"
        computed_file.filename = "quant.sf"
        computed_file.absolute_file_path = "/home/user/data_store/QUANT/smasher-test-quant.sf"
        computed_file.result = result
        computed_file.is_smashable = True
        computed_file.size_in_bytes = 123123
        computed_file.sha1 = "08c7ea90b66b52f7cd9d9a569717a1f5f3874967" # this matches with the downloaded file
        computed_file.save()

        computed_file = ComputedFile()
        computed_file.filename = "logquant.tsv"
        computed_file.is_smashable = True
        computed_file.size_in_bytes = 123123
        computed_file.result = result
        computed_file.save()

        assoc = SampleComputedFileAssociation()
        assoc.sample = sample
        assoc.computed_file = computed_file
        assoc.save()
