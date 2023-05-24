#!/usr/bin/env python3
import wikipedia
import urllib
from bs4 import BeautifulSoup

class LastPageWiki:
    def __init__(self, language = "en") -> None:
        wikipedia.set_lang("en")
        self.wiki_base_url = "https://en.wikipedia.org" 

    def __is_idx_valid(self,idx):
        """Return -1 if invalid idx."""
        #TODO : add checks for validity
        return int(idx)


    def __is_valid_link(self, ref, paragraph):
        """Return True for a valid out link in a paragraph."""
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

    def __get_valid_wiki_query(self):
        """Method to interact with user and wikipedia to get first valid wiki page title.
        
        :return: Valid Wikipedia Page Title.
        """
        is_valid_query = False
        while not is_valid_query:
            query = input("Enter search term for wikipedia: ")
            suggestions = wikipedia.search(query)
            valid_query = ""
            sidx = 1
            if len(suggestions) == 0:
                    print("Not found")
                    continue
            elif len(suggestions) == 1:
                valid_query = suggestions[0]
            else:
                #ignoring the first suggestion to handle redirection pages.
                suggestions = suggestions[1:] 
                for suggestion in suggestions: 
                    print("{}. {}".format(sidx,suggestion))
                    sidx +=1
                idx = input("Enter query number (0 to Exit): ")
                idx = self.__is_idx_valid(idx)
                if idx == 0:
                    return None
                elif idx == -1:
                    print("Invalid input.")
                    continue
                else:
                    is_valid_query = True
                    valid_query = suggestions[idx-1]
        
        wiki_title = '_'.join(valid_query.split())
        return wiki_title

    def __get_first_link_in_page(self, wiki_page_url):
        """Methode to extract first wikipedia page outlink in the given wiki url.

        :param wiki_page_url : A valid wikipedia page url.
        :return: first wiki out link in the given wiki url.
        """
        req = urllib.request.Request(wiki_page_url)
        page = urllib.request.urlopen(req)
        data = page.read()
        soup = BeautifulSoup(data, "html.parser")
        tag = soup.find(id="mw-content-text")
        paragraphs = tag.find_all("p")
        for paragraph in paragraphs:
            for link in paragraph.find_all("a"):
                ref = link.get("href")
                if self.__is_valid_link(str(ref),str(paragraph)):
                    return ref
        return False





    def __get_page_list(self,start_wiki_url):
        """Method to recursively crawl first valid link in wiki page till we reach an already seen page.

        :param start_wiki_url: Valid starting wikipedia page link.
        :return: List of wikipedia page url (ordered by visit) ending at an already visited page.
        """
        is_seen = False
        next_url = start_wiki_url
        page_list = [start_wiki_url]
        while not is_seen:
            next_url = self.__get_first_link_in_page(next_url)
            next_url = self.wiki_base_url + next_url
            if next_url in page_list:
                is_seen = True
            page_list.append(next_url)
        return page_list

    def show_info(self,page_list):
        """Method to display the page list"""
        print("{0} Showing List {0}".format("*"*5))
        print("Wiki link counts : {}.".format(len(page_list)))
        
        #last page is the list is an already seen page. Take second last page in the list.
        last_page = page_list[-2]
        last_page_title = ' '.join(last_page.split('/')[-1].split('_'))
        print("Wiki Chain ends in '{}'".format(last_page_title))
        page_title_list=[ ' '.join(link.split('/')[-1].split('_')) for link in page_list ]
        print(' -> '.join(page_title_list))
        print("*"*25)

    def get_pages(self):
        """ Get first, last and all the pages in between.
        """
        query = self.__get_valid_wiki_query()
        if query:
            first_url = self.wiki_base_url+"/wiki/"+query
            link_list = self.__get_page_list(first_url)
        self.show_info(link_list)
        print("Finished query.")


if __name__ == '__main__':
    pages1 = LastPageWiki()
    pages1.get_pages()