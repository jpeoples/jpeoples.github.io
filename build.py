import sys

import jssg

def compute_href(env, render_context, inpath, outpath, rel_name="href", full_name="fullhref"):
    href = outpath.relative_to(env['output_directory']).as_posix()
    additional_ctx = {
        'href': href,
        'fullhref': render_context['base_url'] + href
    }
    return additional_ctx

def add_push_to_collection(env, render_context, inpath, outpath, page_collection):
    additional_info = {
        "href": render_context['href'],
        'fullhref': render_context['fullhref']
    }
    additional_ctx = {
        'push_to_collection': lambda x: jssg.push_page(page_collection, x, additional_info)
    }

    return additional_ctx

if __name__ == "__main__":
    # set base url
    base_url = 'https://jpeoples.github.io/'
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        base_url = 'http://localhost:8080/'
        print(base_url)

    conf = dict(
        input_directory="src",
        output_directory="build",
        jinja=dict(
            load_paths_with_prefix=(('layouts', 'layouts'),),
            base_render_context=dict(
                css="site.css",
                base_url=base_url
            ),
            jit_context=[compute_href]
        ),
        markdown_filter={},
        date_filters={}
    )

    env = jssg.Environment(conf)

    posts=[]
    jinja_file = env.file.jinja.add_jit_context(add_push_to_collection, page_collection=posts)

    env.build_dir([
        (('*.draft.*', '*index.jinja.*', '*.xml', '*.swp'), env.rule.ignore),
        # process posts
        (('*.jinja.md', '*.jinja.html'), (env.path.to_html, jinja_file)),
        # copy everything else
        ('*', env.rule.copy)
        ], subdir='blog')

    posts = jssg.sort_pages(posts)
    jinja_file = env.file.jinja.add_context({'posts': posts})
    env.build_dir([
        (('blog/index.jinja.html', 'blog/rss.jinja.xml'), (env.path.remove_internal_extensions, jinja_file)),
        (('blog/*', '*.swp'), env.rule.ignore),
        ('*.jinja.md', (env.path.to_html, jinja_file)),
        ('*.jinja.*', (env.path.remove_internal_extensions, jinja_file)),
        ('*', (env.rule.copy))
        ])
