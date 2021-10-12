--  @testpoint:删除词典测试,词典依赖文本搜索配置
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists ts_conf cascade;
CREATE TEXT SEARCH CONFIGURATION ts_conf ( COPY = pg_catalog.english );
--创建词典
drop TEXT SEARCH DICTIONARY if exists thesaurus_astro cascade;
CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
    TEMPLATE = thesaurus,
    DictFile = thesaurus_sample,
    Dictionary = pg_catalog.english_stem
);
--设置文本搜索配置ts_conf，修改某些类型的token对应的词典列表
ALTER TEXT SEARCH CONFIGURATION ts_conf ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,word, hword, hword_part WITH thesaurus_astro;
--删除词典，不加cascade，合理报错
drop TEXT SEARCH DICTIONARY thesaurus_astro;
--删除词典，添加cascade，删除成功
drop TEXT SEARCH DICTIONARY thesaurus_astro cascade;