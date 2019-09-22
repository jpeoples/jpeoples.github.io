import sys

#import jssg
import jssg
import pathlib

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
            'parse_date': jssg.jinja_utils.parse_date
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

    blog_entries = sort_pages(blog_entries)
    jinja_file = jinja_file.add_render_context({'posts': blog_entries})

    env.build((
        # now process the blog index and rss
        (('blog/index.jinja.html', 'blog/rss.jinja.xml'), (jssg.remove_internal_extensions, jinja_file.full_render)),
        # but ignore the rest of the blog files
        (('blog/*', '*.swp'), None),
        # and build any other jinja pages
        ('*.jinja.md', (jssg.replace_extensions('.html'), jinja_file.full_render)),
        ('*.jinja.*', (jssg.remove_internal_extensions, jinja_file.full_render)),
        # and copy any _other_ files
        ('*', (jssg.mirror_path, jssg.copy_file))
        ), jssg.list_all_files('src'))
