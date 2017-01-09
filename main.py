import page
import upload


def main():
	file_name="dashengzhuan.txt"
	pageUrl="http://book.easou.com/w/read/8140825/10811075/1666.html"
	page.download_page(pageUrl,file_name)
	upload.upload_file(file_name)

main()