-- @testpoint: next_day函数参数week为英文
select next_day('2019-08-08','Sunday'),next_day('2019-08-08','Monday'),next_day('2019-08-08','Tuesday'),next_day('2019-08-08','Wednesday'),next_day('2019-08-08','Thursday'),next_day('2019-08-08','Friday'),next_day('2019-08-08','Saturday')
from sys_dummy;