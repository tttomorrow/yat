-- @testpoint: 替换数组array中所有的指定元素，element用函数嵌套结果代替，部分合理报错

--返回类型一致
--函数返回值类型为int,替代element
select array_replace(array[1,2,2,3,5],(select length('world')),(select length('hello,world')));
select array_replace(array[1,2,33,5],((select 4/2 as result) ::int),(select lengthb('world')));
select array_replace(array[1.23,2.25,33,5.0],(select @ -5.0 as result),(select @ 8.0 as result));

--函数返回值类型为text,替代element
select array_replace(array['string','str','st','ring'],(select btrim('string' , 'ing')),(select substrb('string',2,3)));
select array_replace(array['string','str','st','tri','ring'],(select substrb('string',2,3)),(select btrim('string' , 'ing')));
select array_replace(array['string','str','st','ring'],(select left('abcde', 2)),(select repeat('ab', 3)));
select array_replace(array['abcd','str','ababab','abstring'],(select repeat('ab', 3)),(select left('abcde', 4)));

--函数返回值类型为bool，替代element
select array_replace(array[true,false,'1','0','T','F'],(select notlike(1,2)),((select array_lower('[0:2]={1,2,3}'::int[], 1) as result)::bool));
select array_replace(array[true,false,'1','0','T','F'],((select array_lower('[0:2]={1,2,3}'::int[], 1) as result)::bool),(select like(1,2)));

--返回类型不一致，合理报错
--函数返回值类型为text
select array_replace(array[1,2,2,3,5],(select left('abcde', 2)),(select length('hello,world')));
select array_replace(array[1,2,33,5],(select repeat('ab', 3)),(select lengthb('world')));
select array_replace(array[1.23,2.25,33,5.0],(select substrb('string',2,3)),(select @ 8.0 as result));

--函数返回值类型为int
select array_replace(array['string','str','st','ring'],(select length('string')),(select substrb('string',2,3)));
select array_replace(array['string','str','st','tri','ring'],(select lengthb('string')),(select btrim('string' , 'ing')));
select array_replace(array['string','str','st','ring'],(select @ -5.0 as result),(select repeat('ab', 3)));
select array_replace(array['abcd','str','ababab','abstring'],((select 4/2 as result) ::int),(select left('abcde', 4)));

--函数返回值类型为int和text
select array_replace(array[true,false,'1','0','T','F'],(select length('false')),((select array_lower('[0:2]={1,2,3}'::int[], 1) as result)::bool));
select array_replace(array[true,false,'1','0','T','F'],(select repeat('true', 2)),(select like(1,2)));
