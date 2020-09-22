import os
import re
from PIL import Image
import PIL
from resizeimage import resizeimage
import pprint
from datetime import datetime as dt
import random
from shutil import copyfile

def load_values_from_config(): 
    with open(os.path.join(os.getcwd(), 'cms/siteConfig.md')) as config:
        config_values = []
        for line in config.readlines():
            if(re.match(r'(.*?):(.*?)',line)):
                name = re.match(r'(.*?):(.*?)',line).group(1)
                value = re.match(r'(.*?):.*?"(.*?)"',line).group(2)
                config_values.append([name, value])
        return config_values
        

def resize_and_optimize(imagefile,imagename:str,subfolder: str,width:int,shall_optimize:bool,optimizationgrade:int):
    img = resizeimage.resize_width(imagefile, width, validate=False)
    path = os.path.join(os.path.dirname(os.path.dirname( __file__ )),'site','images',subfolder,imagename)
    img.save(path,optimize=shall_optimize, quality=optimizationgrade)

def optimize_images():
    for root,dirs,file in os.walk(os.path.join(os.getcwd(),'site','images')):
        for image in file:
            if (image.endswith('.jpg') or image.endswith('.png')):
                original_image = Image.open(os.path.join(root,image))
                test = os.path.join(os.getcwd(),root,'backup',image)
                if not os.path.isfile(os.path.join(os.getcwd(),root,'backup',image)):
                    original_image.save(os.path.join(os.getcwd(),root,'backup',image))
                img = resize_and_optimize(original_image,image,'blogroll',760,True,80)
                img = resize_and_optimize(original_image,image,'featured',760,True,80)
                img = resize_and_optimize(original_image,image,'thumbs',80,True,80)
                img = resize_and_optimize(original_image,image,'related',214,True,80)
                img = resize_and_optimize(original_image,image,'sidebar_large',350,True,80)
                img = resize_and_optimize(original_image,image,'130px',130,True,80)                
        break #this break makes the os.walk non recursive so we don't optimize the optimized (quid opimizos optimizadan)

def convert_markdown_to_html(value):
    result = ''
    for line in value.split('\n'):
        line = re.sub(r'(### )(.*?)($|\n)', r'<h4>\2</h4>\n', line)
        line = re.sub(r'(## )(.*?)($|\n)', r'<h3>\2</h3>\n', line)
        line = re.sub(r'(# )(.*?)($|\n)', r'<h2>\2</h2>\n', line)
        line = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" />', line)
        line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
        # line = re.sub(r'(\n)(.*?)($|\n)', r'\n<p>\2</p>\n', line)
        if not line.startswith('<'):
            line = re.sub(r'(^)(.*?)($|\n)', r'<p>\2</p>\n', line)
        # if not '<' in line:
        #     line = '<p>'+line+ '</p>'
        result += line
    return result
    


