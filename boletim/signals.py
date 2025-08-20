import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Issue, PageImage
from pdf2image import convert_from_path
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

@receiver(post_save, sender=Issue)
def convert_pdf_to_images(sender, instance: Issue, created, **kwargs):
    """Converte o PDF recém-enviado em imagens e cria PageImage para cada página.
    Se já existirem páginas (re-upload), apaga e reconstrói.
    """
    pdf_path = instance.pdf.path
    # Remove páginas antigas se houver
    instance.pages.all().delete()

    poppler_path = os.getenv('POPPLER_PATH', None) or None

    # Converte em imagens (300 DPI para boa legibilidade)
    pil_images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)

    out_dir = settings.MEDIA_ROOT / 'issues' / instance.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    for idx, img in enumerate(pil_images, start=1):
        # Otimiza e salva JPG
        img = img.convert('RGB')
        out_file = out_dir / f"page_{idx:02d}.jpg"
        img.save(out_file, format='JPEG', optimize=True, quality=85)

        rel_path = out_file.relative_to(settings.MEDIA_ROOT)
        PageImage.objects.create(
            issue=instance,
            image=str(rel_path).replace('\\', '/'),
            page_number=idx,
        )