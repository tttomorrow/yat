--  @testpoint:结合存储过程，隐式游标，结合create语句，属性%FOUND的使用；

--前置条件
drop table if exists cur_test_148;
create table cur_test_148(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_148 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，结合create语句，隐式游标属性%FOUND，没有读记录返回，游标属性未生效；
drop procedure if exists cursor_ftest_148;
create or replace procedure cursor_ftest_148()
as
begin
    create table test_148(id int);
    if sql%found then
        delete from cur_test_148 where c_id <= 3;
    end if;
end;
/

call cursor_ftest_148();

--属性未生效，不影响下一步SQL执行结果
select * from cur_test_148;
drop table cur_test_148;
drop table test_148;
drop procedure cursor_ftest_148;
