-- @testpoint: mod函数入参为字符处理函数
select mod(concat('434234','343434'),concat('4432','')) from sys_dummy;
select mod(concat('434234',''),concat('4432','')) from sys_dummy;
select case when 2>1 then mod(concat('434234','343434'),concat('4432','')) else 323 end from sys_dummy;