def get_previous_post():
    all_previous_posts = []

    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
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
        break
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

    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
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
        break
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

    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root, file)) as f:
                    post_text = f.read()  # this way we get to separate frontmatter from post content
                    frontmatter = re.match(
                        r'(---)((.|\n)*?)(---)', post_text).group(2)
                    content = re.sub(
                        r'(---)((.|\n)*?)(---)', '', post_text).lstrip('\n')
                    teaser = re.match(
                        r'((.|\n)*?)#', content).group(1).lstrip('\n')
                    title = re.search(r'(\ntitle: ")(.*?)(")',
                                    frontmatter, re.MULTILINE).group(2)
                    subtitle = re.search(
                        r'(\nsubtitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
                    image = re.search(r'(\nimage: ")(.*?)(")',
                                    frontmatter).group(2)
                    date = re.search(r'(\ndate: ")(.*?)(")',
                                    frontmatter, re.MULTILINE).group(2)
                    date = dt.strptime(date, "%Y-%m-%d")
                    all_posts.append(['posts/'+title.replace(' ', '_')+'.html', title, subtitle, image, date,content,teaser])
        break
    sorted_list = sorted(all_posts, key=lambda tup: tup[4])
    # here we sort by date and skip the highest to start the blogroll with the first nonfeatured post
    return sorted_list
def get_related_posts(current_post_title):    
    all_posts = []

    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
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
                    if not title == current_post_title:
                        all_posts.append(['posts/'+title.replace(' ', '_')+'.html', title, subtitle, image, date,content])    
        break
    return random.sample(all_posts,3)

#main
    
for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'cms','posts')):
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
                current_post_content = convert_markdown_to_html(current_post_content)
              
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

                #related posts 

                with open(os.path.join(os.path.join(os.getcwd(), 'site','templates','post-sidebar.html')), 'r') as template_file:
                    related_posts = get_related_posts(current_post_title)                
                    template = template_file.read()
                    template = template.replace(
                        'post_title', current_post_title)
                    template = template.replace(
                        'post_subtitle', current_post_subtitle)
                    
                    template = template.replace(
                        'previous_post_url', previous_post_url)
                    template = template.replace('next_post_url', next_post_url)
                    template = template.replace(
                        'post_content', current_post_content)
                    for config_value in load_values_from_config():
                        template = template.replace(config_value[0], config_value[1])
                    template = template.replace('blog_post_related_post_1_url', related_posts[0][0])
                    template = template.replace('blog_post_related_post_1_title', related_posts[0][1])
                    template = template.replace('blog_post_related_post_1_subtitle', related_posts[0][2])
                    template = template.replace('blog_post_related_post_1_image', related_posts[0][3])
                    template = template.replace('blog_post_related_post_2_url', related_posts[1][0])
                    template = template.replace('blog_post_related_post_2_title', related_posts[1][1])
                    template = template.replace('blog_post_related_post_2_subtitle', related_posts[1][2])
                    template = template.replace('blog_post_related_post_2_image', related_posts[1][3])
                    template = template.replace('blog_post_related_post_3_url', related_posts[2][0])
                    template = template.replace('blog_post_related_post_3_title', related_posts[2][1])
                    template = template.replace('blog_post_related_post_3_subtitle', related_posts[2][2])
                    template = template.replace('blog_post_related_post_3_image', related_posts[2][3])
                    newPostFileName = current_post_title.replace(
                        '.md', '.html').replace('.markdown', '.html').replace(' ', '_')
                    with open(os.path.join(os.getcwd(), 'site','posts', newPostFileName+'.html'), 'w') as newpost:
                        newpost.write(template)
                        newpost.close
                        template_file.close                        
    break
