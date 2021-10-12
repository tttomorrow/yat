-- @testpoint: null值
select avg(null) from sys_dummy order by 1;
select avg('') from sys_dummy order by 1;