-- @testpoint: 有效值测试 参数类型相同
select least(14541,5412121)from sys_dummy;
-- 浮点型
-- 字符型
select least('dsdasdsdsd','fdfdfdfdfdffsdf','sdsdsdaffdfsfdfdff','sdasdasdrfewrweeeefdssd')from sys_dummy;
select least('等级考试的考试','是打算打算打算','实打实大声道','啊实打实大声道')from sys_dummy;
select least('@!@-- @-- ','((_*(&*&*&((','{}(*)*(*)(*&^^%&**--','~~~~~~~~())(_)+++_+')from sys_dummy;
select least('?>>>>>>>>>>','...,.,.,.,.,,.,','.........。。。。。。','、。、。、。、。、。、。、')from sys_dummy;
-- bool型
select least(true,false)from sys_dummy;