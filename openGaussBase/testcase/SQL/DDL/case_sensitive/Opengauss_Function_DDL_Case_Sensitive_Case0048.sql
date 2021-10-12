--  @testpoint: 创建表空间，验证表空间名大小写
CREATE TABLESPACE space1 RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE TABLESPACE SPACE1 RELATIVE LOCATION 'tablespace/tablespace_2';

--清理环境
DROP TABLESPACE space1;
DROP TABLESPACE SPACE1;