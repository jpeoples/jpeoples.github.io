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

    rule_env = jssg.RuleEnv(source_dir, build_dir)
    jenv = jssg.jinja_env(load_paths_with_prefix=(('layouts','layouts'),))

    # additional template render context
    render_env = {
            'css': "site.css",
            'base_url': base_url
            }

    jinja_file_t = jssg.JinjaFile(jenv, base_url, build_dir, render_ctx=render_env)

    # Build the blog, storing the posts in a PageCollection
    posts = jssg.PageCollection()
    jinja_file = jinja_file_t.override(page_collection=posts)
    rule_env.build_dir([
        # ignore drafts and index pages
        (('*.draft.*', '*index.jinja.*', '*.xml', '*.swp'), jssg.ignore_file),
        # process posts
        (('*.jinja.md', '*.jinja.html'), (jssg.to_html, jinja_file)),
        # copy everything else
        ('*', (jssg.mirror, jssg.copy_file))
        ], subdir='blog')

    # Build the rest of the site, including the rss and index for the
    # blog (which rely on posts)
    jinja_file = jinja_file_t.override(additional_ctx={'posts': posts})
    rule_env.build_dir([
        (('blog/index.jinja.html', 'blog/rss.jinja.xml'), (jssg.remove_internal_extensions, jinja_file)),
        (('blog/*', '*.swp'), jssg.ignore_file),
        ('*.jinja.md', (jssg.to_html, jinja_file)),
        ('*.jinja.*', (jssg.remove_internal_extensions, jinja_file)),
        ('*', (jssg.mirror, jssg.copy_file))
        ])

