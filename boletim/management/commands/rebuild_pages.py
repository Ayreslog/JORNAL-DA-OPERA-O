from django.core.management.base import BaseCommand
from django.conf import settings
from pdf2image import convert_from_path
from boletim.models import Issue, PageImage

class Command(BaseCommand):
    help = 'Regera as imagens a partir do PDF para uma Issue específica (por slug) ou todas.'

    def add_arguments(self, parser):
        parser.add_argument('--slug', type=str, help='Slug da edição (opcional).')
        parser.add_argument('--dpi', type=int, default=200)

    def handle(self, *args, **opts):
        slug = opts.get('slug')
        dpi = opts.get('dpi')
        qs = Issue.objects.filter(slug=slug) if slug else Issue.objects.all()
        for issue in qs:
            self.stdout.write(self.style.WARNING(f'Regerando {issue}...'))
            issue.pages.all().delete()
            pil_images = convert_from_path(issue.pdf.path, dpi=dpi)
            out_dir = settings.MEDIA_ROOT / 'issues' / issue.slug
            out_dir.mkdir(parents=True, exist_ok=True)
            for idx, img in enumerate(pil_images, start=1):
                img = img.convert('RGB')
                out_file = out_dir / f"page_{idx:02d}.jpg"
                img.save(out_file, format='JPEG', optimize=True, quality=85)
                rel_path = out_file.relative_to(settings.MEDIA_ROOT)
                PageImage.objects.create(issue=issue, image=str(rel_path), page_number=idx)
        self.stdout.write(self.style.SUCCESS('Concluído.'))