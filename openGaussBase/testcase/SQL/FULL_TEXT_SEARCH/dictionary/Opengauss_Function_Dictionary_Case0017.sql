--  @testpoint:创建并使用词典synonym，结合tsquery函数
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
--使用to_tsquery函数，指定文本搜索配置为自定义的tst
SELECT to_tsquery('tst','indices');
--使用::tsquery函数，原样输出
SELECT 'indexes & are & very & useful'::tsquery;
--返回f
SELECT 'indexes are very useful'::tsvector @@ to_tsquery('tst','index');
--删除词典
drop TEXT SEARCH DICTIONARY syn cascade;