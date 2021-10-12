--  @testpoint:删除不存在的类型映射，省略if exists，合理报错
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--查询文本搜索配置（没有映射记录）
SELECT b.cfgname,a.maptokentype,a.mapseqno,a.mapdict,c.dictname FROM pg_ts_config_map a,pg_ts_config b, pg_ts_dict c WHERE a.mapcfg=b.oid AND a.mapdict=c.oid AND b.cfgname='ngram2' ORDER BY 1,2,3,4,5;
--删除不存在的映射类型，省略if exists，合理报错
ALTER TEXT SEARCH CONFIGURATION ngram2 DROP MAPPING FOR multisymbol;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;