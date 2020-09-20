import os
import re

for root, dirs, files in os.walk(os.path.join(os.getcwd(),'cms/posts')):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root,file)) as f:
                    post_text = f.read() #this way we get to separate frontmatter from post content
                    frontmatter = re.match(r'(---)((.|\n)*?)(---)',post_text).group(2)
                    post_content = re.sub(r'(---)((.|\n)*?)(---)','',post_text).lstrip('\n')