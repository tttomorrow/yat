--  @testpoint:临时模式（pg_temp）下创建词典，合理报错
--切换模式
set search_path to pg_temp;
--查看设置是否生效
show search_path;
--在 pg_temp模式下，创建simple词典，合理报错
DROP TEXT SEARCH DICTIONARY if exists pg_temp.simple_dict;
CREATE TEXT SEARCH DICTIONARY pg_temp.simple_dict (TEMPLATE = simple, Accept = false );
--恢复默认模式
reset search_path;
--清理环境  no need to clean