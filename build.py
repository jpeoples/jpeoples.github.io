import sys

#import jssg
import jssg
import pathlib
import jinja2

def compute_href(render_context, build_dir, inpath, outpath, s, rel_name="href", full_name="fullhref"):
    href = pathlib.Path(outpath).relative_to(build_dir).as_posix()
    additional_ctx = {
        rel_name: href,
        full_name: render_context['base_url'] + href
    }
    return additional_ctx

def push_page(pages, info, additional_info=None):
    if additional_info is not None:
        info = info.copy()
        info.update(additional_info)
    pages.append(info)

def sort_pages(pages, key='date'):
    return sorted(pages, key=lambda x: x[key], reverse=True)

def add_push_to_collection(render_context, inpath, outpath, s, page_collection):
    additional_info = {
        "href": render_context['href'],
        'fullhref': render_context['fullhref']
    }

    additional_ctx = {
        'push_to_collection': lambda x: push_page(page_collection, x, additional_info)
    }

    return additional_ctx

note_jinja_template="""
{{% extends "layouts/note.html" %}}
{{% set date = "{}" %}}
{{% set description %}}
{{% filter markdown %}}
{}
{{% endfilter %}}
{{% endset %}}
{{% set remainder %}}
{{% filter markdown %}}
{}
{{% endfilter %}}
{{% endset %}}
{{%set body_html %}}
{{{{ description }}}}
{{% if remainder.strip() != '' %}}
{{{{remainder }}}}
{{% endif %}}
{{% endset %}}
""".strip()

def format_dt(date):
    return jssg.jinja_utils.date_formatter('%B %d, %Y, %H:%M')(date)

def note_jinja(jinja_file):
    def full_render(fs, inf, outf):
        s, add_ctx = jinja_file._get_immediate_context(fs, inf, outf)
        items = s.split('%%%')
        n = len(items)
        if n > 1:
            dstring = items[1]
        if n > 2:
            desc = items[2]
            remainder = ''
        if n > 3:
            remainder = items[3]

        outs = jinja_file.render(note_jinja_template.format(dstring,  desc, remainder), add_ctx)
        fs.write(outf, outs)
    return full_render

@jinja2.contextfilter
def ensure_fullhref(ctx, val):
    base_url = ctx['base_url']
    fullhref = ctx['fullhref']
    if val.startswith(base_url):
        return val
    elif val.startswith("/"):
        return base_url + val[1:]
    else:
        out = "/".join(fullhref.split("/")[:-1] + [val])
        assert(out.startswith(base_url))
        return out

if __name__ == "__main__":
    # set base url
    base_url = 'https://jpeoples.github.io/'
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        base_url = 'http://localhost:8080/'
        print(base_url)

    rss_loader = jssg.jinja_utils.rss_loader()
    filters = {
            'markdown': jssg.jinja_utils.markdown_filter(include_mdx_math=True),
            'format_date': jssg.jinja_utils.date_formatter(),
            'rss_format_date': jssg.jinja_utils.rss_date,
            'parse_date': jssg.jinja_utils.parse_date,
            'format_datetime': format_dt,
            'ensure_fullhref': ensure_fullhref
        }

    jenv = jssg.jinja_utils.jinja_env(prefix_paths=('layouts',), additional_loaders=(jssg.jinja_utils.rss_loader(),), filters=filters)
    ctx = {'css': 'site.css', 'base_url': base_url}

    jinja_file = jssg.jinja_utils.JinjaFile(jenv, ctx, immediate_context=[
        lambda cx, inf,outf,s: compute_href(cx, 'build', inf, outf, s)
        ])

    blog_entries = []
    jinja_blog = jinja_file.add_immediate_context(
            lambda ctx, inf,outf,s: add_push_to_collection(ctx, inf, outf, s, blog_entries))

    env = jssg.BuildEnv.default('src', 'build')

    blog_files = jssg.list_all_files('src/blog', rel_to='src')
    env.build((
            # ignore drafts, index page, rss feed, and swap files
            (('*.draft.*', '*index*', '*.xml', '*.swp'), None),
            # Process all posts
            (('*.jinja.md', '*.jinja.html'), (jssg.replace_extensions('.html'), jinja_blog.full_render)),
            # Copy any other files under the blog dir
            ('*', (jssg.mirror_path, jssg.copy_file))
            ), blog_files)

    notes = []
    note_files = jssg.list_all_files('src/notes', rel_to='src')
    jinja_notes = jinja_file.add_immediate_context(
            lambda ctx, inf,outf,s: add_push_to_collection(ctx, inf, outf, s, notes))
    note_map = note_jinja(jinja_notes)
    env.build((
            # ignore drafts, index page, rss feed, and swap files
            (('*.draft.*', '*index*', '*.xml', '*.swp'), None),
            # Process all posts
            (('*.md', '*.txt'), (jssg.replace_extensions('.html'), note_map)),
            # Copy any other files under the blog dir
            ('*', (jssg.mirror_path, jssg.copy_file))
            ), note_files)


    blog_entries = sort_pages(blog_entries)
    notes = sort_pages(notes)
    full_archive = sort_pages(blog_entries + notes)
    jinja_file = jinja_file.add_render_context({'posts': blog_entries, 'notes': notes, 'full_archive': full_archive})
    print(notes[0])

    # TODO Come up with a way around the fnmatch issue so that I don't
    # need to indclude src/ everywhere!
    env.build((
        # now process the blog index and rss
        (('*blog/index.jinja.html', '*blog/rss.jinja.xml', '*notes/rss.jinja.xml', '*shared_rss.jinja.xml'), (jssg.remove_internal_extensions, jinja_file.full_render)),
        (('*notes/index.jinja.html'), (jssg.remove_internal_extensions, jinja_file.full_render)),
        # but ignore the rest of the blog files
        (('blog/*', 'notes/*', '*.swp'), None),
        # and build any other jinja pages
        ('*.jinja.md', (jssg.replace_extensions('.html'), jinja_file.full_render)),
        ('*.jinja.*', (jssg.remove_internal_extensions, jinja_file.full_render)),
        # and copy any _other_ files
        ('*', (jssg.mirror_path, jssg.copy_file))
        ), jssg.list_all_files('src'))
