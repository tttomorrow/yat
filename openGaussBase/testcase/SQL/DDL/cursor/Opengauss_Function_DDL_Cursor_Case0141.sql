--  @testpoint:结合存储过程，隐式游标，结合drop语句，属性%NOTFOUND的使用；

--前置条件
drop table if exists cur_test_141;
create table cur_test_141(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_141 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，结合drop语句，隐式游标属性%NOTFOUND，没有读记录返回，属性未生效
drop procedure if exists cursor_ftest_141;
create or replace procedure cursor_ftest_141()
as
begin
    drop table cur_test_141;
    if sql%notfound then
        create table cur_test_140(c_id int);
    end if;
end;
/

call cursor_ftest_141();

--属性未生效，不影响下一步SQL执行结果，合理报错
select * from cur_test_141;
drop table cur_test_141;
drop procedure cursor_ftest_141;
