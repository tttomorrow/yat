-- @testpoint: 函数bool_or，如果所有输入值只要有一个为真，则为真，否则为假。当入参输入两种数据类型不一致时，合理报错

select bool_or('a'<1);
select bool_or(array[1.1,2.1,3.1]::int[] =[1,2,3]);
select bool_or(@);
select bool_or('@');