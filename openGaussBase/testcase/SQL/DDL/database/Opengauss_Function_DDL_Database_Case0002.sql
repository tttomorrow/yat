-- @testpoint: 创建数据库指定其字符编码
drop database if exists music;
CREATE DATABASE music ENCODING 'UTF-8' template = template0;
drop database if exists test_utf8;
CREATE DATABASE test_utf8 ENCODING 'UTF8' template = template0;
drop database if exists test_gbk;
CREATE DATABASE test_gbk ENCODING 'GBK' template = template0;
drop database if exists test_latin1;
CREATE DATABASE test_latin1 ENCODING 'Latin1' template = template0;

--tearDown
drop database if exists music;
drop database if exists test_utf8;
drop database if exists test_gbk;
drop database if exists test_latin1;