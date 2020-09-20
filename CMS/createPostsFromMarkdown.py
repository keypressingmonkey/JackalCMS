import os
import re
import pprint
from datetime import datetime as dt

current_post_title = ''
current_post_subtitle = ''
current_post_image = ''
current_post_date = ''
current_post_content = ''

def get_previous_post():
    previous_post_url = ''
    previous_post_title = ''
    previous_post_subtitle = ''
    previous_post_image = ''
    all_previous_posts = []

    for file in os.listdir(os.path.join(os.getcwd(),'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root,file)) as f:
                post_text = f.read() #this way we get to separate frontmatter from post content
                frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                subtitle = re.search(r'(\nsubtitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                date = dt.strptime(date,"%Y-%m-%d")
                master_post_date = dt.strptime(current_post_date, "%Y-%m-%d")
                if date < master_post_date:
                    all_previous_posts.append([file,title,subtitle,image,date])
    if all_previous_posts:
        return max(sorted(all_previous_posts, key=lambda tup: tup[4])) #this sorts by date and returns the highest, aka the previous post
    else:
        return(['/','Homepage','','default.jpg',''])

def get_next_post():
    next_post_url = ''
    next_post_title = ''
    next_post_subtitle = ''
    next_post_image = ''
    all_next_posts = []

    for file in os.listdir(os.path.join(os.getcwd(),'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root,file)) as f:
                post_text = f.read() #this way we get to separate frontmatter from post content
                frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                subtitle = re.search(r'(\nsubtitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                date = dt.strptime(date,"%Y-%m-%d")
                master_post_date = dt.strptime(current_post_date, "%Y-%m-%d")
                if date > master_post_date:
                    all_next_posts.append([file,title,subtitle,image,date])
    if all_next_posts:
        return min(sorted(all_next_posts, key=lambda tup: tup[4])) #this sorts by date and returns the lowest with a higher date than the mainw, aka the next post
    else:
        return(['/','Homepage','','default.jpg',''])

def get_featured_post():
    next_post_url = ''
    next_post_title = ''
    next_post_subtitle = ''
    next_post_image = ''
    all_posts = []

    for file in os.listdir(os.path.join(os.getcwd(),'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root,file)) as f:
                post_text = f.read() #this way we get to separate frontmatter from post content
                frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                subtitle = re.search(r'(\nsubtitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                date = dt.strptime(date,"%Y-%m-%d")
                all_posts.append([file,title,subtitle,image,date])
    
    return max(sorted(all_posts, key=lambda tup: tup[4])) #this sorts by date and returns the highest, aka the most recent post
    
def get_blogroll_posts():
    next_post_url = ''
    next_post_title = ''
    next_post_subtitle = ''
    next_post_image = ''
    all_posts = []

    for file in os.listdir(os.path.join(os.getcwd(),'cms/posts')):
        if file.endswith('.md') or file.endswith('.markdown'):
            with open(os.path.join(root,file)) as f:
                post_text = f.read() #this way we get to separate frontmatter from post content
                frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                subtitle = re.search(r'(\nsubtitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
                date = re.search(r'(\ndate: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                date = dt.strptime(date,"%Y-%m-%d")
                all_posts.append([file,title,subtitle,image,date])
    
    sorted_list = sorted(all_posts, key=lambda tup: tup[4])
    return sorted_list[len(all_posts)-2] #here we sort by date and skip the highest to start the blogroll with the first nonfeatured post
    




for root, dirs, files in os.walk(os.path.join(os.getcwd(),'cms/posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root,file)) as f:
                    post_text = f.read() #this way we get to separate frontmatter from post content
                    frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                    current_post_content = re.sub(r'(---)((.|\n)*?)(---)','',post_text).lstrip('\n')
                    current_post_title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                    current_post_subtitle = re.search(r'(\nsubtitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                    current_post_image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
                    current_post_date = re.search(r'(\ndate: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                    current_post_content = re.sub(r'(### )(.*?)($|\n)',r'<h4>\2</h4>\n',current_post_content) #todo order is important here, better fix this 
                    current_post_content = re.sub(r'(## )(.*?)($|\n)',r'<h3>\2</h3>\n',current_post_content)
                    current_post_content = re.sub(r'(# )(.*?)($|\n)',r'<h2>\2</h2>\n',current_post_content)
                    current_post_content = re.sub(r'!\[(.*?)\]\((.*?)\)',r'<img src="\2" alt="\1" />',current_post_content)
                    current_post_content = re.sub(r'\[(.*?)\]\((.*?)\)',r'<a href="\2">\1</a>',current_post_content)
                    current_post_content = re.sub(r'(\n)(.*?)($|\n)',r'\n<p>\2</p>\n',current_post_content)
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

                    with open(os.path.join(os.path.join(os.getcwd(),'posts/post.html')),'r') as f:
                        template = f.read()
                        template = template.replace('post_title',current_post_title)
                        template = template.replace('post_subtitle',current_post_subtitle)
                        template = template.replace('site_name','site_name') #todo pull from config
                        template = template.replace('previous_post_url',previous_post_url) 
                        template = template.replace('next_post_url',next_post_url) 
                        template = template.replace('post_content',current_post_content) 


                        newPostFileName = current_post_title.replace('.md','.html').replace('.markdown','.html').replace(' ','_')
                        with open(os.path.join(os.getcwd(),'posts',newPostFileName+'.html'),'w') as newpost:
                            newpost.write(template)
                            newpost.close
