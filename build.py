import sys

import pathlib

import jssg
import jinja2
import dateutil.parser

def compute_href(render_context, inpath, outpath, rel_name="href", full_name="fullhref"):
    href = outpath
    if outpath.endswith("index.html"):
        href = pathlib.Path(outpath).parent.as_posix() + "/"
    #href = pathlib.Path(outpath).relative_to(build_dir).as_posix() + "/"
    additional_ctx = {
        rel_name: href,
        full_name: render_context['base_url'] + href
    }
    return additional_ctx

def sort_pages(pages, key='date'):
    return sorted(pages, key=lambda x: x[key], reverse=True)


class PostCollections:
    def __init__(self):
        self.articles = []
        self.notes = []
        self.blog_chains = {}

    def on_data_return(self, inf, outf, data):
        # For now, we only work with jinja_template
        tp = data['type']
        if tp == 'blog_post' or tp == 'note':
            ctx = data['context']
            t = ctx.get('data_template')
            if t is None: return
        else:
            return



        if tp=='blog_post':
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
        if tp=='note':
            note_info=dict(
                title = None,
                date = t['date'],
                is_note=True,
                content = t['body_html'],
                description=t['description'].strip(),
                description_is_full = t['remainder'].strip()=="",
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



def note_load_file(jf, fs, inf, outf, ctx):
    s = fs.read(inf)

    items = s.split('%%%')
    n = len(items)
    if n > 1:
        dstring = items[1]
    if n > 2:
        desc = items[2]
        remainder = ''
    if n > 3:
        remainder = items[3]

    # interpolate context values with jinja !
    mdf = lambda s: jf.render_markdown_string(s, ctx)

    tmod = dict(
        date = dateutil.parser.parse(dstring),
        description = mdf(desc),
        remainder = mdf(remainder),
    )
    tmod['body_html'] = "\n".join((tmod['description'], tmod['remainder']))


    layout = jf.env.get_template("layouts/_note.html")
    ctx['data_template'] = tmod
    state = dict(type="jinja_template_file", context=ctx)
    return layout

def post_load_file(jf, fs, inf, outf, ctx):
    s = fs.read(inf)
    t = jf.env.from_string(s)
    tmod = t.make_module(ctx)
    layout = jf.env.get_template(tmod.content_layout)
    ctx['data_template'] = tmod
    return layout


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
    production_mode = True
    base_url = 'https://jpeoples.github.io/'
    build_dir="build"
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        production_mode = False
        base_url = 'http://localhost:8080/'
        build_dir = "build_local"
        print(base_url)

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


    jenv = jssg.jinja_env(search_paths=(".",), support_rss=True,
            filters=dict(
                markdown=jssg.markdown_filter(extensions=md_extensions, extension_configs=md_extension_configs),
                format_date=jssg.date_formatter("%B %d, %Y"),
                format_datetime=jssg.date_formatter('%B %d, %Y, %H:%M'),
                ensure_fullhref=ensure_fullhref
                ))

    jinja_file = jssg.JinjaFile(jenv, {"css": "site.css", "base_url": base_url, "production_mode": production_mode}, hooks=[compute_href])
    blog_map = jinja_file.renderer(name="blog_post", load_file=post_load_file)
    note_map = jinja_file.renderer(name="note", load_file=note_load_file)
    layout = jinja_file

    listeners = dict(post_collections=PostCollections())
    jssg.build("src", build_dir, (
        (('*.swp', "*.draft.*"), None),
        # Index pages and rss
        (("*index.jinja.*", "*rss.jinja.xml"), (jssg.remove_internal_extensions, layout)),
        # Blog posts
        (("blog/*.html", "blog/*.md"), (jssg.nice_url, blog_map)),
        # Notes
        (("notes/*",), (jssg.nice_url, note_map)),
        # Any other pages
        (("*.jinja.*", ), (jssg.nice_url, layout)),
        # All other files get copied
        ("*", jssg.mirror_file)),
        listeners=listeners)
