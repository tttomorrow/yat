-- @testpoint:str的数值不满足当前bits位输出时make_set的运算

-- str值不包括空值
select make_set(31,'a','b','c','d');
select make_set(8,'a','b');
select make_set(12,'a','b');
select make_set(16,'a','b');
select make_set(20,'a','b');
select make_set(24,'a','b','e','f');

-- str值包括空值
select make_set(31,'a','b','c',null);
select make_set(8,null,'b');
select make_set(12,'a',null);
select make_set(16,null,'b');
select make_set(20,'a',null);
select make_set(24,'a','b',null,'f');

