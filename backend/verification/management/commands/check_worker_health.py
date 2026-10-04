from django.core.management.base import BaseCommand
from config.celery import app as celery_app
from verification.models import NoteProcessingJob


class Command(BaseCommand):
    help = "Inspects Celery worker status, broker connectivity, and pending processing jobs."

    def handle(self, *args, **options):
        self.stdout.write("Inspecting Celery worker pool...")

        # 1. Ping active workers
        try:
            inspector = celery_app.control.inspect(timeout=3.0)
            ping_results = inspector.ping()
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Failed to connect to broker: {exc}"))
            return

        if not ping_results:
            self.stderr.write(self.style.WARNING("⚠️ No active Celery workers found!"))
        else:
            for worker_name, response in ping_results.items():
                self.stdout.write(self.style.SUCCESS(f"✔ Worker online: {worker_name} ({response.get('ok')})"))

        # 2. Inspect active & reserved task queues
        active_tasks = inspector.active() or {}
        total_active = sum(len(tasks) for tasks in active_tasks.values())
        self.stdout.write(f"Active tasks across workers: {total_active}")

        # 3. Query stuck or pending jobs in the database
        stuck_jobs = NoteProcessingJob.objects.filter(
            status=NoteProcessingJob.STATUS_PROCESSING
        ).count()
        if stuck_jobs > 0:
            self.stdout.write(self.style.WARNING(f"⚠️ {stuck_jobs} jobs currently in 'PROCESSING' state."))
        else:
            self.stdout.write(self.style.SUCCESS("✔ No stuck processing jobs in database."))