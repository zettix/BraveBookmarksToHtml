#!/usr/bin/python3
"""
BraveBookmarksToHtml

By: Sean Brennan, 2026

Apache License

Convert Brave Browser "Bookmarks" file from json to html so
Brave can import its own Bookmarks file.
"""

import json
import getopt
import sys

opts, args = getopt.getopt(sys.argv[1:], "b:h:", ["bookmarks", "html"])

bfile = sys.stdin
hfile = sys.stdout

def usage():
  print("Usage: -b /bookmarks-file/ [-h /output-html/]")

for o, a in opts:
  if o == '-b':
    bfile = open(a, 'r')
    continue
  if o == '-h':
    hfile = open(a, 'w')
    continue
  usage()
  exit(1)

js = json.load(bfile)

class ToHtml:
  def __init__(self):
    self.lines = []

  def htmlHeader(self):
    header_text = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>

<DL><p>
    <DT><H3 ADD_DATE="1338185718" LAST_MODIFIED="1685668324" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks bar</H3>
    <DL><p>
"""
    self.lines.append(header_text)

  def emitUrl(self, child):
    da = child["date_added"]
    du = child["date_last_used"]
    gu = child["guid"]
    di = child["id"]
    na = child["name"]
    bu = child["url"]
    url_str = f'<DT><A HREF="{bu}" ADD_DATE="{da}">{na}</A>'
    self.lines.append(url_str)

  def emitFolderBegin(self, child):
    da = child["date_added"]
    du = child["date_last_used"]
    gu = child["guid"]
    di = child["id"]
    na = child["name"]
    url_str = f'<DT><H3 ADD_DATE="{da}" LAST_MODIFIED="{du}">{na}</H3>'
    self.lines.append(url_str)
    self.lines.append("<DL><p>")

  def processChildren(self, children):
    for child in children:
      tp = child["type"]
      if tp == "url":
        self.emitUrl(child)
      if tp == "folder":
        self.emitFolderBegin(child)
        self.processChildren(child["children"])
        self.lines.append("</DL><p>")

  def parseInput(self, book_dict):
    self.htmlHeader()
    children = book_dict["children"]
    self.processChildren(children)
    html_txt = '\n'.join(self.lines)
    return html_txt
      

bookmark_bar = js["roots"]["bookmark_bar"]
tohtml = ToHtml()
txt = tohtml.parseInput(bookmark_bar)
print(txt, file=hfile)
