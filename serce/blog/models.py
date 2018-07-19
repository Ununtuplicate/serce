from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

"""
class BlogPeopleRelationship(Orderable, models.Model):
"""
"""
    Defines relationship between 'People' within 'base' app and BlogPage (below); 
    allows People to be atted to BlogPage
    2-way relationship between BlogPage and People using ParentalKey and ForeignKey

    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'base.People', related_name='person_blog_relationship', on_delete=models.CASCADE
    )
    panes = [
        SnippetChooserPanel('people')
    ]
"""


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    
    def get_context(self, request):
        # update context to include only PUBLISHED posts, REVERSE order chronologically
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    
class BlogPageTag(TaggedItemBase):
    """
    Model, many-to-many relationship between BlogPage object and tags
    """
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
    
class BlogTagIndexPage(Page):
    
    def get_context(self, request):
        #filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        
        #update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
    
class BlogPage(Page):
    """
    Access People object with inline panel that references ParentalKey's related_name in BlogPeopleRelationship
    """
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
    
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'blog categories'