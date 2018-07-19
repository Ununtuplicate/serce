from django import template

from wagtail.core.models import Page

from serce.base.models import FooterText

register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/
# current django version = 2.0.2

@register.simple_tag(takes_context=True)
def get_site_root(context):
    # Returns core.Page
    # Main menu needs site.root_page defined else will return:
    # object attribute error ('str' object has no attribute 'get_children')
    return context['request'].site.root_page

def has_menu_children(page):
    # Used by top_menu property
    # get_children is from Treebeard API
    # https://tabo.pe/projects/django-treebeard/docs/4.0.1/api.html
    return page.get_children().live().in_menu().exists()

def has_children(page):
    # Generic to allow page sto list their children
    return page.get_children().live().exists()

def is_active(page, current_page):
    # gives active state on main nav
    return (current_page.url_path.startswith(page.url_path) if current_page else False)

# Get teop menu items = immediate children of parent page
# has_menu_children method required for Foundation menu
# Foundation menu needs dropdown class that is applied to a parent
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menutem)
        # don't directly check if calling_page is None because template engine can pass empty string
        # to calling_page if variable passed as calling_page does not exist
        menuitem.active = (calling_page.url_path.startswith(menuitem.url_path)
                          if calling_page else False)
        return {
            'calling_page': calling_page,
            'menuitems': menuitems,
            # required by pageurl tag that is used within this template
            'request': context['request'],
        }
    
@register.inclusion_tag('base/include/footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = ""
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().body
        
        return {
            'footer_text': footer_text,
        }