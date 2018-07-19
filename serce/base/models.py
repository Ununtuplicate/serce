from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .blocks import BaseStreamBlock

class StandardPage(Page):
    """
    Generic content page
    Can be used for any page type that only requires: title, image, introduction, body
    """
    
    introduction = models.TextField(
        help_text='Text to describe this page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000 and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]
    
class NewHomePage(Page):
    """
    Home Page, split into:
    - Hero area (image with text caption or overlay)
    - Body area
    - Promotion area
    - Moveable featured site sections
    """
    
    # Hero area
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )
    hero_text = models.CharField(
        max_length=255,
        help_text='Write an introduction for your website'
    )
    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text='Text to display on Call to Action'
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
        help_text='Choose a page to link as your Call to Action'
    )
    
    # Body area
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )
    
    # Promotional section of HomePage
    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Promotional Image'
    )
    promo_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above your promotional image'
    )
    promo_text = RichTextField(
        null=True,
        blank=True,
        help_text='Write the text for your promotional area here'
    )
    
    # Featured sections on HomePage
    # templates/base/home_page.html
    # treated differently, appear in different areas of HomePage
    # each list their children items that are accessed via children function
    # children function defined on individual Page models (BlogPage, BlogIndexPage, etc)
    featured_section_1_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above this featured section'
    )
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='First featured section for HomePage. Displays up to three child items',
        verbose_name='Featured section 1'
    )
    
    featured_section_2_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above this featured section'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Second featured section for HomePage. Displays up to three child items',
        verbose_name='Featured section 2'
    )
    
    featured_section_3_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above this featured section'
    )
    featured_section_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Third featured section for HomePage. Displays up to six child items',
        verbose_name='Featured section 3'
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('hero_text', classname="full"),
            MultiFieldPanel([
                FieldPanel('hero_cta'),
                PageChooserPanel('hero_cta_link'),
                ])
            ], heading="Hero section"),
        MultiFieldPanel([
            ImageChooserPanel('promo_image'),
            FieldPanel('promo_title'),
            FieldPanel('promo_text'),
        ], heading="Promo section"),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_section_1_title'),
                PageChooserPanel('featured_section_1'),    
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_2_title'),
                PageChooserPanel('featured_section_2'),
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_3_title'),
                PageChooserPanel('featured_section_3'),
                ])
        ], heading="Featured homepage sections", classname="collapsible")
    ]
    
    def __str__(self):
        return self.title
        

class GalleryPage(Page):
    """
    This page lists locations from Collection
    Q object to list any collection in (/admin/collections/) - no items is ok
    Can be used for things other than galleries
    """
    
    introduction = models.TextField(
        help_text='Text to describe this page',
        blank=True
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
        FieldPanel('collection'),
    ]
    
    # Defines what content can be under this parent
    # Blank = no subpages can be added
    subpage_types = []
    

@register_snippet
class FooterText(models.Model):
    """
    This is editable text for site footer
    Uses decorator 'register_snippet' so that it can be accessed via admin
    Accessible on template via template tag defined in base/templatetags/navigation_tags.py
    """
    body = RichTextField()
    
    panels = [
        FieldPanel('body'),
    ]
    
    def __str__(self):
        return "Footer text"
    
    class Meta:
        verbose_name_plural = 'Footer Text'
        
        
@register_snippet
class People(index.Indexed, ClusterableModel):
    """
    Django model to store People objects
    Uses '@register_snippet' decorator so that it can be accessed via admin 
        = via Snippets UI (/admin/snippets/base/people)
        
    'People' uses 'ClusterableModel'
        Allows relationship with another model to be stored locally to the 'parent' model 
        e.g. PageModel
        until parent is explicitly saved
        Allows editor to use 'Preview' button (=preview content) without saving relationships to db
        https://github.com/wagtail/django-modelcluster
    """
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)
    
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    panels = [
        FieldPanel('first_name', classname="col6"),
        FieldPanel('last_name', classname="col6"),
        FieldPanel('job_title'),
        ImageChooserPanel('image')
    ]
    
    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]
    
    @property
    def thumb_image(self):
        # Returns empty string is no profile picture or rendition file can't be found
        try:
            return self.image.get_rendition('fill-50x50').img_tag()
        except:
            return ''
        
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        
        
class CentrumPage(Page):
    """
    Replicate of centrumsercalc.pl
    -Logo inline text,
    -6 picture gallery media area
    -Text area
    """
    
    # Logo inline text area
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Logo image'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
    ]
        
        
        
        
        
        
        
        
        
        
        
        
        
