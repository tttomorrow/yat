-- @testpoint:str位不加单引号时make_set的运算,部分测试用例合理报错

-- 输入数值类型
select make_set(3,3,2022-09-03);
select make_set(null,1,4,6);
select make_set(0,3);
select make_set(0,6-8,4,'[2010-01-01 14:30, 2010-01-01 15:30)','e');
select make_set(3,3/0,3-8);
select make_set(3,3/0,4/0);
select make_set(-2147483652,6,87,09,088);
select make_set(31,33/33,33/34,33|22,3&2);

-- 输入布尔类型
select make_set(3,false,true);
select make_set(null,true);
select make_set(0,false);
select make_set(3,true,false);
select make_set(-2147483652,true,false,true,false);

-- 输入日期类型
select make_set(3,2022-09-03,2022-09-03);
select make_set(null,2022-09-03);
select make_set(0,2022-09-03);
select make_set(3,1/8/1999,2022-09-03);
select make_set(3,01/02/03,false,true,false);
select make_set(3,01/02/03,99-Jan-08);
select make_set(3,01/02/03,J2451187);
select make_set(3,01/02/03,1999.008);

-- 输入其他类型
select make_set(3,false,好);
select make_set(3,￥￥,true);
select make_set(3,false,fine);
select make_set(3,B'101',true);
select make_set(3,a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11,true);
select make_set(3,false,192.168.100.128/25);

-- 输入空值
select make_set(3,false,);
select make_set(3,);

-- 输入null
select make_set(3,false,null);
select make_set(3,null,true);
