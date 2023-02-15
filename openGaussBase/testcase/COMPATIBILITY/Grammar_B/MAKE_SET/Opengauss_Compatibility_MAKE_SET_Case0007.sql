-- @testpoint:bits位输入字母或其他或null时make_set的运算,部分测试用例合理报错

select make_set(null,'a','b','c','d');
select make_set(null,'a','b');
select make_set(null,'a','b','c',null);
select make_set(null,null,'b');
select make_set(null,'a',null);

select make_set(a,'a','b','c',null);
select make_set(c,null,'b');
select make_set(h,'a',null);
select make_set(j,'a','b');
select make_set(l,'a','b');
select make_set(我,'a','b');
select make_set(天,'a','b','e','f');
select make_set(wa,'a','b');
select make_set(.,'a','b');
select make_set(&,'a','b');
select make_set(！,'a','b','e','f');
