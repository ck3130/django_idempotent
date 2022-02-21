# custom template tag
@register.simple_tag(takes_context=True)
def idempotent_token(context):
    token = context['idempo_token']
    html = format_html('<input type="hidden" name="idempo_token" value="{}">', token)
    return html
