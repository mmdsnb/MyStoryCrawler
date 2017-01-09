#!encoding:utf-8

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import zipfile
import os.path



def upload_file(fileName):
	register_openers()
	params = {"newfile": open(fileName, "rb")}
	datagen, headers = multipart_encode(params)
	request = urllib2.Request("http://192.168.1.112:12121/files", datagen, headers)
	print urllib2.urlopen(request).read()



def write_epub():
	# book = epub.open_epub('book.epub', u'w')
	# filename = r'book\add.xhtml'
	# manifest_item = epub.opf.ManifestItem(identifier='IdFile',href=r'books\add.xhtml',media_type='application/xhtml+xml')
	# book.add_item(filename, manifest_item)
	# book.close()


	epub = zipfile.ZipFile('my_ebook.epub', 'w')
	# The first file must be named "mimetype"
	epub.writestr("mimetype", "application/epub+zip")

	# The filenames of the HTML are listed in html_files
	html_files = [r'book\foo.html', r'book\bar.html']

	# We need an index file, that lists all other HTML files
	# This index file itself is referenced in the META_INF/container.xml
	# file
	epub.writestr("META-INF/container.xml", '''<container version="1.0"
	           xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
	  <rootfiles>
	    <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
	  </rootfiles>
	</container>''');

	# The index file is another XML file, living per convention
	# in OEBPS/Content.xml
	index_tpl = '''<package version="2.0"
	  xmlns="http://www.idpf.org/2007/opf">
	  <metadata/>
	  <manifest>
	    %(manifest)s
	  </manifest>
	  <spine toc="ncx">
	    %(spine)s
	  </spine>
	</package>'''

	manifest = ""
	spine = ""

	# Write each HTML file to the ebook, collect information for the index
	for i, html in enumerate(html_files):
	    basename = os.path.basename(html)
	    manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
	                  i+1, basename)
	    spine += '<itemref idref="file_%s" />' % (i+1)
	    epub.write(html, 'OEBPS/'+basename)

	# Finally, write the index
	epub.writestr('OEBPS/Content.opf', index_tpl % {
	  'manifest': manifest,
	  'spine': spine,
	})

write_epub()
