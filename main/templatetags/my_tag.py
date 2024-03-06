from django import template
import datetime
from main.models import *
register = template.Library()


@register.simple_tag
def payment_True_or_False(summa,payment_summa):
    index = len(payment_summa)
    if summa <= payment_summa[index-1].summa:
        return "✅"
    if payment_summa[index-1].summa == 0:
        return '❌'
    if payment_summa[index-1].summa > 0 and  payment_summa[index-1].summa < summa:
        return '🟨'

@register.simple_tag
def payment_summa(objects):
    index = len(objects)
    return  objects[index-1].summa


@register.simple_tag
def came_and_went(text):
    text = text.split(',')
    number = 0
    for i in text:
        if len(i) == 10:
            number+=1
    return number

@register.simple_tag
def color(lop):
    if lop % 2 == 0:
        return 'alert alert-warning '
    return 'alert alert-dark'

@register.simple_tag
def customer_days(came_and_went , total_summa , working_day  ):
    came_and_went = came_and_went.split(',')
    number = 0
    for i in came_and_went:
        if len(i) == 10:
            number+=1
    summa  = total_summa // working_day
    return summa * number

@register.simple_tag
def month_cost(objects):
    summa = 0
    for i in objects:
        summa += i.summa
    return summa