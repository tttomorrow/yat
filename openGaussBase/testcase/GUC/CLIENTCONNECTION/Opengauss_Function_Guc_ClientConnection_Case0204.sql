-- @testpoint: alter system set方法设置参数fault_mon_timeout为无效值，合理报错
--查看默认
show fault_mon_timeout;
--设置超临界值，报错
ALTER SYSTEM SET fault_mon_timeout to -1;
ALTER SYSTEM SET fault_mon_timeout to 1441;
--设置浮点型，报错
ALTER SYSTEM SET fault_mon_timeout to 1582.256;
--设置字符型，报错
ALTER SYSTEM SET fault_mon_timeout to 'test';
ALTER SYSTEM SET fault_mon_timeout to '20%$#';
--设置空串，报错
ALTER SYSTEM SET fault_mon_timeout to '';
ALTER SYSTEM SET fault_mon_timeout to 'null';
--恢复默认值
ALTER SYSTEM SET fault_mon_timeout to 5;
