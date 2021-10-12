--  @testpoint: 子查询验证表名大小写
CREATE TABLESPACE SPACE1 RELATIVE LOCATION 'tablespace/tablespace_1';
Select spcname From PG_TABLESPACE where spcname='space1';
Select spcname From PG_TABLESPACE where spcname='SPACE1';
--清理环境
DROP TABLESPACE space1;
