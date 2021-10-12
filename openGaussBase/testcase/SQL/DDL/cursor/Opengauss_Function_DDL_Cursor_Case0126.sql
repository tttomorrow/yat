--  @testpoint:结合存储过程，隐式游标，结合update语句，属性%ROWCOUNT的使用；

--前置条件
drop table if exists cur_test_126;
create table cur_test_126(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_126 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，结合update语句，隐式游标属性%ROWCOUNT；
drop procedure if exists cursor_ftest_126;
create or replace procedure cursor_ftest_126()
as
declare
    fet_num int := 80;
begin
    update cur_test_126 set c_name = 'nnnlllccc' where c_num <= fet_num;
    if sql%rowcount > 2 then
        delete from cur_test_126 where c_id <= 3;
    end if;
end;
/

call cursor_ftest_126();
select * from cur_test_126;
drop table cur_test_126;
drop procedure cursor_ftest_126;
