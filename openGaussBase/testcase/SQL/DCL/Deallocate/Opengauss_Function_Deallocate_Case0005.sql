--- Case Type： Deallocate
--- Case Name： 删除多个预备语句，参数all

--前置条件，创建表
drop table if exists deallocate_test;
create table deallocate_test(id int,name varchar(10));

--创建insert预备语句
prepare insert_sql(int,varchar(10)) as insert into deallocate_test values($1,$2);
--创建update预备语句
prepare update_sql(int,varchar(10)) as update deallocate_test set id=$1 where name=$2;
--创建delete预备语句
prepare delete_sql(int,varchar(10)) as delete from deallocate_test where id < $1;

--删除预备语句
deallocate all;

--执行任意预备语句，已不存在
execute update_sql(1,'a');

--清理环境
drop table deallocate_test;

