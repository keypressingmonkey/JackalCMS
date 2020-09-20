import os
import re
import pprint
from datetime import datetime as dt

current_post_title = ''
current_post_subtitle = ''
current_post_image = ''
current_post_date = ''
current_post_content = ''

website_title = ''
website_subtitle = ''
author_name = ''
author_bio = ''
author_image_name = ''
instagram_profile_url = ''
sidebar_banner_ad_code = ''

blogroll = []


def get_previous_post():
    previous_post_url = ''
    previous_post_title = ''
    previous_post_subtitle = ''
    previous_post_image = ''
    all_previous_posts = []

    for file in os.listdir(os.path.join(os.getcwd(), 'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root, file)) as f:
                post_text = f.read()  # this way we get to separate frontmatter from post content
                frontmatter = re.match(
                    r'(---)((.|\n)*?)(---)', post_text).group(2)
                title = re.search(r'(\ntitle: ")(.*?)(")',
                                  frontmatter, re.MULTILINE).group(2)
                subtitle = re.search(
                    r'(\nsubtitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',
                                  frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',
                                 frontmatter, re.MULTILINE).group(2)
                date = dt.strptime(date, "%Y-%m-%d")
                master_post_date = dt.strptime(current_post_date, "%Y-%m-%d")
                if date < master_post_date:
                    all_previous_posts.append(
                        ['posts/'+title.replace(' ', '_')+'.html', title, subtitle, image, date])
    if all_previous_posts:
        # this sorts by date and returns the highest, aka the previous post
        return max(sorted(all_previous_posts, key=lambda tup: tup[4]))
    else:
        return(['/', 'Homepage', '', 'default.jpg', ''])


def get_next_post():
    next_post_url = ''
    next_post_title = ''
    next_post_subtitle = ''
    next_post_image = ''
    all_next_posts = []

    for file in os.listdir(os.path.join(os.getcwd(), 'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root, file)) as f:
                post_text = f.read()  # this way we get to separate frontmatter from post content
                frontmatter = re.match(
                    r'(---)((.|\n)*?)(---)', post_text).group(2)
                title = re.search(r'(\ntitle: ")(.*?)(")',
                                  frontmatter, re.MULTILINE).group(2)
                subtitle = re.search(
                    r'(\nsubtitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',
                                  frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',
                                 frontmatter, re.MULTILINE).group(2)
                date = dt.strptime(date, "%Y-%m-%d")
                master_post_date = dt.strptime(current_post_date, "%Y-%m-%d")
                if date > master_post_date:
                    all_next_posts.append(['posts/'+title.replace(' ', '_')+'.html', title, subtitle, image, date])
    if all_next_posts:
        # this sorts by date and returns the lowest with a higher date than the mainw, aka the next post
        return min(sorted(all_next_posts, key=lambda tup: tup[4]))
    else:
        return(['/', 'Homepage', '', 'default.jpg', ''])


def get_blogroll_posts():
    next_post_url = ''
    next_post_title = ''
    next_post_subtitle = ''
    next_post_image = ''
    all_posts = []

    for file in os.listdir(os.path.join(os.getcwd(), 'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root, file)) as f:
                post_text = f.read()  # this way we get to separate frontmatter from post content
                frontmatter = re.match(
                    r'(---)((.|\n)*?)(---)', post_text).group(2)
                content = re.sub(
                    r'(---)((.|\n)*?)(---)', '', post_text).lstrip('\n')
                title = re.search(r'(\ntitle: ")(.*?)(")',
                                  frontmatter, re.MULTILINE).group(2)
                subtitle = re.search(
                    r'(\nsubtitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',
                                  frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',
                                 frontmatter, re.MULTILINE).group(2)
                date = dt.strptime(date, "%Y-%m-%d")
                all_posts.append(['posts/'+title.replace(' ', '_')+'.html', title, subtitle, image, date,content])

    sorted_list = sorted(all_posts, key=lambda tup: tup[4])
    # here we sort by date and skip the highest to start the blogroll with the first nonfeatured post
    return sorted_list

#main
    
for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'cms/posts')):
    for file in files:
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root, file)) as template:
                post_text = template.read()  # this way we get to separate frontmatter from post content
                frontmatter = re.match(
                    r'(---)((.|\n)*?)(---)', post_text).group(2)
                current_post_content = re.sub(
                    r'(---)((.|\n)*?)(---)', '', post_text).lstrip('\n')
                current_post_title = re.search(
                    r'(\ntitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                current_post_subtitle = re.search(
                    r'(\nsubtitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                current_post_image = re.search(
                    r'(\nimage: ")(.*?)(")', frontmatter).group(2)
                current_post_date = re.search(
                    r'(\ndate: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                # todo order is important here, better fix this
                current_post_content = re.sub(
                    r'(### )(.*?)($|\n)', r'<h4>\2</h4>\n', current_post_content)
                current_post_content = re.sub(
                    r'(## )(.*?)($|\n)', r'<h3>\2</h3>\n', current_post_content)
                current_post_content = re.sub(
                    r'(# )(.*?)($|\n)', r'<h2>\2</h2>\n', current_post_content)
                current_post_content = re.sub(
                    r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" />', current_post_content)
                current_post_content = re.sub(
                    r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', current_post_content)
                current_post_content = re.sub(
                    r'(\n)(.*?)($|\n)', r'\n<p>\2</p>\n', current_post_content)
                previous_post = get_previous_post()
                previous_post_url = previous_post[0]
                previous_post_title = previous_post[1]
                previous_post_subtitle = previous_post[2]
                previous_post_image = previous_post[3]
                previous_post_date = previous_post[4]
                next_post = get_next_post()
                next_post_url = next_post[0]
                next_post_title = next_post[1]
                next_post_subtitle = next_post[2]
                next_post_image = next_post[3]
                next_post_date = next_post[4]

                with open(os.path.join(os.path.join(os.getcwd(), 'posts/post.html')), 'r') as template:
                    template = template.read()
                    template = template.replace(
                        'post_title', current_post_title)
                    template = template.replace(
                        'post_subtitle', current_post_subtitle)
                    template = template.replace(
                        'site_name', 'site_name')  # todo pull from config
                    template = template.replace(
                        'previous_post_url', previous_post_url)
                    template = template.replace('next_post_url', next_post_url)
                    template = template.replace(
                        'post_content', current_post_content)

                    newPostFileName = current_post_title.replace(
                        '.md', '.html').replace('.markdown', '.html').replace(' ', '_')
                    with open(os.path.join(os.getcwd(), 'posts', newPostFileName+'.html'), 'w') as newpost:
                        newpost.write(template)
                        newpost.close
#todo fill index.html with posts
with open(os.path.join(os.getcwd(), 'cms/index.html'),'r') as template:
    template = template.read()
    with open(os.path.join(os.getcwd(), 'cms/siteConfig.md')) as config:
        config = config.readlines()
        
        website_title = list(filter(lambda line: line.startswith('website_title'),config))[0].replace('website_title: "','').replace('"','').replace('\n','')
        website_subtitle = list(filter(lambda line: line.startswith('website_subtitle'),config))[0].replace('website_subtitle: "','').replace('"','').replace('\n','')
        author_name = list(filter(lambda line: line.startswith('author_name'),config))[0].replace('author_name: "','').replace('"','').replace('\n','')
        author_bio = list(filter(lambda line: line.startswith('author_bio'),config))[0].replace('author_bio: "','').replace('"','').replace('\n','')
        author_image_name = list(filter(lambda line: line.startswith('author_image_name'),config))[0].replace('author_image_name: "','').replace('"','').replace('\n','')
        instagram_profile_url = list(filter(lambda line: line.startswith('instagram_profile_url'),config))[0].replace('instagram_profile_url: "','').replace('"','').replace('\n','')
        sidebar_banner_ad_code = list(filter(lambda line: line.startswith('sidebar_banner_ad_code'),config))[0].replace('sidebar_banner_ad_code: "','').replace('"','').replace('\n','')
        frontpage_teaser_length = list(filter(lambda line: line.startswith('frontpage_teaser_length'),config))[0].replace('frontpage_teaser_length: "','').replace('"','').replace('\n','')
        frontpage_featured_teaser_length = list(filter(lambda line: line.startswith('frontpage_featured_teaser_length'),config))[0].replace('frontpage_featured_teaser_length: "','').replace('"','').replace('\n','')
        blogroll = get_blogroll_posts()
        template = template.replace('sidebar_recent_post_1_url', blogroll[0][0])
        template = template.replace('sidebar_recent_post_1_title', blogroll[0][1])
        template = template.replace('sidebar_recent_post_1_image', blogroll[0][3])
        if len(blogroll)>1:
            template = template.replace('sidebar_recent_post_2_url', blogroll[1][1])
            template = template.replace('sidebar_recent_post_2_title', blogroll[1][1])
            template = template.replace('sidebar_recent_post_2_image', blogroll[1][3])
        if len(blogroll)>2:
            template = template.replace('sidebar_recent_post_3_url', blogroll[2][0])
            template = template.replace('sidebar_recent_post_3_title', blogroll[2][1])
            template = template.replace('sidebar_recent_post_3_image', blogroll[2][3])
        if len(blogroll)>3:
            template = template.replace('sidebar_recent_post_4_url', blogroll[3][0])
            template = template.replace('sidebar_recent_post_4_title', blogroll[3][1])
            template = template.replace('sidebar_recent_post_4_image', blogroll[3][3]) 
        
        template = template.replace('featured_post_1_url', blogroll[len(blogroll)-1][0])
        template = template.replace('featured_post_1_title', blogroll[len(blogroll)-1][1])
        template = template.replace('featured_post_1_subtitle', blogroll[len(blogroll)-1][2])
        template = template.replace('featured_post_1_image',blogroll[len(blogroll)-1][3])
        template = template.replace('featured_post_1_teaser_text',blogroll[len(blogroll)-1][5][:int(frontpage_featured_teaser_length)])

        blogroll_without_featured = sorted(blogroll,key=lambda x: x[4])[0:len(blogroll)-1]
        blogroll_html = ''
        for post in sorted(blogroll_without_featured,key=lambda x: x[4],reverse=True):
            post_template = '''<div class="homepage-post">
                            <figure>
                                <img src="images/blog_loop_post_image" alt="" />
                                <div class="overlay">
                                    <div class="inner">
                                        <div class="figure-text">
                                            <!-- todo the page break here is not automatic, title has a br tag in the middle. Need to figure this out (with css?) -->
                                            <h3><a href="blog_loop_post_url">blog_loop_post_title</a></h3>
                                            <hr class="hidden-xs" />
                                            <h5 class="hidden-xs">blog_loop_post_subtitle</h5>
                                        </div>
                                    </div>
                                </div>
                            </figure>
                            <p>
                                blog_loop_post_teaser_text
                            </p>
                            <div class="readmore">
                                <a href="blog_loop_post_url" class="text">
                                    Read More
                                </a>
                            </div>
                        </div>
'''.replace('blog_loop_post_url',post[0]).replace('blog_loop_post_title',post[1]).replace('blog_loop_post_subtitle',post[2]).replace('blog_loop_post_image',post[3]).replace('blog_loop_post_teaser_text',post[5][0:int(frontpage_teaser_length)])
            blogroll_html += post_template
        template = template.replace('blog_roll', blogroll_html)
        template = template.replace('website_title',website_title)
        template = template.replace('website_subtitle',website_subtitle)
        template = template.replace('author_name',author_name)
        template = template.replace('author_bio',author_bio)
        template = template.replace('author_image_name',author_image_name)
        template = template.replace('instagram_profile_url',instagram_profile_url)
        template = template.replace('sidebar_banner_ad_code',sidebar_banner_ad_code)
        with open(os.path.join(os.getcwd(), 'index.html'), 'w') as indexPage:
            indexPage.write(template.replace('.md','.html').replace('.markdown','.html'))
            indexPage.close