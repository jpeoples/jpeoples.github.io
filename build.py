import sys

#import jssg
import jssg
import pathlib
import jinja2

def compute_href(render_context, build_dir, inpath, outpath, s, rel_name="href", full_name="fullhref"):
    if outpath.endswith("index.html"):
        outpath = pathlib.Path(outpath).parent.as_posix()
    href = pathlib.Path(outpath).relative_to(build_dir).as_posix() + "/"
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

format_dt = jssg.jinja_utils.date_formatter('%B %d, %Y, %H:%M')

def note_jinja(jinja_file):
    def full_render(fs, inf, outf):
        s = fs.read(inf)
        add_ctx = jinja_file.get_immediate_context(fs, inf, outf, s)
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

def nice_url(fn):
    return pathlib.Path(jssg.remove_extensions(fn), "index.html").as_posix()

@jinja2.contextfilter
def ensure_fullhref(ctx, val):
    base_url = ctx['base_url']
    fullhref = ctx['fullhref']
    if fullhref.endswith("/"):
        fullhref = fullhref[:-1]
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

    env = jssg.Environment.default("src", "build")
    env.jinja_filters.update({
            'format_datetime': format_dt,
            'ensure_fullhref': ensure_fullhref
        })

    jinja_file = env.jinja.add_render_context(
            {"css": "site.css", "base_url": base_url}).add_immediate_context(
                    lambda cx, inf, outf, s: compute_href(cx, "build", inf, outf, s)
                    )

    blog_entries = []
    jinja_blog = jinja_file.add_immediate_context(
            lambda ctx, inf,outf,s: add_push_to_collection(ctx, inf, outf, s, blog_entries))

    env.build((
            # ignore drafts, index page, rss feed, and swap files
            (('*.draft.*', '*index*', '*.xml', '*.swp'), env.ignore_file),
            # Process all posts
            (('*.jinja.md', '*.jinja.html'), (nice_url, jinja_blog.full_render)),
            # Copy any other files under the blog dir
            ('*', env.mirror_file),
            ), "blog")

    notes = []
    jinja_notes = jinja_file.add_immediate_context(
            lambda ctx, inf,outf,s: add_push_to_collection(ctx, inf, outf, s, notes))
    note_map = note_jinja(jinja_notes)
    env.build((
            # ignore drafts, index page, rss feed, and swap files
            (('*.draft.*', '*index*', '*.xml', '*.swp'), None),
            # Process all posts
            (('*.md', '*.txt'), (nice_url, note_map)),
            # Copy any other files under the blog dir
            ('*', env.mirror_file)
            ), "notes")


    blog_entries = sort_pages(blog_entries)
    notes = sort_pages(notes)
    full_archive = sort_pages(blog_entries + notes)
    jinja_file = jinja_file.add_render_context({'posts': blog_entries, 'notes': notes, 'full_archive': full_archive})
    print(notes[0])

    env.build((
        # now process index pages and rss
        (('blog/rss.jinja.xml', 'notes/rss.jinja.xml', 'shared_rss.jinja.xml'), (jssg.remove_internal_extensions, jinja_file.full_render)),
        (('*index.jinja.*'), (jssg.remove_internal_extensions, jinja_file.full_render)),
        # but ignore the rest of the blog files
        (('blog/*', 'notes/*', '*.swp'), None),
        # and build any other jinja pages
        ('*.jinja.md', (nice_url, jinja_file.full_render)),
        ('*.jinja.*', (nice_url, jinja_file.full_render)),
        # and copy any _other_ files
        ('*', env.mirror_file)
        ))
