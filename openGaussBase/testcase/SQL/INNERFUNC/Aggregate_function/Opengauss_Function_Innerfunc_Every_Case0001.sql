-- @testpoint: 函数every(expression)，等效于bool_and，如果所有输入值都是真，则为真，否则为假

select every(100 <2500);
select every(array[1.1,2.1,3.1]::int[] = array[1,2,3]);
select every('a'='a');
select every('a'>'a');
select every('a'>'b');
select every('a'<'b');
select every('a=b'='b=a');