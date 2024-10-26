from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        value = d.get(str(key), 'No Value Found')
        print(f"dict_get: key={key}, value={value}")  # 디버깅용 출력
        return value
    return 'Not a dictionary'
