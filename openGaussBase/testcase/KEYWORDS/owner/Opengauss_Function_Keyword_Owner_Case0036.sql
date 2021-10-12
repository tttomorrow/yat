--  @testpoint:opengauss关键字owner(非保留)，表空间模式指定为用户,改变表空间所有者


CREATE ROLE joe IDENTIFIED BY 'Bigdata@123';
CREATE ROLE jay IDENTIFIED BY 'Bigdata@123';
CREATE TABLESPACE ds_location2 OWNER joe RELATIVE LOCATION 'tablespace/tablespace_1';
ALTER TABLESPACE ds_location2 OWNER TO jay;

DROP TABLESPACE ds_location2;
DROP ROLE joe;
DROP ROLE jay;