-- @testpoint: 创建数据库测试编码方式与区域匹配规则,合理报错

drop database if exists test;
create database test with ENCODING='SQL_ASCII'  LC_COLLATE = 'ayc_PE' LC_CTYPE =' ayc_PE';
drop database if exists test;
create database test with ENCODING='UTF8'  LC_COLLATE = 'ayc_PE' LC_CTYPE = 'ayc_PE';
create database test with ENCODING='ISO_8859_6'  LC_COLLATE = 'C' LC_CTYPE = 'C';
drop database if exists test;
create database test with ENCODING='LATIN9'  LC_COLLATE = 'POSIX' LC_CTYPE = 'POSIX';
drop database if exists test;
create database test with ENCODING='ISO_8859_6'  LC_COLLATE = 'UTF8' LC_CTYPE = 'UTF8';

--tearDown
drop database if exists test;
