--  @testpoint: 修改表空间，验证表空间名的大小写
CREATE TABLESPACE SPACE1 RELATIVE LOCATION 'tablespace/tablespace_1';

alter tablespace SPACE1 rename to space1;
alter tablespace space1 rename to SPACE1;
Select spcname From PG_TABLESPACE where spcname='space1';
Select spcname From PG_TABLESPACE where spcname='SPACE1';

--清理环境
DROP TABLESPACE space1;
