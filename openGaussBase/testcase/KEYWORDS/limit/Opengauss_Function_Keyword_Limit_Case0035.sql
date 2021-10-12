-- @testpoint: 关键字limit加引号作为普通表的列名
drop table if exists test_limit_001;
create table test_limit_001 ("limit" int);
--清理环境
drop table if exists test_limit_001;