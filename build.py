import sys

import jssg

if __name__ == "__main__":
    # set base url
    base_url = 'https://jpeoples.github.io/'
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        base_url = 'http://localhost:8080/'
        print(base_url)

    source_dir = 'src'
    build_dir = 'build'

    # additional template render context
    render_env = {
            'css': "site.css",
            }

    env = jssg.Environment(source_dir, build_dir, base_url, template_render_data=render_env,
            template_loader_dirs=(('layouts', 'layouts'),))

    # Build the blog, storing the posts in a PageCollection
    posts = jssg.PageCollection()
    env.build_dir([
        # ignore drafts and index pages
        (('*.draft.*', '*index.jinja.*', '*.xml', '*.swp'), jssg.ignore_file),
        # process posts
        (('*.jinja.md', '*.jinja.html'), (jssg.to_html, jssg.jinja_file)),
        # copy everything else
        ('*', (jssg.mirror, jssg.copy_file))
        ], subdir='blog', page_collection=posts)

    # Build the rest of the site, including the rss and index for the
    # blog (which rely on posts)
    env.build_dir([
        (('blog/index.jinja.html', 'blog/rss.jinja.xml'), (jssg.remove_internal_extensions, jssg.jinja_file)),
        (('blog/*', '*.swp'), jssg.ignore_file),
        ('*.jinja.md', (jssg.to_html, jssg.jinja_file)),
        ('*.jinja.*', (jssg.remove_internal_extensions, jssg.jinja_file)),
        ('*', (jssg.mirror, jssg.copy_file))
        ], additional_template_render_data={'posts': posts})

