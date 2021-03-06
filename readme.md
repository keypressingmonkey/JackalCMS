# About Jackal
Jackal is a website CMS based on Python that was inspired by Jekyll's great concept of creating blazing fast static HTML sites from Markdown files. See the result in action [here](https://compassionate-hawking-9b2eb5.netlify.app/)

Here is a Jackal fighting a Python to see how the development process looked like.
https://www.youtube.com/watch?v=JgKN3BuvC3E

Features:
 - Works with _any_ HTML template (you just place the needed variables inside your index.html and single post templates)
 - Automatic image optimization using PIL (will also generate the right thumbnail sizes for featured posts, sidebar thumbnails etc.)
 - Takes a list of Markdown files inside the CMS/Posts directory and generates valid HTML from them to create posts and your index file. 
  - Generates previous / next post links, related posts (currently randomized)
  - Site configuration file to allow you to place common values like author and site information, number of featured posts etc.)
  - Currently works with the basic Markdown elements (images, links, headings and regular text).
  - Support for drafts inside the CMS/posts/drafts folder, just take the files out into the main directory as soon as you're done with writing
 - Creates an automatic deploy of your theme chosen in your config and pushes it to the site/ directory for easy setup with Netlify
 ![](cms/images/2020-09-24-15-36-54.png)
  
# Installation and Setup
The CMS itself is free to use in your own projects but I worked off of a paid HTML template called [Arwyn](https://themeforest.net/item/arwyn-creative-personal-html-template/7698147).
This will change in a future release as I add more themes but right now if you wanted to use this as-is in production you would need to acquire a 16$ license for it.

To use just create an empty repository and place the CMS and Arwyn (or any other upcoming theme folders) into it. Run the CreatePostFromMarkdown.py file and push the generated site/ directory to your master branch to have it built by Netlify. 

For configuration there are two relevant files: 
- cms/siteConfig.md for everything that is configured globally
- THEMEFOLDER/themeConfig.md for everything that is specific to the theme like image dimensions and number of featured posts. 

Bonus tip: Use this image-to-Markdown poster plugin for VS Code and make your life a lot easier: https://marketplace.visualstudio.com/items?itemName=mushan.vscode-paste-image

# Adapt to your own theme

- Download HTML theme as normally inside the root folder of your repository
- Add the CMS folder from this project to the root directory 
- Inside the theme folder create a new one called templates with the following HTML files:
 - blogroll_post.html (this is your main page blogroll single post)
 - footer.html
 - index.html
 - post_featured.html
 - recent_posts_sidebar.html
 - related_posts.html
 - single_post.html
 - themeConfig.html

For the most part you will use the files from your new theme here and place the needed variables inside. The following ones are available:
- Anything in either themeConfig.md or cms/siteConfig.md will be auto-replaced if you put the name inside your html templates
- #todo fill later

- You can also replace sidebar, related posts and recent posts widgets, refer to the index.html in the default folders for further examples of this. This way we can reuse components across multiple html pages which saves a lot of time. 

# Upcoming features
- ~~Make images as links possible~~ Done!
- ~~Add theme specific configuration files~~ Done!
- ~~Add pagination~~ Partly implemented, use the massively theme to see how it works but the implementation is not yet generic enough to work with any theme. 
- implement new (free!) themes and adapt them for rapid prototyping - first one done! Just change "arwyn" or "massively" in cms/siteConfig.md and rebuild the site to be amazed.
- Make image optimization and resizing configurable per theme
- ~~Add support for Markdown lists~~
