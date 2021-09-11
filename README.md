# WSCTW-Topics-Flarum-Post-2
 全國技能競賽題目自動更新發佈到Flarum.  
 使用Python搭配[wdasec-announcement-crawler](https://github.com/CRT-HAO/wdasec-announcement-crawler)進行了重寫
 
## 部署
1. 初始化submodule
```
git submodule init
git submodule update
```
2. 安裝相依套件
 - requests `pip3 install requests`
 - BeautifulSoup4 `pip3 install beautifulsoup4`
 - pyFlarum `pip3 install pyflarum`
 - pytablewriter `pip3 install pytablewriter`
 - python-dotenv `pip3 install python-dotenv`
3. 編寫配置檔
在目錄下新增`.env`檔案
```
forum_url = Flarum論壇網址
username = 使用者帳號
password = 使用者密碼

announcement_url = 技能競賽題目公告網址

discussion_id = 用於發布更新的Flarum論壇討論串
```
## 運行

```
python3 main.py
```
## 範例
[https://taiwanskills.cish.xyz/d/11-51](https://taiwanskills.cish.xyz/d/11-51)
