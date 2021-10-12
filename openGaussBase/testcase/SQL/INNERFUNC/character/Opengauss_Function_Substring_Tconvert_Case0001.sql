-- @testpoint: 函数tconvert(key text, value text，将字符串转换为hstore格式

select tconvert('aa', 'bb');
select tconvert('123@qazd', 'bb');
select tconvert(123, 'bb');
select tconvert('你好', 'bb');