--  @testpoint:generate_series函数测试
--testpoint1:generate_series(start, stop)函数，start, stop都为int型
SELECT * FROM generate_series(2,4);
--generate_series(start, stop)函数，start, stop都为numeric型
SELECT * FROM generate_series(2.1,4.1);
--generate_series(start, stop)函数，start为numeric型，stop为int
SELECT * FROM generate_series(2.5,4);
--testpoint2:generate_series(start, stop, step)
SELECT * FROM generate_series(5,1,-2);
--step是正数且start大于stop，则返回零行
SELECT * FROM generate_series(5,1,2);
--step是负数且start小于stop，则也返回零行
SELECT * FROM generate_series(5,6,-2);
--输入是NULL，同样产生零行
SELECT * FROM generate_series(null,null,null);
--step为零，合理报错
SELECT * FROM generate_series(5,6,0);
--start和stop是numeric型
SELECT * FROM generate_series(-5.5,-1.5,2);
--testpoint3:generate_series(start, stop, step interval)
--start和stop是timestamp
SELECT * FROM generate_series('2008-03-01 00:00'::timestamp, '2008-03-04 12:00', '10 hours');
--start和stop是timestamp  with time zone
SELECT * FROM generate_series('2013-12-11 pst'::timestamp with time zone, '2013-12-14 pst', '10 hours');




