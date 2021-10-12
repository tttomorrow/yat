--  @testpoint:openGauss关键字template(非保留),
--opengauss模板数据库template0，创建新数据库成功
 DROP DATABASE IF EXISTS music1;
 CREATE DATABASE music1 ENCODING 'GBK' template = template0;
 DROP DATABASE music1; 
 
--opengauss模板数据库template1，创建新数据库失败，合理报错
 DROP DATABASE IF EXISTS music2;
 CREATE DATABASE music2 ENCODING 'GBK' template = template1;