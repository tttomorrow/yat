--  @testpoint:to_tsvector函数测试（把文档处理成tsvector数据类型）
--解析文档，其中tsvector中列出了词素及它们在文档中的位置
 SELECT to_tsvector('english', 'a fat  cat sat on a mat - it ate a fat rats');
 --不带分词器，使用默认english分词器
 SELECT to_tsvector('a fat  cat sat on a mat - it ate a fat rats');
 --文档中的字串已ing结尾（也会删除）
 SELECT to_tsvector('a fat  cat sat on a mat - it ate a fating rats');
