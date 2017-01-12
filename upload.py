#!encoding:utf-8

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import zipfile
import os.path
import chardet

class EpubUtil:
	'generater epub file utils'

	htmls=[]
	metadata={}
	epub=None

	def __init__(self):
		pass

	def createEpub(self,path):
		self.epub = zipfile.ZipFile(path, 'w')
		self.epub.writestr("mimetype", "application/epub+zip")
		self.epub.writestr("META-INF/container.xml", '''
				<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
				  <rootfiles>
				    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
				  </rootfiles>
				</container>
			''');

	def addItem(self,dirName,path):
		# if(self.epub is None):
		# 	raise Exception('epubutil must be createEpub before additem')
		item={"dirName":dirName,"path":path}
		self.htmls.append(item)

	def setMetadata(self,title,creator,description):
		self.metadata={"title":title,"creator":creator,"description":description}

	def close(self):

		metadata_tpl='''
		    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
			  	<dc:title>%(title)s</dc:title>
				<dc:creator>%(creator)s</dc:creator>
				<dc:description>%(description)s</dc:description>	
		  	</metadata>
		'''

		index_tpl = '''<?xml version='1.0' encoding='utf-8'?>
		<package version="2.0" xmlns="http://www.idpf.org/2007/opf">
		  %(metadata)s
		  <manifest>
		  	<item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>
		    %(manifests)s
		  </manifest>
		  <spine toc="ncx">
		    %(spines)s
		  </spine>
		</package>
		'''
		manifests=[]
		spines=[]
		navpoints =[]
		for i,html in enumerate(self.htmls):
			manifest='<item id="file_%d" href="%s" media-type="application/xhtml+xml"/>' %(i+1,html['path'])
			spine='<itemref idref="file_%d" /> ' %(i+1,)
			navpoint ='<navPoint id="file_%d" playOrder="%d"><navLabel><text>%s</text></navLabel><content src="%s"/></navPoint> ' %(i+1,i+1,html['dirName'],html['path'])
			manifests.append(manifest)
			spines.append(spine)
			navpoints.append(navpoint)
			#copy html
			self.epub.write(html['path'], html['path'], compress_type=zipfile.ZIP_DEFLATED)


		contentStr= index_tpl % {"manifests":''.join(manifests),"spines":''.join(spines),"metadata":metadata_tpl % self.metadata}
		self.epub.writestr("content.opf", contentStr)


		#toc.ncx
		toc_tpl='''<?xml version='1.0' encoding='utf-8'?>
			<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
			<head>
			<meta content="test" name="dtb:uid"/>
			<meta content="2" name="dtb:depth"/>
			<meta content="test" name="dtb:generator"/>
			<meta content="0" name="dtb:totalPageCount"/>
			<meta content="0" name="dtb:maxPageNumber"/>
			</head>
			<navMap>
				%(navpoint)s
			</navMap></ncx>
			'''

		navpointstr=toc_tpl % {'navpoint':''.join(navpoints)}
		self.epub.writestr("toc.ncx", navpointstr.encode('utf-8') )

		self.epub.close()


def upload_file(fileName):
	register_openers()
	params = {"newfile": open(fileName, "rb")}
	datagen, headers = multipart_encode(params)
	request = urllib2.Request("http://192.168.1.112:12121/files", datagen, headers)
	print urllib2.urlopen(request).read()


def packageEpub(name):
	epubUtil=EpubUtil()
	epubUtil.createEpub(r'd:\a.epub')
	epubUtil.setMetadata('title_epub','fm','this is a test epub')
	epubUtil.addItem('1zhang',r'book\1.html')
	epubUtil.addItem('2zhang',r'book\2.html')
	epubUtil.close()




