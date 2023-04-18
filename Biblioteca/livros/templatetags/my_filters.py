from django import template
import utils

register = template.Library()


@register.filter
def subtrai(value1, value2):

    resultado = utils.subtrai(value1, value2)
    if not resultado:
        return 0
    return resultado.days