#todo fill index.html with posts
with open(os.path.join(os.getcwd(), 'site/templates/index.html'),'r') as template_file:
    template = template_file.read()
    with open(os.path.join(os.getcwd(), 'cms/siteConfig.md')) as config:
        config = config.readlines()
        
        website_title = list(filter(lambda line: line.startswith('website_title'),config))[0].replace('website_title: "','').replace('"','').replace('\n','')
        website_subtitle = list(filter(lambda line: line.startswith('website_subtitle'),config))[0].replace('website_subtitle: "','').replace('"','').replace('\n','')
        author_name = list(filter(lambda line: line.startswith('author_name'),config))[0].replace('author_name: "','').replace('"','').replace('\n','')
        author_bio = list(filter(lambda line: line.startswith('author_bio'),config))[0].replace('author_bio: "','').replace('"','').replace('\n','')
        author_image_name = list(filter(lambda line: line.startswith('author_image_name'),config))[0].replace('author_image_name: "','').replace('"','').replace('\n','')
        website_logo_white = list(filter(lambda line: line.startswith('website_logo_white'),config))[0].replace('website_logo_white: "','').replace('"','').replace('\n','')
        website_logo_dark = list(filter(lambda line: line.startswith('website_logo_dark'),config))[0].replace('website_logo_dark: "','').replace('"','').replace('\n','')
        instagram_profile_url = list(filter(lambda line: line.startswith('instagram_profile_url'),config))[0].replace('instagram_profile_url: "','').replace('"','').replace('\n','')
        sidebar_banner_ad_code = list(filter(lambda line: line.startswith('sidebar_banner_ad_code'),config))[0].replace('sidebar_banner_ad_code: "','').replace('"','').replace('\n','')
        frontpage_teaser_length = list(filter(lambda line: line.startswith('frontpage_teaser_length'),config))[0].replace('frontpage_teaser_length: "','').replace('"','').replace('\n','')
        frontpage_featured_teaser_length = list(filter(lambda line: line.startswith('frontpage_featured_teaser_length'),config))[0].replace('frontpage_featured_teaser_length: "','').replace('"','').replace('\n','')
        header_nav_bar_links = list(filter(lambda line: line.startswith('header_nav_bar_links'),config))[0].replace('header_nav_bar_links: "','').replace('"','').replace('\n','').split(',')
        navlinks = ''
        for header_nav_bar_link in header_nav_bar_links:
            link = header_nav_bar_link.split('(')[0]
            link_name = header_nav_bar_link.split('(')[1].replace(')','')
            navlinks += '<li><a href="'+link +'">'+link_name + '</a></li>'
        template = template.replace('header_nav_bar_links',navlinks)
        blogroll = get_blogroll_posts()
        blogroll = sorted(blogroll,key=lambda x: x[4],reverse = True)
        template = template.replace('sidebar_recent_post_1_url', blogroll[0][0])
        template = template.replace('sidebar_recent_post_1_title', blogroll[0][1]) 
        template = template.replace('sidebar_recent_post_1_image', blogroll[0][3])
        if len(blogroll)>1:
            template = template.replace('sidebar_recent_post_2_url', blogroll[1][0])
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
        
        template = template.replace('featured_post_1_url', blogroll[0][0])
        template = template.replace('featured_post_1_title', blogroll[0][1])
        template = template.replace('featured_post_1_subtitle', blogroll[0][2])
        template = template.replace('featured_post_1_image',blogroll[0][3])
        template = template.replace('featured_post_1_teaser_text',blogroll[0][5][:int(frontpage_featured_teaser_length)])

        blogroll_without_featured = sorted(blogroll,key=lambda x: x[4])[0:len(blogroll)-1]
        blogroll_html = ''
        for post in sorted(blogroll_without_featured,key=lambda x: x[4],reverse=True):
            post_template = '''<div class="homepage-post">
                            <figure>
                                <img src="images/blogroll/blog_loop_post_image" alt="" />
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
                            <p>blog_loop_post_teaser_text</p>
                            <div class="readmore"><a href="blog_loop_post_url" class="text">Read More</a></div>
                            
                        </div>
'''.replace('blog_loop_post_url',post[0]).replace('blog_loop_post_title',post[1]).replace('blog_loop_post_subtitle',post[2]).replace('blog_loop_post_image',post[3]).replace('blog_loop_post_teaser_text',convert_markdown_to_html(post[6][0:int(frontpage_teaser_length)]+'......'))
            blogroll_html += post_template
        template = template.replace('blog_roll', blogroll_html)
        template = template.replace('website_title',website_title)
        template = template.replace('website_subtitle',website_subtitle)
        template = template.replace('sidebar_banner_ad_code',sidebar_banner_ad_code)
        template = template.replace('author_name',author_name)
        template = template.replace('author_bio',author_bio)
        template = template.replace('author_image_name',author_image_name)
        template = template.replace('website_logo_white',website_logo_white)
        template = template.replace('website_logo_dark',website_logo_dark)
        template = template.replace('instagram_profile_url',instagram_profile_url)
        with open(os.path.join(os.getcwd(), 'site','index.html'), 'w') as indexPage:
            indexPage.write(template.replace('.md','.html').replace('.markdown','.html'))
            indexPage.close
            template_file.close

optimize_images()