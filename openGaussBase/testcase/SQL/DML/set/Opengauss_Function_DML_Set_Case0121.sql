-- @testpoint: 参数vacuum_defer_cleanup_age无效值测试,合理报错
--设置参数为小数，合理报错，ERROR:  parameter "vacuum_defer_cleanup_age" requires a numeric value
ALTER SYSTEM SET vacuum_defer_cleanup_age TO 10.5;
--查看参数值，仍然是0
show vacuum_defer_cleanup_age;
--设置参数为大于临界点的值1000001，合理报错，ERROR:  1000001 is outside the valid range for parameter "vacuum_defer_cleanup_age" (0 .. 1000000)
ALTER SYSTEM SET vacuum_defer_cleanup_age TO 1000001;
--设置参数为负数，合理报错，ERROR:  1000001 is outside the valid range for parameter "vacuum_defer_cleanup_age" (0 .. 1000000)
ALTER SYSTEM SET vacuum_defer_cleanup_age TO -1;
--设置参数为非法字符，合理报错，ERROR:  parameter "vacuum_defer_cleanup_age" requires a numeric value
ALTER SYSTEM SET vacuum_defer_cleanup_age TO '1$&^^%$$';