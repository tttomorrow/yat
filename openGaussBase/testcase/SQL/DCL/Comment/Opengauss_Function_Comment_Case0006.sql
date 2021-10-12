-- @testpoint: 在表空间上添加注释

--创建表空间
drop tablespace if exists tablespace_comment;
create tablespace tablespace_comment relative location 'tablespace/path_1';

--给表空间添加注释信息
comment on tablespace tablespace_comment is '测试表空间注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_shdescription where objoid=(select oid from pg_tablespace where spcname='tablespace_comment');

--清理环境
drop tablespace tablespace_comment;


