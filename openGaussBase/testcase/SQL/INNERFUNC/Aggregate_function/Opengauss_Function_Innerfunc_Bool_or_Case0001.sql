-- @testpoint: 函数bool_or，如果所有输入值只要有一个为真，则为真，否则为假。

select bool_or(100 <2500);
select bool_or(array[1.1,2.1,3.1]::int[] = array[1,2,3]);
select bool_or('a'='a');
select bool_or('a'>'a');
select bool_or('a'>'b');
select bool_or('a'<'b');
select bool_or('a=b'='b=a');
select bool_or(1);
