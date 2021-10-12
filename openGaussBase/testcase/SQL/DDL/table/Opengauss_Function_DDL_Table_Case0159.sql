-- @testpoint: 创建列类型是时间日期类型的列存表
DROP TABLE if exists date_type_tab;
CREATE TABLE date_type_tab (ab date,da time without time zone ,dai time with time zone,dfgh timestamp without time zone,dfga timestamp with time zone)with (ORIENTATION=COLUMN);
INSERT INTO date_type_tab VALUES ('2020-07-27','21:21:21','21:21:21 pst','2010-12-12','2013-12-11 pst');
DROP TABLE if exists date_type_tab;

