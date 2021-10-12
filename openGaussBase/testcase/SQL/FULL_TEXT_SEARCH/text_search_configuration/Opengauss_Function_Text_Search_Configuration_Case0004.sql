--  @testpoint:创建文本搜索配置，添加COPY参数
--复制现有文本搜索配置为ngram
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (COPY=ngram);
--复制现有文本搜索配置为pound
DROP TEXT SEARCH CONFIGURATION if exists pound2;
CREATE TEXT SEARCH CONFIGURATION pound2 (copy=pound);
--复制现有文本搜索配置为english
DROP TEXT SEARCH CONFIGURATION if exists english2;
CREATE TEXT SEARCH CONFIGURATION english2 (copy=english);
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
DROP TEXT SEARCH CONFIGURATION pound2;
DROP TEXT SEARCH CONFIGURATION english2;