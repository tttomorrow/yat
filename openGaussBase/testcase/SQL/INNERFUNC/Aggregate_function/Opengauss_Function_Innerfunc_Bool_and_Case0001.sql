-- @testpoint: 函数bool_and，如果所有输入值都是真，则为真，否则为假

select bool_and(100 <2500);
select bool_and(array[1.1,2.1,3.1]::int[] = array[1,2,3]);
select bool_and('a'='a');
select bool_and('a'>'a');
select bool_and('a'>'b');
select bool_and('a'<'b');
select bool_and('a=b'='b=a');
select bool_and(0);