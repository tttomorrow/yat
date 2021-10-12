--  @testpoint:创建词典，词典模板为非PG_TS_TEMPLATE的值，合理报错
--通过系统表，查询词典模板取值（共5种）
select tmplname from PG_TS_TEMPLATE;
--testpoint1:创建simple词典，模板取值为simples，合理报错
drop TEXT SEARCH DICTIONARY if exists public.simple_dict;
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.simples,
     STOPWORDS = english
);
--testpoint2:创建Synonym词典，模板取值为synonyms，合理报错
drop TEXT SEARCH DICTIONARY if exists my_synonym;
CREATE TEXT SEARCH DICTIONARY my_synonym (
    TEMPLATE = synonyms,
    SYNONYMS = my_synonyms,
);
--testpoint3:创建Thesaurus词典，模板取值为Thesauru，合理报错
drop TEXT SEARCH DICTIONARY if exists thesaurus_astro;
CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
    TEMPLATE = thesauru,
    DictFile = thesaurus_astro,
    Dictionary = pg_catalog.english_stem,
);
--testpoint4:创建Ispell词典词典，模板取值为Ispells词典，合理报错
drop TEXT SEARCH DICTIONARY if exists test_ispell;
CREATE TEXT SEARCH DICTIONARY test_ispell (
    TEMPLATE = ispells,
    DictFile = ispell_sample,
    AffFile = ispell_sample,
);
--testpoint5:创建Snowball词典，模板取值为snowballs，合理报错
drop TEXT SEARCH DICTIONARY if exists snowball_test cascade;
CREATE TEXT SEARCH DICTIONARY snowball_test (
    TEMPLATE = snowballs,
    LANGUAGE = 'english',
    STOPWORDS = english);
--清理环境：no need to clean