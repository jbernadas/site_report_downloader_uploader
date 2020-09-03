  EMPTY = []

class MyHTMLParser(HTMLParser):

    def __init__(self, pageMap, redirects, baseUrl, maxUrls, blockExtensions, robotParser):
        HTMLParser.__init__(self)
        self.pageMap = pageMap
        self.redirects = redirects
        self.baseUrl = baseUrl
        self.server = urllib.parse.urlsplit(baseUrl)[1] # netloc in python 2.5
        self.maxUrls = maxUrls
        self.blockExtensions = tuple(blockExtensions)
        self.robotParser = robotParser
    #end def

    def hasBlockedExtension(self, url):
        p = urllib.parse.urlparse(url)
        path = p[2].upper() # path attribute
        return path.endswith(self.blockExtensions)
    #end def

    def handle_starttag(self, tag, attrs):
        if len(self.pageMap) >= self.maxUrls:
            return

        if tag.upper() == "BASE":
            if attrs[0][0].upper() == "HREF":
                self.baseUrl = joinUrls(self.baseUrl, attrs[0][1])
                print("BASE URL set to " + self.baseUrl)

        if tag.upper() == "A":
            #print("Attrs: " + str(attrs))
            url = ""
            # Let's scan the list of tag's attributes
            for attr in attrs:
                #print("  attr: " + str(attr))
                if (attr[0].upper() == "REL") and (attr[1].upper().find('NOFOLLOW') != -1):
                    # We have discovered a nofollow, so we won't continue
                    return
                elif (attr[0].upper() == "HREF") and (attr[1].upper().find('MAILTO:') == -1):
                    # We have discovered a link that is not a Mailto:
                    url = joinUrls(self.baseUrl, attr[1])
            #end for
            # if the url is empty, there was none in the list of attributes
            if url == "":
                return

            # Check if we want to follow the link
            if urllib.parse.urlsplit(url)[1] != self.server:
                return
            if self.hasBlockedExtension(url) or self.redirects.count(url) > 0:
                return
            if self.robotParser is not None and not self.robotParser.allowed(url, "sitemap_gen"):
                print("URL restricted by ROBOTS.TXT: " + url)
                return
            # It's OK to add url to the map and fetch it later
            if not url in self.pageMap:
                self.pageMap[url] = EMPTY
        #end if

        ### ADDED BY JB TO GET IMAGES AS WELL ###
        if tag.upper() == "IMG":
            url = ""
            for attr in attrs:
                if attr[0].upper() == "SRC":
                    url = joinUrls(self.baseUrl, attr[1])
            #end for

            if  url == "":
                return
            
            # Check if we want to follow the link
            if urllib.parse.urlsplit(url)[1] != self.server:
                return
            if self.hasBlockedExtension(url) or self.redirects.count(url) > 0:
                return
            if self.robotParser is not None and not self.robotParser.allowed(url, "sitemap_gen"):
                print("URL restricted by ROBOTS.TXT: " + url)
                return
            # It's ok to add url to the map and fetch it later
            if not url in self.pageMap:
                self.pageMap[url] = EMPTY
        #end if
        ### END OF JB ADDED ###
    #end def
#end class
