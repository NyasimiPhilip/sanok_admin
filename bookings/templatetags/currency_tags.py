from django import template

register = template.Library()


@register.filter(name='currency')
def currency(value, country):
    """
    Format currency based on country
    Usage: {{ booking.amount|currency:booking.country }}
    """
    if value is None:
        return ""
    
    symbol_map = {
        'kenya': 'KSh',
        'uganda': 'USh',
        'zambia': 'ZK',
        'south_africa': 'R',
    }
    
    symbol = symbol_map.get(country, '$')
    
    try:
        amount = float(value)
        return f"{symbol} {amount:,.2f}"
    except (ValueError, TypeError):
        return f"{symbol} {value}"


@register.filter(name='currency_symbol')
def currency_symbol(country):
    """
    Get currency symbol for a country
    Usage: {{ booking.country|currency_symbol }}
    """
    symbol_map = {
        'kenya': 'KSh',
        'uganda': 'USh',
        'zambia': 'ZK',
        'south_africa': 'R',
    }
    
    return symbol_map.get(country, '$')


@register.filter(name='currency_code')
def currency_code(country):
    """
    Get currency code for a country
    Usage: {{ booking.country|currency_code }}
    """
    code_map = {
        'kenya': 'KES',
        'uganda': 'UGX',
        'zambia': 'ZMW',
        'south_africa': 'ZAR',
    }
    
    return code_map.get(country, 'USD')
