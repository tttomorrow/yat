--- Case Type： Deallocate
--- Case Name： 删除预备语句，语句存在

--前置条件，创建表
drop table if exists deallocate_test;
create table deallocate_test(id int,name varchar(10));

--创建insert预备语句
prepare insert_sql(int,varchar(10)) as insert into deallocate_test values($1,$2);

--执行预备语句
execute insert_sql(1,'a');
insert into deallocate_test values(1,'a');

--删除预备语句
deallocate insert_sql;

--再次执行预备语句，语句已不存在
execute insert_sql(1,'a');

--清理环境
drop table deallocate_test;

