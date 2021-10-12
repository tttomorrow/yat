-- @testpoint: numrange(numeric, numeric, [text]) 描述：表示一个范围

select numrange(1.1,2.2,'[]') as result;
select numrange(5.1,6.7,'()') as result;
select numrange(5.1,6.7,'(]') as result;
select numrange(7.7,8.7,'[)') as result;
select numrange(1.1,'123','[]') as result;