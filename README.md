
>*这是我练习python写的小说爬虫，不用于商业用途，如果有侵权等，请联系本人删除代码 qq:578593908*

----------

* 首先确认你已经有PYTHON基础，明白什么是模块，以及知道你的PYTHON脚本缺少什么模块和如何安装模块。
* 所有执行都在main.py中，下面开始介绍使用。

----------

1. 变量的一些声明<pre><code>bookname='小说名'
pinyinbookname='xiaoshuopinyingming'
epubpath="books"+os.path.sep+pinyinbookname+".epub"
uploadurl="http://xxx.xxx.xxx.xxx:12121/files" 
</code></pre>
2. `startIndex(bookname)` 用于根据小说名搜索小说列表，定位出小说的目录url，并检索出目录url，存入sqlite3
3. `startDownload(bookname)` 根据第1步检索出的目录url，下载每个章节的小说内容
4. `packageEpub(pinyinbookname,'作者')` 打包下载好的各章节内容成epub格式，这里需要注意，第一个参数为英文，因为我也还没搞定python下的中文路径，然后上传至小说阅读器后的名字乱码的问题
5. `upload.uploadFile(epubpath,uploadurl)` 将打包好的epub格式小说上传至手机阅读器，这里我用的是多看阅读，代码中的上传是模拟多看阅读的wifi传输实现的上传


