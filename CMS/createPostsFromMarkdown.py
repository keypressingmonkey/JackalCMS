import os
import re
from PIL import Image
import PIL
from resizeimage import resizeimage
import pprint
from datetime import datetime as dt
import random
import shutil
from shutil import copyfile

def replace_config_data(template):
    config_values = load_values_from_config()
    
    for config_value in config_values:
        if config_value[0] == 'header_nav_bar_links':
            navlinks = ''
            for header_nav_bar_link in config_value[1].split(','):            
                navlinks += header_nav_bar_link
            template = template.replace('header_nav_bar_links',navlinks)
        else:
            template = template.replace(config_value[0], config_value[1])
    
    return template

def copy_theme_files():
    config_values = load_values_from_config()
    for config_value in config_values:
        global themefolder 
        if config_value[0] == 'themefolder':
            themefolder = config_value[1]

    themefolder = os.path.join(os.getcwd(),themefolder)
    deploy_folder = os.path.join(os.getcwd(),'site')
    if os.path.exists(deploy_folder):
        shutil.rmtree(deploy_folder, ignore_errors=True)

    for src_dir, dirs, files in os.walk(themefolder):
        dst_dir = src_dir.replace(themefolder, deploy_folder, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy (src_file, dst_dir)

def generate_recent_posts_widget(blogroll):
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates/recent_posts_sidebar.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates/recent_posts_sidebar.html'),'r') as template_file:
            recent_posts_template = template_file.read()
            all_posts = ''
            for post in blogroll:
                temp = recent_posts_template
                temp = temp.replace('recent_post_url', post[0])
                temp = temp.replace('recent_post_title', post[1])
                temp = temp.replace('recent_post_image', post[3])
                all_posts += temp
            return all_posts
    else:
        return ''

def generate_sidebar_widget(blogroll):    
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates/sidebar.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates/sidebar.html'),'r') as template_file:
            sidebar_widget_template = template_file.read()
            return sidebar_widget_template.replace('sidebar_recent_post_component',generate_recent_posts_widget(blogroll))


def generate_related_posts_widget(related_posts):
    with open(os.path.join(os.getcwd(), themefolder,'templates/related_posts.html'),'r') as template_file:
        post_template = template_file.read()
        all_posts = ''
        for post in related_posts:
            temp = post_template
            temp = temp.replace('blog_post_related_post_url', post[0])
            temp = temp.replace('blog_post_related_post_title', post[1])
            temp = temp.replace('blog_post_related_post_subtitle', post[2])
            temp = temp.replace('blog_post_related_post_image', post[3])
            all_posts += temp
        return all_posts

def generate_post_from_Markdown(post_text):
    frontmatter = re.match(r'(---)((.|\n)*?)(---)', post_text).group(2)
    content = re.sub(r'(---)((.|\n)*?)(---)', '', post_text).lstrip('\n')
    teaser = re.match(r'((.|\n)*?)#', content).group(1).lstrip('\n')
    title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter, re.MULTILINE).group(2)
    subtitle = re.search(r'(\nsubtitle: ")(.*?)(")', frontmatter, re.MULTILINE).group(2)
    image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
    date = re.search(r'(\ndate: ")(.*?)(")',frontmatter, re.MULTILINE).group(2)
    return [title.replace(' ', '_')+'.html', title, subtitle, image, date,content,teaser]

def get_frontmatter_values(frontmatter:str):
    frontmattervalues = []
    for frontmattervalue in frontmatter.strip().split('\n'):
        name = re.match(r'(.*?):.*?"(.*?)"',frontmattervalue).group(1)
        value = re.match(r'(.*?):.*?"(.*?)"',frontmattervalue).group(2)
        frontmattervalues.append({name:value})
    return frontmattervalues

def load_values_from_config(): 
    with open(os.path.join(os.getcwd(), 'cms/siteConfig.md')) as config:
        config_values = []
        for line in config.readlines():
            if(re.match(r'(.*?):(.*?)',line)):
                name = re.match(r'(.*?):(.*?)',line).group(1)
                value = re.match(r'(.*?):.*?"(.*?)"($|\n)',line).group(2)
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
                    post_text = f.read() 
                    post = generate_post_from_Markdown(post_text)
                    date = dt.strptime(post[4], "%Y-%m-%d")
                    master_post_date = dt.strptime(current_post_date, "%Y-%m-%d")
                    if date < master_post_date:
                        all_previous_posts.append(post)
        break
    if all_previous_posts:
        # this sorts by date and returns the highest, aka the previous post
        return max(sorted(all_previous_posts, key=lambda tup: tup[4]))
    else:
        return(['/', 'Homepage', '', 'default.jpg', ''])


def get_next_post():
    all_next_posts = []

    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root, file)) as f:
                    post_text = f.read()  # this way we get to separate frontmatter from post content
                    post = generate_post_from_Markdown(post_text)
                    date = dt.strptime(post[4], "%Y-%m-%d")
                    master_post_date = dt.strptime(current_post_date, "%Y-%m-%d")
                    if date > master_post_date:
                        all_next_posts.append(post)
        break
    if all_next_posts:
        # this sorts by date and returns the lowest with a higher date than the mainw, aka the next post
        return min(sorted(all_next_posts, key=lambda tup: tup[4]))
    else:
        return(['/', 'Homepage', '', 'default.jpg', ''])


