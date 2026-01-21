from utils.downloader import Downloader
from utils.mail import Mail
downloader = Downloader()

downloader.download("https://www.zxxk.com/soft/36887191.html")

#Mail().send(["XXX"]) #XXX 为收件人邮箱

