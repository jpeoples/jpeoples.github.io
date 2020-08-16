import sys

import pathlib

import jssg
import jinja2
import dateutil.parser

# TODO Move more logic to build.py from rendering. The different pages
# are now different classes, so we can polymorph their different kinds
# of rendering

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

def sort_pages(pages, key='date', reverse=True):
    return sorted(pages, key=lambda x: x[key], reverse=reverse)


class PostCollections:
    def __init__(self):
        self.articles = []
        self.notes = []
        self.blog_chains = {}
        self.blog_chains_info = {}

    def on_data_return(self, inf, outf, data):
        # For now, we only work with jinja_template
        tp = data['type']
        if tp == 'blog_post' or tp == 'note' or tp =='blog_chain_landing':
            ctx = data['context']
            t = ctx.get('data_template')
            if t is None: return
        else:
            return


        if tp == "blog_chain_landing":
            self.blog_chains_info[t.blog_chain] = t
        if tp=='blog_post':
            article_info = t
            self.articles.append(article_info)
            if hasattr(t, 'blog_chain'):
                chain_name = t.blog_chain
                chain = self.blog_chains.setdefault(chain_name, [])
                chain.append(article_info)
        if tp=='note':
            note_info = t
            self.notes.append(note_info)

    def before_execute(self):
        articles = sort_pages(self.articles)
        notes = sort_pages(self.notes)
        full_archive = sort_pages(self.notes + self.articles)
        blog_chains = {}

        # sort blog chains alphabetically
        for k in sorted(self.blog_chains):
            blog_chain_posts = sort_pages(self.blog_chains[k], reverse=False)
            blog_chain_info = self.blog_chains_info[k]
            blog_chain_info.posts = blog_chain_posts
            blog_chains[k] = blog_chain_info

        return dict(articles=articles, notes=notes, blog_chains=blog_chains, full_archive=full_archive)

format_date=jssg.date_formatter("%B %d, %Y")
format_datetime=jssg.date_formatter('%B %d, %Y, %H:%M')

def wrap(s, tag, additional=None):
    if additional is None:
        additional = []
    op = '<' + ' '.join([tag] + additional) + '>'
    cl = f'</{tag}>'
    return f'{op}{s}{cl}'


def details_page_list(pages, default_open=False):
    def details(s, default_open):
        add = ['open'] if default_open else []
        return wrap(s, 'details', add)

    for page in pages:
        link = page.page_list_item()
        summ = page.read_more_summary()
        yield details(f'<summary>{link}</summary>\n<blockquote>{summ}</blockquote>', default_open)

def render_ul(items, nopad=False, cls='list-no-bullet'):
    if nopad:
        cls += ' pad-none'

    items = [wrap(item, 'li') for item in items]
    inner = "\n".join(items)
    return wrap(inner, 'ul', additional=[f'class="{cls}"'])

class Page:
    def __getitem__(self, name):
        return getattr(self, name)

    def get_meta_description(self):
        try:
            return self.meta_description
        except AttributeError:
            try:
                return self.description
            except AttributeError:
                return "Personal blog of Jacob Peoples"

class Note(Page):
    def __init__(self, date, description, remainder, ctx):
        self.ctx = ctx
        self.href = ctx['href']
        self.fullhref = ctx['fullhref']
        self.date = date
        self.description = description.strip()
        self.description_is_full = remainder.strip() == ""
        self.remainder = remainder

        self.title = None
        self.is_note = True
        self.body_html = "\n".join((description, remainder))
        self.content = self.body_html

    def __getitem__(self, name):
        return getattr(self, name)

    def page_list_item(self):
        date = format_date(self.date)
        time = format_datetime(self.date).split()[3]
        return f'{date}, <a href="{self.fullhref}">{time}</a>'

    def read_more_summary(self):
        blocks = [self.description]
        if not self.description_is_full:
            blocks.append(f'<p><a href="{self.fullhref}">Read More</a></p>')
        return "\n".join(blocks)

class Post(Page):
    def __init__(self, t, ctx):
        self.ctx = ctx
        self.tmod = t
        self.title = t.title
        self.date = dateutil.parser.parse(t.date)
        self.content = t.body_html
        self.description_is_full=False
        self.href = ctx['href']
        self.fullhref = ctx['fullhref']

    def page_list_item(self):
        date = format_date(self.date)
        return f'{date} – <a href="{self.fullhref}">{self.title}</a>'

    def read_more_summary(self):
        blocks = []
        if hasattr(self.tmod, 'description'):
            blocks.append(self.tmod.description)
            blocks.append(f'<p><a href="{self.fullhref}">Read More</a></p>')
        else:
            blocks.append(f'<p><a href="{self.fullhref}">Read Post</a></p>')
        return "\n".join(blocks)


    def __getattr__(self, name):
        return getattr(self.tmod, name)

class Chain(Post):
    def __init__(self, t, ctx):
        self.ctx = ctx
        self.tmod = t
        self.title = t.blog_chain
        self.blog_chain = t.blog_chain
        self.description_is_full=False
        self.href = ctx['href']
        self.fullhref = ctx['fullhref']
        self.content = getattr(t, 'body_html', None)

    def page_list_item(self):
        return f'<a href="{self.fullhref}">{self.title}</a>'

    def read_more_summary(self):
        assert hasattr(self.tmod, 'description')
        return super().read_more_summary()

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

    tmod = Note(
        date = dateutil.parser.parse(dstring),
        description = mdf(desc),
        remainder = mdf(remainder),
        ctx=ctx
    )

    layout = jf.env.get_template("layouts/_note.html")
    ctx['data_template'] = tmod
    # state = dict(type="jinja_template_file", context=ctx)
    return layout

def post_load_file(jf, fs, inf, outf, ctx):
    t = jf.env.get_template(fs.resolve_in(inf))
    tmod = t.make_module(ctx)
    layout = jf.env.get_template(tmod.content_layout)
    ctx['data_template'] = Post(tmod, ctx)
    return layout

def chain_load_file(jf, fs, inf, outf, ctx):
    t = jf.env.get_template(fs.resolve_in(inf))
    tmod = t.make_module(ctx)
    layout = jf.env.get_template(tmod.content_layout)
    ctx['data_template'] = Chain(tmod, ctx)
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
                ensure_fullhref=ensure_fullhref,
                render_ul=render_ul,
                details_page_list=details_page_list
                ))

    jinja_file = jssg.JinjaFile(jenv, {"css": "site.css", "base_url": base_url, "production_mode": production_mode}, hooks=[compute_href])
    blog_map = jinja_file.renderer(name="blog_post", load_file=post_load_file)
    blog_chain_landing = jinja_file.renderer(name="blog_chain_landing", load_file=chain_load_file)
    note_map = jinja_file.renderer(name="note", load_file=note_load_file)
    layout = jinja_file

    listeners = dict(post_collections=PostCollections())
    jssg.build("src", build_dir, (
        (('*.swp', "*.draft.*"), None),
        # Index pages and rss
        (("*index.jinja.*", "*rss.jinja.xml"), (jssg.remove_internal_extensions, layout)),
        # Blog posts
        (("blog/*/*.html", "blog/*/*.md"), (jssg.nice_url, blog_map)),
        (("blog/*.html", "blog/*.md"), (jssg.nice_url, blog_chain_landing)),
        # Notes
        (("notes/*",), (jssg.nice_url, note_map)),
        # Any other pages
        (("*.jinja.*", ), (jssg.nice_url, layout)),
        # All other files get copied
        ("*", jssg.mirror_file)),
        listeners=listeners)
