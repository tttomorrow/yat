--- Case Type： Comment
--- Case Name： 在自定义类型上添加注释

--创建自定义类型
create type comfoo as (c1 int,c2 text);

--给自定义类型添加注释信息
comment on type comfoo is '测试自定义类型注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select oid from pg_type where typname='comfoo');

--清理环境
drop type comfoo;