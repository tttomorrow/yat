-- @testpoint: 列名出现关键字authid；authid大小写混合
drop table if exists test_authid_001 ;
create table test_authid_001 ("authid" int);
drop table if exists test_authid_001 ;