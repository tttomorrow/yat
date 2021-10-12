--# -*- TIME:2020/6/16 14:35  -*-
--# @testpoint:date_part函数
--date_part函数是在传统的Ingres函数的基础上制作的（该函数等效于SQL标准函数extract）：
--date_part('field', source)这里的field参数必须是一个字符串，而不是一个名称。有效的field与extract一样，详细信息请参见EXTRACT。
SELECT date_part('day', TIMESTAMP '2001-02-16 20:38:40');
SELECT date_part('hour', INTERVAL '4 hours 3 minutes');