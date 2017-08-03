import sys
import os, os.path
import shutil
import functools
from fnmatch import fnmatchcase
from dateutil.parser import parse as parse_date

import jinja2
import markdown

def forward_sep(path):
    return path.replace("\\", "/")

def url_join(*args):
    return "/".join(args)

def build_all(input_directory, output_directory, build_rules):
    """Build input_directory into output_directory.

    build_rules is a sequence of rules of the form
        [(pattern, rule), (pattern, rule), ...]
    where pattern is a pattern matching string (Unix style) and rule is
    a function to be applied to that file.

    rules should have the signature
        rule(input_directory, output_directory, rel_dir, filename)
    where rel_dir is the path to the directory of the file, relative to
    input_directory, and filename is the name of the file within that
    directory.
    """

    for directory_path, directories, file_names in os.walk(input_directory):
        # strip off the input_directory to get just the rel path.
        directory_path = os.path.relpath(directory_path, input_directory)

        for fn in file_names:
            rel_file_path = os.path.join(directory_path, fn)
            for pattern, rule in build_rules:
                # find the first matching build rule and apply it.
                if fnmatchcase(rel_file_path, pattern):
                    rule(input_directory, output_directory,
                         directory_path, fn)
                    break

def ensure_directory(pathname):
    """Ensure directory specified by pathname exists, file or directory."""
    path = os.path.split(pathname)[0] # get directory
    print(path)
    # create it if it does not exist.
    if os.path.isdir(path): return
    os.makedirs(path)

def copy_file(indir, outdir, reldir, fname):
    inpath = os.path.join(indir, reldir, fname)
    outpath = os.path.join(outdir, reldir, fname)
    ensure_directory(outpath)
    shutil.copy(inpath, outpath)

def ignore_file(indir, outdir, reldir, fname):
    pass

def jinja_md(indir, outdir, reldir, fname):
    inpath = os.path.join(indir, reldir, fname)
    parts = fname.split('.')
    parts.remove('jinja')
    parts.remove('md')
    parts.append('html')
    ofname = '.'.join(parts)
    outpath = os.path.join(outdir, reldir, ofname)
    ensure_directory(outpath)
    jinja_build(inpath, outpath)

def jinja_file(indir, outdir, reldir, fname):
    inpath = os.path.join(indir, reldir, fname)
    parts = fname.split('.')
    parts.remove('jinja')
    ofname = '.'.join(parts)
    outpath = os.path.join(outdir, reldir, ofname)
    ensure_directory(outpath)
    jinja_build(inpath, outpath)


def jinja_build(inpath, outpath):
    href = forward_sep(os.path.relpath(outpath, build_dir))
    jpath = forward_sep(os.path.relpath(inpath, source_dir))

    template = jinja_env.get_template(jpath)
    renderdict = jinja_render_env.copy()
    renderdict['href'] = href
    renderdict['fullhref'] = base_url + href
    renderdict['post_push'] = post_push;
    odata = template.render(renderdict)

    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(odata)

def rss_date(datestr):
    thedate = parse_date(datestr)
    return thedate.strftime("%a, %d %b %Y %H:%M:%S %z") + "EST"

def sort_posts(posts):
    posts.sort(key=lambda x: x['dateobj'], reverse=True)

def group_posts_by_month(posts):
    months = []
    mposts = []
    for post in posts:
        post_month = post['dateobj'].strftime('%B, %Y')
        if post_month not in months:
            months.append(post_month)
            mposts.append({'month': post_month, 'posts': []})

        mposts[-1]['posts'].append(post)
    return mposts



def post_push(title, datestr, content, href):
    post = {
            'fullhref': base_url + href,
            'href': '/' + href,
            'date': rss_date(datestr),
            'dateobj': parse_date(datestr),
            'content': content,
            'title': title
            }
    #print(post)
    posts.append(post)

build_rules = [
        ('*.swp', ignore_file),
        ('layouts*', ignore_file),
        ('*.jinja.md', jinja_md),
        ('*.jinja.*', jinja_file),
        #('*conf.yaml', ignore_file,
        ('*.draft.*', ignore_file),
        ('index.jinja.html', ignore_file),
        ('rss.jinja.xml', ignore_file),
        ('*', copy_file)
        ]

source_dir = "src"
build_dir = "build"
base_url = 'https://jacobpeoples.com/blog/'

if len(sys.argv) > 1 and sys.argv[1] == 'local':
    base_url = 'localhost:8000'

mdextensions = [
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        'markdown.extensions.toc',
        'markdown.extensions.headerid',
        'markdown.extensions.codehilite',
        'mdx_math'
        ]
mdextconf = {"mdx_math": {'enable_dollar_delimiter': True}}
def mdfilter(x):
    s = markdown.markdown(x, extensions=mdextensions, extension_configs=mdextconf)
    return s


#mdfilter = lambda x: markdown.markdown(x, extensions=mdextensions, extension_configs=mdextconf)

loader = jinja2.FileSystemLoader(source_dir)
jinja_env = jinja2.Environment(loader=loader)
jinja_env.filters.update({"markdown": mdfilter})
#jinja_env.globals.update(post_push = post_push)
jinja_render_env = {
        'css': "/site.css",
        'base_url': base_url
        }
posts = []
build_all(source_dir, build_dir, build_rules)
sort_posts(posts)
months = group_posts_by_month(posts)

jinja_render_env['months'] = months
jinja_file(source_dir, build_dir, '', 'index.jinja.html')
