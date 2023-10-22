"""All HTML related data here"""


class AllTopicsPage:

    topic = {
        "tag": "div",
        "class_name": "flex direction-column flex-column-gap-2"
        }


class TopicPage:
    
    product = {
        "tag": "div",
        "class_name": "styles_item__jDvwG flex direction-row flex-row-gap-4 flex-row-gap-mobile-3 flex-row-gap-widescreen-undefined flex-1 px-mobile-1 px-tablet-1 pt-mobile-0 pt-desktop-6 pt-tablet-6 pt-widescreen-6 pb-mobile-7 pb-desktop-6 pb-tablet-6 pb-widescreen-6"
        }


class ProductPage:

    columns = ("name", "blurb", "description", "rating", "reviews", "followers", "category", "link")
        
    name = {
        "tag": "h1", 
        "class_name": "color-darker-grey fontSize-desktop-32 fontSize-tablet-32 fontSize-mobile-18 fontSize-widescreen-32 fontWeight-700 noOfLines-undefined"
        }
        
    blurb = {
        "tag": "div",
        "class_name": "color-lighter-grey fontSize-18 fontWeight-400 noOfLines-undefined"
        }
        
    description = {
        "tag": "div",
        "class_name": "mb-6 color-lighter-grey fontSize-16 fontWeight-400 noOfLines-undefined"
        }
        
    rating = {
        "tag": "script",
        "type": "application/ld+json"
        }
        
    reviews = {
        "tag": "a",
        "class_name": "color-lighter-grey fontSize-14 fontWeight-400 noOfLines-undefined styles_count___6_8F"
        }
        
    followers = {
        "tag": "div",
        "class_name": "color-lighter-grey fontSize-14 fontWeight-400 noOfLines-undefined styles_count___6_8F"
        }
        
    category = {
        "tag": "span",
        "class_name": "color-darker-grey fontSize-12 fontWeight-600 noOfLines-undefined styles_subnavLinkText__WGIz0"
        }

    link = {
        "tag": "a",
        "class_name": "color-lighter-grey fontSize-14 fontWeight-600 noOfLines-undefined styles_format__k3_8m flex align-center"
        }
