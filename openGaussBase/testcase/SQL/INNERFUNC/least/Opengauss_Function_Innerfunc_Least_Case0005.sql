-- @testpoint: 有效值测试 参数类型相同
select least(-343232132,3423123,0) from sys_dummy;
select least(14541,5412121)from sys_dummy;
select least(145414343434232334343434234,541212133333333333333334,48898934434324343,365464435435345435454534324243234323)from sys_dummy;
-- 浮点型
select least(14541.2353212,5412121.23211454541)from sys_dummy;
select least(1453433323434342343441.2353212,5412121.23211454541,8748758479238928327434.123,98394834893489.93849328492374873247284783)from sys_dummy;
-- 字符型
select least('14541.2353212','5412121.23211454541','sdsdsdaffdfsfdfdff')from sys_dummy;
select least('14541.2353212','5412121.23211454541','sdsdsdaffdfsfdfdff','sdasdasdrfewrweeeefdssd')from sys_dummy;
select least('dsdasdsdsd','fdfdfdfdfdffsdf','sdsdsdaffdfsfdfdff','sdasdasdrfewrweeeefdssd')from sys_dummy;
select least('等级考试的考试','是打算打算打算','实打实大声道','啊实打实大声道')from sys_dummy;
select least('@!@-- @-- ','((_*(&*&*&((','{}(*)*(*)(*&^^%&**--','~~~~~~~~())(_)+++_+')from sys_dummy;
select least('?>>>>>>>>>>','...,.,.,.,.,,.,','.........。。。。。。','、。、。、。、。、。、。、')from sys_dummy;
-- bool型
select least(true,false)from sys_dummy;