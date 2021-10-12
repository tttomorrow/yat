-- @testpoint: 用在存储过程中

create or replace procedure abc
as
b_number number;
begin
select  1 into b_number from dual;
end;
/
drop procedure abc;