def get_blogroll_posts():    
    all_posts = []
    
    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root, file)) as f:
                    post_text = f.read()  # this way we get to separate frontmatter from post content
                    post = generate_post_from_Markdown(post_text)                    
                    all_posts.append(post)
        break
    sorted_list = sorted(all_posts, key=lambda tup: tup[4])
    # here we sort by date and skip the highest to start the blogroll with the first nonfeatured post
    return sorted_list

def generate_blogroll_widget():
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates/blogroll_post.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates/blogroll_post.html'),'r') as template_file:
            recent_posts_template = template_file.read()
            all_posts = ''
            blogroll_without_featured = sorted(get_blogroll_posts(),key=lambda x: x[4])[0:len(blogroll)-1]
            for post in sorted(blogroll_without_featured,key=lambda x: x[4],reverse=True):
                post_template = recent_posts_template.replace('blog_loop_post_url',post[0]).replace('blog_loop_post_title',post[1]).replace('blog_loop_post_subtitle',post[2]).replace('blog_loop_post_image',post[3]).replace('blog_loop_post_teaser_text',convert_markdown_to_html(post[6][0:int(frontpage_teaser_length)]+'......'))
                all_posts += post_template
            
            return all_posts
    else:
        return ''
    
    get_blogroll_posts


def get_related_posts(current_post_title):    
    all_posts = []

    for root,dirs,files in os.walk(os.path.join(os.getcwd(),'cms','posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root, file)) as f:
                    post_text = f.read()  # this way we get to separate frontmatter from post content
                    post = generate_post_from_Markdown(post_text)                    
                    if not post[1] == current_post_title:
                        all_posts.append(post)
        break
    return random.sample(all_posts,3)

#main

copy_theme_files()



for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'cms','posts')):
    for file in files:
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root, file)) as template:
                post_text = template.read()  # this way we get to separate frontmatter from post content
                post = generate_post_from_Markdown(post_text)       
                current_post_title = post[0]
                current_post_subtitle = post[1]
                current_post_image = post[3]
                current_post_date = post[4]
                current_post_content = post[5]
                
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

                with open(os.path.join(os.path.join(os.getcwd(), themefolder,'templates','post-sidebar.html')), 'r') as template_file:
                    related_posts = get_related_posts(current_post_title)                
                    template = template_file.read()
                    template = template.replace('post_title', current_post_title)
                    template = template.replace('post_subtitle', current_post_subtitle)
                    
                    template = template.replace('previous_post_url', previous_post_url)
                    template = template.replace('next_post_url', next_post_url)
                    template = template.replace('post_content', current_post_content)
                    related_posts_widget = generate_related_posts_widget(get_related_posts(current_post_title))
                    template = template.replace('related_posts_widget',related_posts_widget)
                    blogroll = get_blogroll_posts()
                    blogroll = sorted(blogroll,key=lambda x: x[4],reverse = True)
                    template = template.replace('sidebar_component', generate_sidebar_widget(blogroll))
                    template = replace_config_data(template)

                    newPostFileName = current_post_title.replace('.md', '.html').replace('.markdown', '.html').replace(' ', '_')
                    with open(os.path.join(os.getcwd(), 'site', newPostFileName), 'w') as newpost:
                        newpost.write(template)
                        newpost.close
                        template_file.close                        
    break
#todo fill index.html with posts
with open(os.path.join(os.getcwd(), themefolder,'templates/index.html'),'r') as template_file:
    template = template_file.read()
    with open(os.path.join(os.getcwd(), 'cms/siteConfig.md')) as config:
        config = config.readlines()       
        frontpage_teaser_length = list(filter(lambda line: line.startswith('frontpage_teaser_length'),config))[0].replace('frontpage_teaser_length: "','').replace('"','').replace('\n','')
        frontpage_featured_teaser_length = list(filter(lambda line: line.startswith('frontpage_featured_teaser_length'),config))[0].replace('frontpage_featured_teaser_length: "','').replace('"','').replace('\n','')
       
        blogroll = get_blogroll_posts()
        blogroll = sorted(blogroll,key=lambda x: x[4],reverse = True)

        template = template.replace('sidebar_component', generate_sidebar_widget(blogroll))
        
        
        template = template.replace('featured_post_url', blogroll[0][0])
        template = template.replace('featured_post_title', blogroll[0][1])
        template = template.replace('featured_post_subtitle', blogroll[0][2])
        template = template.replace('featured_post_image',blogroll[0][3])
        template = template.replace('featured_post_teaser_text',blogroll[0][5][:int(frontpage_featured_teaser_length)])

        template = template.replace('blog_roll',generate_blogroll_widget())
        template = replace_config_data(template)
        with open(os.path.join(os.getcwd(), 'site','index.html'), 'w') as indexPage:
            indexPage.write(template.replace('.md','.html').replace('.markdown','.html'))
            indexPage.close
            template_file.close

optimize_images()