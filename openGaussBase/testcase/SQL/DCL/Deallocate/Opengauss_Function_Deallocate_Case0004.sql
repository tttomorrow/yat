--- Case Type： Deallocate
--- Case Name： 未删除已创建的预备语句，再次创建，合理报错

--前置条件，创建表
drop table if exists deallocate_test1;
drop table if exists deallocate_test2;
create table deallocate_test1(id int,name varchar(10));
create table deallocate_test2(id int,name varchar(10));

--创建insert预备语句
prepare insert_sql(int,varchar(10)) as insert into deallocate_test1 values($1,$2);

--同一会话，未删除已创建的预备语句，再次创建，合理报错
prepare insert_sql(int,varchar(10)) as insert into deallocate_test2 values($1,$2);

--删除预备语句
deallocate insert_sql;

--清理环境
drop table deallocate_test1;
drop table deallocate_test2;

