-- @testpoint: 关键字all带双引号作为普通表的列名，大小写混合
drop table if exists test_all_001 CASCADE ;
create table test_all_001 ("All" int);
drop table if exists test_all_001 CASCADE ;