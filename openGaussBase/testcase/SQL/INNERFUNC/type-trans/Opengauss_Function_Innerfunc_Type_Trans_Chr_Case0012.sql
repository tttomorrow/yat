-- @testpoint: 类型转换函数to_char(numeric, text)数字类型的值转换为指定格式的字符串，入参为有效参数

--numeric 只指定p，缺省的比例是 0，即转化成整数精度
select to_char(-123.456::numeric(6),'999D999s');

-- numeric不指定p、s
SELECT to_char(-125.8, '999D99S');

--numeric p、s 都指定
select to_char(-123.456::numeric(6,3),'999D999s');

--小数位>指定s，四舍五入
select to_char(-123.456::numeric(6,2),'999D999s');

--模式串短，整数位不够显示#，小数位不够四舍五入
select to_char(-1239.456::numeric(7,3),'9999D9s');
select to_char(-1239.456::numeric(7,3),'999D999s');

-- 模式串长、短
select to_char(-1239.456::numeric(7,3),'0009999D9000s');
select to_char(-1239.456::numeric(7,3),'00000000');

--指定其它格式
select to_char(-1239.456::numeric(7,3),'08f9999D9000s');
select to_char(-1239.456::numeric(7,3),'*&……%￥');
