# About Jackal
Jackal is a website CMS based on Python that was inspired by Jekyll's great concept of creating blazing fast static HTML sites from Markdown files.

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
  
# Installation and Setup
The CMS itself is free to use in your own projects but I worked off of a paid HTML template called [Arwyn](https://themeforest.net/item/arwyn-creative-personal-html-template/7698147).
This will change in a future release as I add more themes but right now if you wanted to use this as-is in production you would need to acquire a 16$ license for it.

To use just create an empty repository and place the CMS and Arwyn (or any other upcoming theme folders) into it. Run the CreatePostFromMarkdown.py file and push the generated site/ directory to your master branch to have it built by Netlify. 

# Upcoming features

