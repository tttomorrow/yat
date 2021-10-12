-- @testpoint:  函数every(expression)，当入参输入两种数据类型不一致时，合理报错

select every('a'<1);
select every(array[1.1,2.1,3.1]::int[] =[1,2,3]);
