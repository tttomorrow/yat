--  @testpoint:创建并使用词典synonym，结合tsvector函数
drop TEXT SEARCH DICTIONARY if exists syn;
CREATE TEXT SEARCH DICTIONARY syn (
    TEMPLATE = synonym,
    SYNONYMS = synonym_sample
);
--测试一个数据字典，返回字串原型
SELECT ts_lexize('syn','indices');
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists tst;
CREATE TEXT SEARCH CONFIGURATION tst (copy=simple);
--增加映射
 ALTER TEXT SEARCH CONFIGURATION tst ALTER MAPPING FOR asciiword WITH syn;
--使用to_tsvector函数，指定文本搜索配置为自定义的tst
SELECT to_tsvector('tst','indices');
--使用::tsvector函数，原样输出
SELECT 'indexes:2A are very useful'::tsvector;
--::tsvector对indexes返回index，to_tsquery('tst','indices')返回'index':*，故返回t
SELECT 'indexes are very useful'::tsvector @@ to_tsquery('tst','indices');
--删除词典，合理报错（文本搜索配置依赖于词典）
drop TEXT SEARCH DICTIONARY syn;
--删除词典，添加cascade参数
drop TEXT SEARCH DICTIONARY syn cascade;
