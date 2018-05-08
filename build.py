import sys
import os
import shutil
from dateutil.parser import parse as parse_date
import pathlib
import bisect

import jinja2
import markdown

    
def ensure_directory(path):
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass

def path_replace_all_suffix(path, suffix):
    while path.suffix:
        path = path.with_suffix('')
    return path.with_suffix(suffix)

def walk_directory(input_directory):
    for directory_path, _, file_names in os.walk(str(input_directory)):
        relative_directory = pathlib.Path(directory_path).relative_to(input_directory)
        for fn in file_names:
            yield relative_directory.joinpath(fn)

class FileMapper:
    def __init__(self, indir, outdir):
        self.indir = pathlib.Path(indir)
        self.outdir = pathlib.Path(outdir)

    def mirror(self, fn):
        return self.indir / fn, self.outdir / fn

    def to_html(self, fn):
        return self.indir / fn, self.outdir / path_replace_all_suffix(fn, '.html')

    def remove_internal_extensions(self, fn):
        return self.indir / fn, self.outdir / path_replace_all_suffix(fn, fn.suffix)

def copy_file(inpath, outpath):
    shutil.copy(str(inpath), str(outpath))

def ignore_file(*args, **kwargs):
    pass

def make_post(title, datestr, content, href):
    post = {
            'fullhref': base_url + href,
            'href': '/' + href,
            'date': rss_date(datestr),
            'dateobj': parse_date(datestr),
            'content': content,
            'title': title
            }
    return post

class PostCollection:
    def __init__(self):
        self.posts = []
        self.keys = []

    def post_push(self, post):
        key = post['dateobj']
        x = bisect.bisect_left(self.keys, key)
        self.keys[x:x] = [key]
        self.posts[x:x] = [post]

    def history(self, count=20):
        for i, post in enumerate(reversed(self.posts)):
            if count is not None and i >= count:
                break
            yield post

    def by_year(self):
        current_year = None
        for post in reversed(self.posts):
            date = post['dateobj']
            if date.year != current_year:
                if current_year is not None:
                    yield obj
                obj = {'year': date.year, 'posts': []}
                current_year = date.year

            obj['posts'].append(post)
        yield obj


def make_jinja_builder(template_load, prepare_dict):
    def build(inpath, outpath):
        template = template_load(inpath)
        rdct = prepare_dict(outpath)

        with outpath.open('w', encoding='utf-8') as f:
            f.write(template.render(rdct))
    return build

def make_template_loader(indir, load):
    def map(inpath):
        return load(str(inpath.relative_to(indir)))
    return map

def make_render_dict(outdir, initial_dict, base_uri, post_collection):
    def map(outpath):
        href = outpath.relative_to(outdir).as_posix()
        renderdict = initial_dict.copy()
        renderdict['href'] = href
        renderdict['fullhref'] = base_uri + href
        renderdict['post_push'] = lambda t, d, c, h: post_collection.post_push(make_post(t,d,c,h))
        return renderdict
    return map

def make_rule(file_map, file_transform):
    def map(fn):
        inpath, outpath = file_map(fn)
        ensure_directory(outpath)
        file_transform(inpath, outpath)
    return map

def build_all(input_directory, output_directory, build_rules):
    for fn in walk_directory(input_directory):
        build_rules(fn)

def format_date(dateobj):
    dateobj = parse_date(dateobj)
    return dateobj.strftime('%B %d, %Y')

def rss_date(dateobj):
    thedate = parse_date(dateobj)
    return thedate.strftime("%a, %d %b %Y %H:%M:%S %z") + "EST"

class BuildRules:
    def __init__(self, rules):
        self.rules = rules

    def match(self, fn):
        # call first matching rule
        for matcher, rule in self.rules:
            if self._single_match(matcher, fn):
                return rule(fn)

    def _single_match(self, matcher, fn):
        try:
            ret = matcher(fn)
        except TypeError:
            # fallback is to match as glob string
            ret = fn.match(matcher)
        return ret


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

def setup_jinja(source_dir, filters):
    loader = jinja2.FileSystemLoader(str(source_dir))
    jinja_env = jinja2.Environment(loader=loader)
    jinja_env.filters.update(filters)
    return jinja_env


if __name__ == "__main__":

    base_url = 'https://jpeoples.github.io/'
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        base_url = 'http://localhost:8080/'
        print(base_url)
    source_dir = pathlib.Path("src")
    build_dir = pathlib.Path("build")
    file_mapper = FileMapper(source_dir, build_dir)
    jinja_env = setup_jinja(source_dir, {'markdown': mdfilter, 'format_date': format_date})
    
    posts = PostCollection()
    jinja_render_env = {
            'css': "site.css",
            'base_url': base_url
            }

    jinja_build = make_jinja_builder(make_template_loader(source_dir, jinja_env.get_template),
                                    make_render_dict(build_dir, jinja_render_env, base_url, posts))

    jinja_md = make_rule(file_mapper.to_html, jinja_build)
    jinja_file = make_rule(file_mapper.remove_internal_extensions, jinja_build)
    simple_copy = make_rule(file_mapper.mirror, copy_file)

    build_rules = BuildRules([
            ('*.swp', ignore_file),
            ('./layouts*', ignore_file),
            ('./index.jinja.html', ignore_file),
            ('./blog/index.jinja.html', ignore_file),
            ('*.draft.*', ignore_file),
            ('./rss.jinja.xml', ignore_file),
            ('*.jinja.md', jinja_md),
            ('*.jinja.*', jinja_file),
            #('*conf.yaml', ignore_file,
            ('*', simple_copy)
           ])


    build_all(source_dir, build_dir, build_rules.match)
    jinja_render_env['posts'] = posts
    jinja_file(pathlib.Path('index.jinja.html'))
    jinja_file(pathlib.Path('blog/index.jinja.html'))