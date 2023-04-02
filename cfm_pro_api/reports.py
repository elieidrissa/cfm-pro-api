from django.db.models import Sum, Count, Avg
from .models import Lot, Cooperative
from dataclasses import dataclass



@dataclass
class ReportEntry:
    cooperative: Cooperative
    colis: int
    poids: int


def lot_report():
    data = []
    queryset = Lot.objects.values('cooperative').annotate(
        count = Count('id'),
        colis = Sum('colis'),
        poids = Sum('poids')
    )
    for entry in queryset:
        cooperative = Cooperative
        report_entry = ReportEntry(cooperative, entry['colis'], entry['poids'], entry['count'])
        data.append(report_entry)
    return data

output = lot_report()