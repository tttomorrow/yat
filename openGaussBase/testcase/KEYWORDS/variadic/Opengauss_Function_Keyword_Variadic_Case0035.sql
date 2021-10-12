--  @testpoint:关键字variadic，函数参数的模式，只有out模式参数后能跟variadic


create function variadic_test(variadic int[]) returns int
language sql as 'SELECT 1';

select variadic_test(0),
       variadic_test(0.0),
       variadic_test(variadic array[0.0]);