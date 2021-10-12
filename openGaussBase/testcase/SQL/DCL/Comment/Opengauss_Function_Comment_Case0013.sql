--- Case Type： Comment
--- Case Name： 在约束上添加注释

--创建表，添加约束
drop table if exists constraint_comment;
create table constraint_comment(id int,name varchar(10),class varchar(10),
                                constraint ct_on_name primary key(name));

--给约束添加注释信息
comment on constraint ct_on_name on constraint_comment is '测试约束注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select oid from pg_constraint where conname='ct_on_name');

--清理环境
drop table constraint_comment;



