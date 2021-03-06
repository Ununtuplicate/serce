# Generated by Django 2.0.2 on 2018-07-12 09:15

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0020_add-verbose-name'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('hero_text', models.CharField(help_text='Write an introduction for your website', max_length=255)),
                ('hero_cta', models.CharField(help_text='Text to display on Call to Action', max_length=255, verbose_name='Hero CTA')),
                ('body', wagtail.core.fields.StreamField([('heading_block', wagtail.core.blocks.StructBlock([('heading_text', wagtail.core.blocks.CharBlock(classname='title', required=True)), ('size', wagtail.core.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.core.blocks.RichTextBlock(icon='fa-paragraph', template='blocks/paragraph_block.html')), ('image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(requred=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False))])), ('block_quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock()), ('attribute_name', wagtail.core.blocks.CharBlock(blank=True, label='Name of the author', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert a URL to embed, e.g. youtube.com/embed/', icon='fa-s15', template='blocks/embed_block.html'))], blank=True, verbose_name='Home content block')),
                ('promo_title', models.CharField(blank=True, help_text='Title to display above your promotional image', max_length=255, null=True)),
                ('promo_text', wagtail.core.fields.RichTextField(blank=True, help_text='Write the text for your promotional area here', null=True)),
                ('featured_section_1_title', models.CharField(blank=True, help_text='Title to display above this featured section', max_length=255, null=True)),
                ('featured_section_2_title', models.CharField(blank=True, help_text='Title to display above this featured section', max_length=255, null=True)),
                ('featured_section_3_title', models.CharField(blank=True, help_text='Title to display above this featured section', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe this page')),
                ('body', wagtail.core.fields.StreamField([('heading_block', wagtail.core.blocks.StructBlock([('heading_text', wagtail.core.blocks.CharBlock(classname='title', required=True)), ('size', wagtail.core.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.core.blocks.RichTextBlock(icon='fa-paragraph', template='blocks/paragraph_block.html')), ('image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(requred=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False))])), ('block_quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock()), ('attribute_name', wagtail.core.blocks.CharBlock(blank=True, label='Name of the author', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert a URL to embed, e.g. youtube.com/embed/', icon='fa-s15', template='blocks/embed_block.html'))], blank=True, verbose_name='Page body')),
                ('image', models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000 and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='newhomepage',
            name='featured_section_1',
            field=models.ForeignKey(blank=True, help_text='First featured section for HomePage. Displays up to three child items', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Featured section 1'),
        ),
        migrations.AddField(
            model_name='newhomepage',
            name='featured_section_2',
            field=models.ForeignKey(blank=True, help_text='Second featured section for HomePage. Displays up to three child items', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Featured section 2'),
        ),
        migrations.AddField(
            model_name='newhomepage',
            name='featured_section_3',
            field=models.ForeignKey(blank=True, help_text='Third featured section for HomePage. Displays up to six child items', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Featured section 3'),
        ),
        migrations.AddField(
            model_name='newhomepage',
            name='hero_cta_link',
            field=models.ForeignKey(blank=True, help_text='Choose a page to link as your Call to Action', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Hero CTA link'),
        ),
        migrations.AddField(
            model_name='newhomepage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Homepage image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='newhomepage',
            name='promo_image',
            field=models.ForeignKey(blank=True, help_text='Promotional Image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
