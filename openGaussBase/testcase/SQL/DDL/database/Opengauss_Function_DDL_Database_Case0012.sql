-- @testpoint: 创建重名数据库，合理报错

drop database if exists test;
create database test with LC_COLLATE='zh_CN.gbk' LC_CTYPE = 'zh_CN.gbk' CONNECTION LIMIT=2;

create database test with LC_COLLATE='zh_CN.gbk' LC_CTYPE = 'zh_CN.gbk' CONNECTION LIMIT=2;

create database test with LC_COLLATE='C' LC_CTYPE = 'C' CONNECTION LIMIT=-1;

--tearDown
drop database if exists test;
