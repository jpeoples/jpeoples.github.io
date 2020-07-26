import sys

#import jssg
import jssg
from jssg.jinja_utils import markdown_filter
import pathlib
import jinja2

import dateutil.parser

def compute_href(render_context, build_dir, inpath, outpath, s, rel_name="href", full_name="fullhref"):
    if outpath.endswith("index.html"):
        outpath = pathlib.Path(outpath).parent.as_posix()
    href = pathlib.Path(outpath).relative_to(build_dir).as_posix() + "/"
    additional_ctx = {
        rel_name: href,
        full_name: render_context['base_url'] + href
    }
    return additional_ctx

def sort_pages(pages, key='date'):
    return sorted(pages, key=lambda x: x[key], reverse=True)


# For now: no touching the context generation stuff. Just using these
# listeners for the sake of implementing the post collections.

class PostCollections:
    def __init__(self):
        self.articles = []
        self.notes = []
        self.blog_chains = {}

    def on_data_return(self, inf, outf, data):
        # For now, we only work with jinja_template
        if data['type'] != "jinja_template": return

        ctx = data['context']
        t = data['template']

        # For every jinja_template: we need to know if it is a blog
        # article. For now, the test will be:
        #   1) has a date; and
        #   2) is in the blog folder


        if ctx['href'].startswith('blog') and hasattr(t, 'date'):
            article_info=dict(
                title = t.title,
                date = dateutil.parser.parse(t.date),
                content = t.body_html,
                description=getattr(t, 'description', None),
                description_is_full=False,
                href = ctx['href'],
                fullhref = ctx['fullhref']
                )
            self.articles.append(article_info)
            if hasattr(t, 'blog_chain'):
                chain_name = t.blog_chain
                chain = self.blog_chains.setdefault(chain_name, [])
                chain.append(article_info)
        if ctx['href'].startswith('note') and hasattr(t, 'date'):
            note_info=dict(
                title = None,
                date = dateutil.parser.parse(t.date),
                is_note=True,
                content = t.body_html,
                description=t.description.strip(),
                description_is_full = t.remainder.strip()=="",
                href = ctx['href'],
                fullhref = ctx['fullhref']
                )
            self.notes.append(note_info)



    def before_execute(self):
        articles = sort_pages(self.articles)
        notes = sort_pages(self.notes)
        full_archive = sort_pages(self.notes + self.articles)
        blog_chains = {}

        # sort blog chains alphabetically
        for k in sorted(self.blog_chains):
            blog_chains[k] = sort_pages(self.blog_chains[k])

        return dict(articles=articles, notes=notes, blog_chains=blog_chains, full_archive=full_archive)


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

# TODO Simplify this!!!!
def note_jinja(jinja_file):
    class NoteJinja(jssg.ExecutionRule):
        # TODO Obviously, simplify this......
        def __call__(self, fs, inf, outf):
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

            t, render_context = jinja_file.pre_render(note_jinja_template.format(dstring,  desc, remainder), add_ctx)
            tmod = t.make_module(render_context)
            layout = jinja_file.env.get_template(tmod.content_layout)
            def update_context(state):
                ctx = render_context.copy()
                assert 'user_context' not in ctx
                ctx['user_context'] = state
                return ctx

            def finish_render(state):
                ctx = update_context(state)
                ctx['data_template'] = tmod
                s = layout.render(ctx)
                fs.write(outf, s)

            # TODO Simplify all this stuff omg
            execution = lambda state: finish_render(state)
            state = dict(type="jinja_template", context=render_context.copy(), template=tmod)
            return execution, state

    return NoteJinja()

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
    ctx = {"production_mode": True}
    base_url = 'https://jpeoples.github.io/'
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        ctx['production_mode'] = False
        base_url = 'http://localhost:8080/'
        print(base_url)

    env = jssg.Environment.default("src", "build")
    env.build_env.add_listener('post_collections', PostCollections())
    env.jinja_filters.update({
            'format_datetime': format_dt,
            'ensure_fullhref': ensure_fullhref
        })

    md_extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite',
        'markdown.extensions.smarty',
        'mdx_math'
    ]
    md_extension_configs = {
            'markdown.extensions.codehilite': {'guess_lang': False},
            'markdown.extensions.toc': {
                "permalink": True,
                "baselevel": 2
                },
            'mdx_math': {'enable_dollar_delimiter': True}
    }

    mdfilter = markdown_filter(extensions=md_extensions, extension_configs=md_extension_configs)
    env.jinja_filters['markdown'] = mdfilter

    jinja_file = env.jinja.add_render_context(
            {"css": "site.css", "base_url": base_url}).add_immediate_context(
                    lambda cx, inf, outf, s: compute_href(cx, "build", inf, outf, s)
                    ).add_render_context(ctx)

    jinja_blog = jinja_file

    note_map = note_jinja(jinja_file)

    env.build((
        # Ignore
        (('*.swp', "*.draft.*"), None),
        # Index pages and rss
        (("*index.jinja.*", "*rss.jinja.xml"), (jssg.remove_internal_extensions, jinja_file.as_layout)),
        # Blog posts
        (("blog/*.html", "blog/*.md"), (nice_url, jinja_file)),
        # Notes
        (("notes/*",), (nice_url, note_map)),
        # Any other pages
        (("*.jinja.*", ), (nice_url, jinja_file.as_layout)),
        # All other files get copied
        ("*", env.mirror_file)
        ))
