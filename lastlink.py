#!/usr/bin/env python3
import wikipedia
import urllib
from bs4 import BeautifulSoup

wikipedia.set_lang("en")
template = "https://en.wikipedia.org"    


def is_idx_valid(idx):
    """Return -1 if invalid idx."""
    #TODO : add checks for validity
    return int(idx)


def isValid(ref,paragraph):
   if not ref or "#" in ref or "//" in ref or ":" in ref:
      return False
   if "/wiki/" not in ref:
      return False
   if ref not in paragraph:
      return False
   prefix = paragraph.split(ref,1)[0]
   if prefix.count("(")!=prefix.count(")"):
      return False
   return True

def validateTag(tag):
   name = tag.name
   isParagraph = name == "p"
   isList = name == "ul"
   return isParagraph or isList

def get_first_link(url):
   print(url)
   req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
   page = urllib.request.urlopen(req)
   data = page.read()
   soup = BeautifulSoup(data, "html.parser")
   tag = soup.find(id="mw-content-text")
   paragraphs = tag.find_all("p")
   #print("text content: ",paragraphs)
   for paragraph in paragraphs:
      #print("Processing Paragraph: ", paragraph)
      for link in paragraph.find_all("a"):
        #print("Processing link.")
        ref = link.get("href")
        #print(ref)
        if isValid(str(ref),str(paragraph)):
            return ref
   return False

def get_valid_query():
    """Return the first valid wiki link."""
    is_valid = False
    while not is_valid:
        query = input("Enter search term for wikipedia: ")
        suggestions = wikipedia.search(query)
        final = ""
        sidx = 1
        if len(suggestions) == 0:
                print("Not found")
                continue
        elif len(suggestions) == 1:
            final = suggestions[0]
        else:
            #ignoring the first suggestion to handle redirection.
            suggestions = suggestions[1:] 
            for suggestion in suggestions: 
                print("{}. {}".format(sidx,suggestion))
                sidx +=1
            idx = input("Enter query number (0 to Exit): ")
            idx = is_idx_valid(idx)
            if idx == 0:
                return None
            elif idx == -1:
                print("Invalid input.")
                continue
            else:
                is_valid = True
                final = suggestions[idx-1]
    print("Topic: ", final)
    tile_str = '_'.join(final.split())
    return tile_str




def get_link_list(first_url):
    """Recursively crawl first link in wiki page.
    Return list of links terminating at link pointing to itself.
    """
    is_repeat = False
    next_url = first_url
    link_list = [first_url]
    while not is_repeat:
        next_url = get_first_link(next_url)
        next_url = template + next_url
        if next_url in link_list:
            is_repeat = True
        link_list.append(next_url)
    return link_list

def show_info(link_list):
    """Display the list"""
    print("{0} Showing List {0}".format("*"*5))
    print("Wiki link counts : {}.".format(len(link_list)))
    print("Chain ends in cycle of {}".format(link_list[-1]))
    for link in link_list:
        print(link)
    print("*"*25)

def main():
    """"""
    query = get_valid_query()
    if query:
        first_url = template+"/wiki/"+query
        link_list = get_link_list(first_url)
    
    print("Finished query.")

    show_info(link_list)


if __name__ == '__main__':
    main()