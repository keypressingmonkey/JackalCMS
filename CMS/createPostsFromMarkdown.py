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
import markdown


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

def get_single_value_from_config(name_of_value:str):
    config_values = load_values_from_config()
    
    for config_value in config_values:
        if config_value[0] == name_of_value:
            return config_value[1]        

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
    
def copy_images_from_cms_to_site():
    cms_images_folder = os.path.join(os.getcwd(),'cms','images')
    deploy_folder = os.path.join(os.getcwd(),'site','images')
    
    for src_dir, dirs, files in os.walk(cms_images_folder):
        dst_dir = src_dir.replace(cms_images_folder, deploy_folder, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy (src_file, dst_dir)

def generate_recent_posts_widget():
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates/recent_posts_sidebar.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates/recent_posts_sidebar.html'),'r') as template_file:
            recent_posts_template = template_file.read()
            all_posts = ''
            blogroll = sort_posts_by_date(get_blogroll_posts())
            blogroll = blogroll[0:int(get_single_value_from_config('number_of_recent_blog_posts_in_sidebar'))]
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
            return sidebar_widget_template.replace('sidebar_recent_post_component',generate_recent_posts_widget())

def generate_related_posts_widget(related_posts):
    with open(os.path.join(os.getcwd(), themefolder,'templates/related_posts.html'),'r') as template_file:
        post_template = template_file.read()
        all_posts = ''
        for post in related_posts:
            temp = post_template
            temp = temp.replace('blog_post_related_post_url', post[0])
            temp = temp.replace('blog_post_related_post_title', post[1])
            temp = temp.replace('blog_post_related_post_s', post[2])
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
    global config_values 
    global themefolder 
    with open(os.path.join(os.getcwd(), 'cms/siteConfig.md')) as config:
        config_values = []
        for line in config.readlines():
            if(re.match(r'(.*?):(.*?)',line)):
                name = re.match(r'(.*?):(.*?)',line).group(1)
                value = re.match(r'(.*?):.*?"(.*?)"($|\n)',line).group(2)
                config_values.append([name, value])
                for config_value in config_values:
                    if config_value[0] == 'themefolder':
                        themefolder = os.path.join(os.getcwd(),config_value[1])

    with open(os.path.join(os.getcwd(), themefolder,'templates','themeConfig.md')) as theme_config:
        for line in theme_config.readlines():
            if(re.match(r'(.*?):(.*?)',line)):
                name = re.match(r'(.*?):(.*?)',line).group(1)
                value = re.match(r'(.*?):.*?"(.*?)"($|\n)',line).group(2)
                config_values.append([name, value])
    return config_values

def resize_and_optimize(imagefile,imagename:str,subfolder: str,width:int,shall_optimize:bool,optimizationgrade:int):
    img = resizeimage.resize_width(imagefile, width, validate=False)
    path = os.path.join(os.path.dirname(os.path.dirname( __file__ )),'site','images',subfolder)
    if not os.path.exists(path):
        os.makedirs(path)
    img.save(os.path.join(path,imagename),optimize=shall_optimize, quality=optimizationgrade)

def optimize_images():
    for root,dirs,file in os.walk(os.path.join(os.getcwd(),'site','images')):
        for image in file:
            if (image.endswith('.jpg') or image.endswith('.png')):
                original_image = Image.open(os.path.join(root,image))
             
                img = resize_and_optimize(original_image,image,'blogroll',760,True,80)
                img = resize_and_optimize(original_image,image,'featured',760,True,80)
                img = resize_and_optimize(original_image,image,'thumbs',80,True,80)
                img = resize_and_optimize(original_image,image,'related',214,True,80)
                img = resize_and_optimize(original_image,image,'sidebar_large',350,True,80)
                img = resize_and_optimize(original_image,image,'130px',130,True,80)                
        break #this break makes the os.walk non recursive so we don't optimize the optimized (quid opimizos optimizadan)

def convert_markdown_to_html(value):
    result = markdown.markdown(value)
    return result

def get_previous_post(current_post_date):
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
        return sort_posts_by_date(all_previous_posts,True)[0]
    else:
        return(['/', 'Homepage', '', 'default.jpg', ''])

def get_next_post(current_post_date):
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
        return sort_posts_by_date(all_next_posts,False)[0]
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
    sorted_list = sort_posts_by_date(all_posts)
    return sorted_list

def generate_blogroll_widget(paginated_posts):
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates/blogroll_post.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates/blogroll_post.html'),'r') as template_file:
            recent_posts_template = template_file.read()
            all_posts = ''
            number_of_featured_posts = int(get_single_value_from_config('number_of_featured_posts'))
            blogroll_without_featured = sort_posts_by_date(paginated_posts)[number_of_featured_posts:len(paginated_posts)]

            for post in sort_posts_by_date(blogroll_without_featured):
                post_template = recent_posts_template.replace('blog_loop_post_url',post[0])
                post_template = post_template.replace('blog_loop_post_title',post[1])
                post_template = post_template.replace('blog_loop_post_subtitle',post[2])
                post_template = post_template.replace('blog_loop_post_image',post[3])
                post_template = post_template.replace('blog_loop_post_date',post[4])
                post_template = post_template.replace('blog_loop_post_teaser_text',convert_markdown_to_html(post[6][0:int(get_single_value_from_config('frontpage_teaser_length'))]+'......'))
                all_posts += post_template
            
            return all_posts
    else:
        return ''

def generate_featured_post_widget(paginated_posts):
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates/post_featured.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates/post_featured.html'),'r') as template_file:
            recent_posts_template = template_file.read()
            all_posts = ''
            number_of_featured_posts = int(get_single_value_from_config('number_of_featured_posts'))
            blogroll_featured = sort_posts_by_date(paginated_posts,False)[len(paginated_posts)-number_of_featured_posts:len(paginated_posts)]

            for post in blogroll_featured:
                post_template = recent_posts_template.replace('featured_post_url',post[0])
                post_template = post_template.replace('featured_post_title',post[1])
                post_template = post_template.replace('featured_post_subtitle',post[2])
                post_template = post_template.replace('featured_post_image',post[3])
                post_template = post_template.replace('featured_post_date',post[4])
                post_template = post_template.replace('featured_post_teaser_text',convert_markdown_to_html(post[6][0:int(get_single_value_from_config('frontpage_featured_teaser_length'))]+'......'))
                all_posts += post_template
            
            return all_posts
    else:
        return ''

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

def split_list_into_chunks(lst, n:int): #stolen from https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_paginated_posts():    
    all_pages = []
    blogroll = sort_posts_by_date(get_blogroll_posts())
    batch_size = int(get_single_value_from_config('number_of_blog_posts_in_blogroll'))
    blogroll_split_into_chunks = list(split_list_into_chunks(blogroll,batch_size))
    for paginated_block in  blogroll_split_into_chunks:
        all_pages.append(sort_posts_by_date(paginated_block))
        
    return sorted(all_pages,key=lambda x: x[0][4],reverse=True)

def generate_post_pages():
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'cms','posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root, file)) as template:
                    post_text = template.read()  # this way we get to separate frontmatter from post content
                    post = generate_post_from_Markdown(post_text)     
                    current_post_url = post[0]
                    current_post_title = post[1]
                    current_post_subtitle = post[2]
                    current_post_image = post[3]
                    current_post_date = post[4]
                    current_post_content = convert_markdown_to_html(post[5])
                
                    previous_post = get_previous_post(current_post_date)
                    previous_post_url = previous_post[0]
                    previous_post_title = previous_post[1]
                    previous_post_subtitle = previous_post[2]
                    previous_post_image = previous_post[3]
                    previous_post_date = previous_post[4]
                    next_post = get_next_post(current_post_date)
                    next_post_url = next_post[0]
                    next_post_title = next_post[1]
                    next_post_subtitle = next_post[2]
                    next_post_image = next_post[3]
                    next_post_date = next_post[4]

                    #related posts 

                    with open(os.path.join(os.path.join(os.getcwd(), themefolder,'templates','single_post.html')), 'r') as template_file:
                        related_posts = get_related_posts(current_post_title)                
                        template = template_file.read()
                        template = template.replace('post_title', current_post_title)
                        template = template.replace('post_subtitle', current_post_subtitle)
                        template = template.replace('post_date', current_post_date)
                        template = template.replace('post_image', current_post_image)
                        
                        template = template.replace('previous_post_url', previous_post_url)
                        template = template.replace('next_post_url', next_post_url)
                        template = template.replace('post_content', current_post_content)
                        related_posts_widget = generate_related_posts_widget(get_related_posts(current_post_title))
                        template = template.replace('related_posts_widget',related_posts_widget)
                        blogroll = get_blogroll_posts()
                        blogroll = sort_posts_by_date(blogroll)
                        template = template.replace('sidebar_component', generate_sidebar_widget(blogroll))
                        template = replace_config_data(template)

                        newPostFileName = current_post_url
                        with open(os.path.join(os.getcwd(), 'site', newPostFileName), 'w') as newpost:
                            newpost.write(template)
                            newpost.close
                            template_file.close   
        break
def generate_pagination_widget(current_page_index:int,total_pages:int):
    #todo generate pagination buttons and numbers based on templates
    if os.path.isfile(os.path.join(os.getcwd(), themefolder,'templates','pagination.html')):
        with open(os.path.join(os.getcwd(), themefolder,'templates','pagination.html'),'r') as template_file:
            pagination_widget_template = template_file.read()

            #todo make more generic, this right now works specifically with 3 previous/next posts
            pagination_previous_page_1_number = '1'
            pagination_previous_page_2_number = '2'if total_pages >1 else '...'
            pagination_previous_page_3_number = '3'if total_pages >2 else '...'
            pagination_next_page_1_number = total_pages -2 if total_pages >2 else '...'
            pagination_next_page_2_number = total_pages -1 if total_pages >1 else '...'
            pagination_next_page_3_number = total_pages  if total_pages >0 else '...'
            pagination_previous_page_url = 'page_'+ str(current_page_index)+'.html' if total_pages >1 and current_page_index >1 else '/'
            pagination_previous_page_1_url = 'index.html'
            pagination_previous_page_2_url = 'page_2.html' if total_pages >1 else '/'
            pagination_previous_page_3_url = 'page_3.html' if total_pages >2 else '/'
            pagination_next_page_1_url = 'page_'+ str(total_pages - 2)+'.html'  if total_pages >3 else '/'
            pagination_next_page_2_url = 'page_'+ str(total_pages - 1)+'.html'  if total_pages >2 else '/'
            pagination_next_page_3_url = 'page_'+ str(total_pages )+'.html'
            pagination_next_page_url = 'page_'+ str(current_page_index+1)+'.html' if total_pages >1 and current_page_index < total_pages else '/'

            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_1_number',str(pagination_previous_page_1_number))
            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_2_number',str(pagination_previous_page_2_number))
            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_3_number',str(pagination_previous_page_3_number))
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_1_number',str(pagination_next_page_1_number))
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_2_number',str(pagination_next_page_2_number))
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_3_number',str(pagination_next_page_3_number))
            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_url',pagination_previous_page_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_1_url',pagination_previous_page_1_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_2_url',pagination_previous_page_2_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_previous_page_3_url',pagination_previous_page_3_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_1_url',pagination_next_page_1_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_2_url',pagination_next_page_2_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_3_url',pagination_next_page_3_url)
            pagination_widget_template = pagination_widget_template.replace('pagination_next_page_url',pagination_next_page_url)
            return pagination_widget_template

def sort_posts_by_date(posts,descending=True):
    if descending:
        return sorted(posts,key=lambda x: dt.strptime(x[4], "%Y-%m-%d"),reverse=True)
    else:
        return sorted(posts,key=lambda x: dt.strptime(x[4], "%Y-%m-%d"),reverse=False)

def generate_pagination_pages():
        global paginated_pages
        paginated_pages = []
        frontpage_featured_teaser_length = get_single_value_from_config('frontpage_featured_teaser_length')
        pages = get_paginated_posts()
        for index, pagination_page in enumerate(pages):
            with open(os.path.join(os.getcwd(), themefolder,'templates','index.html'),'r') as template_file:
                template = template_file.read()
            

                template = template.replace('sidebar_component', generate_sidebar_widget(pagination_page))          
                
                template = template.replace('featured_post_url', pagination_page[0][0])
                template = template.replace('featured_post_title', pagination_page[0][1])
                template = template.replace('featured_post_subtitle', pagination_page[0][2])
                template = template.replace('featured_post_image',pagination_page[0][3])
                template = template.replace('featured_post_date',pagination_page[0][3])
                template = template.replace('featured_post_teaser_text',pagination_page[0][5][:int(frontpage_featured_teaser_length)])

                for post in  pagination_page:
                    template = template.replace('blog_roll',generate_blogroll_widget(pagination_page))
                    template = template.replace('featured_post_widget',generate_featured_post_widget(pagination_page))
                    template = replace_config_data(template)
                
                if index == 0:
                    with open(os.path.join(os.getcwd(), 'site','index.html'), 'w') as indexPage:
                        paginated_pages.append(index)
                        template = template.replace('pagination_widget',generate_pagination_widget(index+1,len(pages)))
                        indexPage.write(template.replace('.md','.html').replace('.markdown','.html'))
                        indexPage.close
                        
                else: 
                    with open(os.path.join(os.getcwd(), 'site','page_'+str(index+1) +'.html'), 'w') as indexPage:
                        template = template.replace('pagination_widget',generate_pagination_widget(index,len(pages)))
                        paginated_pages.append(index+1)
                        indexPage.write(template.replace('.md','.html').replace('.markdown','.html'))
                        indexPage.close
                template_file.close



def main():
    copy_theme_files()
    copy_images_from_cms_to_site()
    generate_post_pages()
    generate_pagination_pages()
    optimize_images()

if __name__ == "__main__":
    main()