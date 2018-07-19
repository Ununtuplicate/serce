from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)

class ImageBlock(StructBlock):
    """
    Custom 'StructBlock' for using images with associated captions / text and attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(requred=False)
    attribution = CharBlock(required=False)
    
    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"
        
class HeadingBlock(StructBlock):
    """
    Custom 'StructBlock' that allows selection of h2-h4 header sizes
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)
    
    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
        
class BlockQuote(StructBlock):
    """
    Custom 'StructBlock' that allows user to attribute quote to author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='Name of the author')
    
    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"

# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define custom blocks for 'StreamField'
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon = "fa-paragraph",
        template = "blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text = 'Insert a URL to embed, e.g. youtube.com/embed/',
        icon = "fa-s15",
        template = "blocks/embed_block.html")