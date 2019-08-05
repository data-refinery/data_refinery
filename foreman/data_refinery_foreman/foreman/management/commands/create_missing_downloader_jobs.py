"""
This command finds Samples that were created and didn't spawned any downloader jobs.
We tried to debug the reasons why this happened on
https://github.com/alexslemonade/refinebio/issues/1391
without any luck.
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from dateutil.parser import parse as parse_date
import time

from data_refinery_common.models import Sample
from data_refinery_common.logging import get_and_configure_logger
from data_refinery_common.job_management import create_downloader_job
from data_refinery_foreman.foreman.performant_pagination.pagination import PerformantPaginator as Paginator

from data_refinery_common import job_lookup

logger = get_and_configure_logger(__name__)

PAGE_SIZE = 2000


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--created-after',
                            type=parse_date,
                            help='Only recreate jobs created after this date')

    def handle(self, *args, **options):
        """ Requeues downloader jobs for samples that haven't been processed and their original files
        have no no downloader jobs associated with them
        """
        samples_without_downloader = Sample.objects.all()\
                                                   .annotate(original_files_count=Count('original_files'), downloader_job_count=Count('original_files__downloader_jobs'))\
                                                   .filter(is_processed=False, original_files_count__gt=0, downloader_job_count=0)\

        if options.get('created_after', None):
            samples_without_downloader = samples_without_downloader.filter(created_at__gt=options['created_after'])

        samples_without_downloader = samples_without_downloader.prefetch_related("original_files")

        logger.info("Found %d samples without downloader jobs, starting to create them now.", samples_without_downloader.count())

        paginator = Paginator(samples_without_downloader, PAGE_SIZE)
        page = paginator.page()

        while True:
            count = 0
            for sample in page.object_list:
                # ensure a downloader job can be created for the sample before trying to create a new one
                downloader_task = job_lookup.determine_downloader_task(sample_object)
                if downloader_task != job_lookup.Downloaders.NONE:
                    logger.debug("Creating downloader job for a sample.", sample=sample.accession_code)
                    create_downloader_job(sample.original_files.all())
                    count = count + 1

            logger.info("Created %d new downloader jobs because their samples didn't have any.", count)

            if not page.has_next():
                break

            page = paginator.page(page.next_page_number())
