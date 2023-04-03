def get_lots_stats(queryset):
    '''Extract stats from a given lots' 'queryset' '''
    stats ={'total_poids_Ta':0,
            'total_poids_Sn':0,
            'total_poids_W':0,
            'total_colis_Ta':0,
            'total_colis_Sn':0,
            'total_colis_W':0}
    for obj in queryset:
        if obj.minerai.symbol == 'Ta':
            stats['total_poids_Ta'] += obj.poids
            stats['total_colis_Ta'] += obj.colis
        elif obj.minerai.symbol == 'Sn':
            stats['total_poids_Sn'] += obj.poids
            stats['total_colis_Sn'] += obj.colis
        elif obj.minerai.symbol == 'W':
            stats['total_poids_W'] += obj.poids
            stats['total_colis_W'] += obj.colis
    return stats