-- @testpoint: next_day函数参数week使用数字1~7
select next_day('2020-06-13',1),next_day('2020-06-13',2),next_day('2020-06-13',3),next_day('2020-06-13',4),next_day('2020-06-13',5),next_day('2020-06-13',6),next_day('2020-06-13',7)
from sys_dummy;
