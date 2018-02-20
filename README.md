# scrapy_Zhihu

## 1模拟登陆思路 ---
  xsrf---通过get请求 + 正则 得到
  username 
  pwd
  
  ------知乎验证的数据 很多，这里直接 用cookie登陆了
  
## 2 利用递归，深度优先，来获取全网站的 问题回答
    提取 相关 的 url
    并 yield Request 请求
    
## 3 item 和 item_loader机制 来获取有用的 信息

## 4 pipeline --- 连接 mysql数据库 保存数据 --这里可以使用 twisted的 adbapi的连接池 优化，异步数据插入 数据库
  
## 5 sql 语句 在 insert的时候 考虑，爬取时候数据的更新---使用sql的 ON DUPLICATE KEY UPDATE content=VALUES(contetn)











