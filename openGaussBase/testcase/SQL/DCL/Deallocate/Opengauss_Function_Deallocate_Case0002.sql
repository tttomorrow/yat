--- Case Type： Deallocate
--- Case Name： 删除预备语句，语句不存在，合理报错

--前置条件，创建表
drop table if exists deallocate_test;
create table deallocate_test(id int,name varchar(10));

--删除预备语句，合理报错，预备语句不存在
deallocate insert_sql1;

--清理环境
drop table deallocate_test;

