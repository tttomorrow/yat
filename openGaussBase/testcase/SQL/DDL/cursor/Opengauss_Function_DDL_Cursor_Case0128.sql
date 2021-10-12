--  @testpoint:结合存储过程，隐式游标，结合delete语句，属性%FOUND的使用；

--前置条件
drop table if exists cur_test_128;
create table cur_test_128(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_128 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，结合delete语句，隐式游标属性%FOUND为True；
drop procedure if exists cursor_ftest_128;
create or replace procedure cursor_ftest_128()
as
declare
    fet_city varchar(10):= 'Suzhou';
begin
    delete from cur_test_128 where c_city = fet_city;
    if sql%found then
        update cur_test_128 set c_city ='Beijing' where c_id <= 3;
    end if;
end;
/

call cursor_ftest_128();
select * from cur_test_128;
drop table cur_test_128;
drop procedure cursor_ftest_128;
