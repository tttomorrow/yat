--  @testpoint:关键字volatile,测试函数稳定级别

---对于“易变”（volatile）函数它是v，其结果可能在任何时候变化v也用于那些有副作用的函数，因此调用它们无法得到优化。


drop function if exists vol_test;
create function vol_test(integer,integer)
returns integer
as 'select $1+$2;'
language SQL
volatile
returns null on null input;
/
call vol_test(1,2);
call vol_test(1,2);
call vol_test(1,2);
call vol_test(1,2);
call vol_test(1,2);

drop function vol_test;
