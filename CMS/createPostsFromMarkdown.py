import os
import re
import pprint

for root, dirs, files in os.walk(os.path.join(os.getcwd(),'cms/posts')):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                with open(os.path.join(root,file)) as f:
                    post_text = f.read() #this way we get to separate frontmatter from post content
                    frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                    post_content = re.sub(r'(---)((.|\n)*?)(---)','',post_text).lstrip('\n')
                    title = re.search(r'(\ntitle: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                    image = re.search(r'(\nimage: ")(.*?)(")',frontmatter).group(2)
                    date = re.search(r'(\ndate: ")(.*?)(")',frontmatter,re.MULTILINE).group(2)
                    post_content = re.sub(r'(### )(.*?)($|\n)',r'<h4>\2</h4>\n',post_content) #todo order is important here, better fix this 
                    post_content = re.sub(r'(## )(.*?)($|\n)',r'<h3>\2</h3>\n',post_content)
                    post_content = re.sub(r'(# )(.*?)($|\n)',r'<h2>\2</h2>\n',post_content)
                    post_content = re.sub(r'!\[(.*?)\]\((.*?)\)',r'<img src="\2" alt="\1" />',post_content)
                    post_content = re.sub(r'\[(.*?)\]\((.*?)\)',r'<a href="\2">\1</a>',post_content)
                    post_content = re.sub(r'(\n)(.*?)($|\n)',r'\n<p>\2</p>\n',post_content)

                    pprint.PrettyPrinter(indent=6).pprint(post_content)